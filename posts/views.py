from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Post
from .serializers import PostSerializer
from authors.permissions import IsAuthorOrReadOnly

@extend_schema_view(
    list=extend_schema(auth=[]),
    retrieve=extend_schema(auth=[]),
)
class PostViewSet(viewsets.ModelViewSet):
    """
    Pagination: 10 posts per page. / Пагинация: 10 постов на страницу.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filterset_fields = ['status', 'author']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
