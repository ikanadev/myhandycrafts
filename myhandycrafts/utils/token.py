"""  Token jwt """

# Django
from config.settings.base import(
    ACCESS_TOKEN_LIFETIME,
    REFRESH_TOKEN_LIFETIME
)


# Django REST Framework
from rest_framework_simplejwt.tokens import RefreshToken

# Utilities
from datetime import timedelta

# Models
from myhandycrafts.users.models import User


def get_token(user):
    refresh_token = RefreshToken.for_user(user)
    refresh_token['username'] = user.username
    refresh_token['email'] = user.email
    return refresh_token

def get_response_token(user_pk):  # login

    user = User.objects.get(pk=user_pk)
    refresh = get_token(user)
    refresh.set_exp(lifetime=REFRESH_TOKEN_LIFETIME)
    access = refresh.access_token
    access.set_exp(lifetime=ACCESS_TOKEN_LIFETIME)

    response = {
        'access_token': str(access),  # access_token,
        'refresh_token': str(refresh),  # refresh_token,
        'reset_token': None,
        'token_type': "bearer"
    }

    return response