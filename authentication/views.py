from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class RegisterUserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('firstName')
        last_name = request.data.get('lastName')

        # Check if the user with the same email already exists
        if User.objects.filter(email=email).exists():
            return Response({"error": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a new user
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email, # arbitrary but required in the django User model
                password=make_password(password)  # Hash the password before saving
            )
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": "Error creating user", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('email') # requires username to be here
        password = request.data.get('password')
        print(f'Email: {username}, Password: {password}')
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        #user = authenticate(request, username='srazzano15@gmail.com', password='password123')
        print(user)
        if user is not None:
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # This is the authenticated user
        user_data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
        }
        return Response(user_data, status=status.HTTP_200_OK)