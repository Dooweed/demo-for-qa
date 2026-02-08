from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from .models import Author

class AuthorJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            author = Author.objects.get(id=user_id)
            if not author.active:
                raise exceptions.AuthenticationFailed('Author is inactive / Автор неактивен', code='user_inactive')
            return author
        except Author.DoesNotExist:
            raise exceptions.AuthenticationFailed('Author not found / Автор не найден', code='user_not_found')

class AuthorJWTAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = 'authors.authentication.AuthorJWTAuthentication'
    name = 'jwtAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
