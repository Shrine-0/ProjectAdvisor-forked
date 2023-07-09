from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from users.serializers import UserRegistrationSerializers, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, sendPasswordResetEmailSerializer, userPasswordResetSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta


# ==== For refresh Token ====
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


# === adding custom renderer in view ===
from users.render.renderers import UserRenderer

# ===== Importing custom token =====
from users.token.token import get_tokens_for_user
from rest_framework.exceptions import APIException

## === For sending an email
from django.core.mail import send_mail
from django.conf import settings

# === Creating a UserRegistrationView ====
class UserRegistrationView(APIView):

    # added a custom renderer class
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        try:
            serializer = UserRegistrationSerializers(data=request.data)
    
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
    
                # ==== calling the Token generating function and storing in the variable ====
                token = get_tokens_for_user(user)
                
                
                # Send email to the user
                subject = 'Welcome to Wallet Wizzard'
                message = 'Thank you for signing up with Wallet Wizzard. We are excited to have you on board!'
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    
                return Response({'msg': 'User Successfully Created', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    
        except APIException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# === Login a USER ====
class UserLoginView(APIView):

    # added a custom renderer class
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):

        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            # ==== Authenticating email and passowrd ====
            user = authenticate(email=email, password=password)

            if user is not None:
                # ==== calling the TOken generating function function and storing in the variable ====
                # === print("Token is generated only when Login is successful") ===
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Successful', 'data': serializer.data}, status=status.HTTP_200_OK)

            else:
                return Response({'errors': {'non_field_errors': 'Email or password is not Valid'}}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# === Token REFRESHER ===
class UserTokenRefreshView(TokenObtainPairView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        authorization_header = request.headers.get('Authorization')
        if authorization_header is None or not authorization_header.startswith('Bearer '):
            return Response({'error': 'Invalid authorization header'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh_token = authorization_header.split(' ')[1]

        try:
            refresh = RefreshToken(refresh_token)
            refreshed_token = refresh.access_token

            # Set the expiration time for the new token
            expiry_time = timedelta(minutes=5)
            expiry_timestamp = int((datetime.now() + expiry_time).timestamp())
            refreshed_token.set_exp(expiry_timestamp)

            return Response({'access': str(refreshed_token), 'refresh': str(refresh)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class UserLogoutView(APIView):
#     def post(self, request, format=None):
#         refresh_token = request.data.get('refresh')

#         if not refresh_token:
#             return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             token = RefreshToken(refresh_token)
#             token.blacklist()

#             return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




# === USER PROFILE ====
class UserProfileView(APIView):
    # added a custom renderer class
    renderer_classes = [UserRenderer]

    # === adding a Permission ====
    permission_classes = [IsAuthenticated]

    def get(self, requset, format=None):

        # === Getting the detail of specific user only
        serializer = UserProfileSerializer(requset.user)

        return Response(serializer.data, status=status.HTTP_200_OK)


# === USER PASSWORD CHANGE ====
class UserChangePasswordView(APIView):
    # added a custom renderer class
    renderer_classes = [UserRenderer]

    # === adding a Permission ====
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # Sending data apart from request.data then we use context
        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})

        if serializer.is_valid(raise_exception=True):

            return Response({'msg': 'Password CHanged Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# === Sending an email to rest your password ====
class sendPasswordResetEmailView(APIView):

    # === added a custom renderer class to handle error ===
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):

        serializer = sendPasswordResetEmailSerializer(data=request.data)

        # NOTE: If you are raising an exception if is not required / necessary
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Reset Link has been send to your email. Please check your Email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# === View for reseting the password ====
class UserPasswordResetView(APIView):
    # === added a custom renderer class to handle error ===
    renderer_classes = [UserRenderer]

    # == Will not use authentication

    def post(self, request, uid, token, format=None):
        serializer = userPasswordResetSerializer(
            data=request.data, context={'uid': uid, 'token': token})

        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

