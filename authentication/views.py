from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password

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

