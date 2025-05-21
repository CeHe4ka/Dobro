from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from accounts.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        required_fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'birth_date']

        for field in required_fields:
            if field not in data:
                return Response({field: 'Обязательное поле'}, status=400)

        if data['password1'] != data['password2']:
            return Response({'password': 'Пароли не совпадают'}, status=400)

        try:
            validate_password(data['password1'])
        except ValidationError as e:
            return Response({'password': e.messages}, status=400)

        if CustomUser.objects.filter(email=data['email']).exists():
            return Response({'email': 'Email уже зарегистрирован'}, status=400)

        user = CustomUser.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password1'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=data['birth_date'],
            is_active=True
        )

        return Response({'message': 'Пользователь зарегистрирован'}, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'error': 'Email и пароль обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        if user is not None:
            return Response({
                'message': 'Успешный вход',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })
        else:
            return Response({'error': 'Неверные данные для входа'}, status=status.HTTP_401_UNAUTHORIZED)
