from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Author
from .serializers import AuthorSerializer, AuthorLoginSerializer
from .permissions import IsSelfOrReadOnly

@extend_schema_view(
    list=extend_schema(responses={200: AuthorSerializer(many=True)}, auth=[]),
    retrieve=extend_schema(responses={200: AuthorSerializer}, auth=[]),
    create=extend_schema(responses={201: AuthorSerializer}, auth=[]),
    update=extend_schema(responses={200: AuthorSerializer}),
    partial_update=extend_schema(responses={200: AuthorSerializer}),
    destroy=extend_schema(responses={204: None}),
)
class AuthorViewSet(viewsets.ModelViewSet):
    """
    Pagination: 10 authors per page. / Пагинация: 10 авторов на страницу.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsSelfOrReadOnly]

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

class AuthorLoginView(generics.GenericAPIView):
    serializer_class = AuthorLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        try:
            author = Author.objects.get(username=username)
            if author.check_password(password):
                if not author.active:
                    return Response({"detail": "Author is inactive / Автор неактивен"}, status=status.HTTP_403_FORBIDDEN)
                refresh = RefreshToken.for_user(author)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
        except Author.DoesNotExist:
            pass
        
        return Response({"detail": "Invalid credentials / Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
