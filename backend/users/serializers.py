from django.forms import ValidationError
from rest_framework import serializers
from users.models import myUser
from users.utils import Util

# importing necerries for sending email
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserRegistrationSerializers(serializers.ModelSerializer):

    # ===To COnfirm password ===
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = myUser
        fields = ['id', 'email', 'username', 'fName', 'lName', 'date_of_birth', 'tc', 'phone',
                  'is_admin', 'is_active', 'created_at', 'updated_at', 'password', 'password2']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    # === Validating the password only if it matches with password2 ====
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password does not match")

        return data

    def create(self, validated_data):
        return myUser.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255)

    class Meta:
        model = myUser
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = myUser
        fields = ['id', 'email', 'username', 'fName', 'lName',
                  'date_of_birth', 'phone', 'created_at', 'updated_at']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, min_length=8, style={
                                     'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, min_length=8, style={
                                      'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")

        else:
            user.set_password(password)
            user.save()

        return attrs


# === serializer for sending an email ===
class sendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    # validating email
    def validate(self, attrs):
        email = attrs.get('email')

        # === sends email only if it is found in the myUser Model
        if myUser.objects.filter(email=email).exists():
            user = myUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)

            # === Generating the PasswordResetToken ===
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = '\nhttp://localhost:3000/reset/'+uid+'/'+token+'/'
            print('Password Reset Link', link)
            # NOTE: Send email code is written here
            body = 'Click below link to reset your password' + link
            data = {
                'email_subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)

            return attrs

        else:
            raise ValidationError('You are not a Registered User')


# === serializer for reseting password ===
class userPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, min_length=8, style={
                                     'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, min_length=8, style={
                                      'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            
            if password != password2:
                raise serializers.ValidationError(
                    "Password and Confirm Password doesn't match")

            # Ensure uid is of type str
            uid = str(uid)
            
            # Decoding  the Id
            id = smart_str(urlsafe_base64_decode(uid))
            user = myUser.objects.get(id=id)

            # Check if token is vlaid or not
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError("Token is Invalid or Expired")
            user.set_password(password)
            user.save()
            return attrs
        
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError("Token is Invalid or Expired")
