from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from users.serializers import UserRegistrationSerializers, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, sendPasswordResetEmailSerializer, userPasswordResetSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

# === adding custom renderer in view ===
from users.render.renderers import UserRenderer

# ===== Importing custom token =====
from users.token.token import get_tokens_for_user


# === Creating a UserRegistrationView ====
class UserRegistrationView(APIView):

    # added a custom renderer class
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializers(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            # ==== calling the TOken generating function function and storing in the variable ====
            token = get_tokens_for_user(user)

            return Response({'token': token, 'msg': 'User Successfully Created', 'data': serializer.data}, status=status.HTTP_201_CREATED)

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

