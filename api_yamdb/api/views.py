from rest_framework.generics import get_object_or_404
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import (EmailSerializer, ConfirmationCodeSerializer)
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


@api_view(['POST'])
def send_confirmation_code(request):
    if request.method == 'POST':
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.POST.get('email')
        user, state = User.objects.get_or_create(email=email)
        token = default_token_generator.make_token(user)
        send_mail(
            subject='Confirmation code!',
            message=str(token),
            from_email='example@mail.ru',
            recipient_list=[email, ]
        )
        return Response('Confirmation code отправлен на ваш Email.')
    return Response('Что-то пошло не так.')


@api_view(['POST'])
def send_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = request.POST.get('confirmation_code')
    email = request.POST.get('email')
    user = get_object_or_404(User, email=email)
    if confirmation_code is None:
        return Response('Введите confirmation_code')
    if email is None:
        return Response('Введите email')
    token_check = default_token_generator.check_token(user, confirmation_code)
    if token_check is True:
        refresh = RefreshToken.for_user(user)
        return Response(f'Ваш токен:{refresh.access_token}')
    return Response('Неправильный confirmation_code или email.')
