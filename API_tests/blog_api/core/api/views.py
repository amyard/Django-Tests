from rest_framework import generics, mixins
from core.models import Post
from .serializers import PostSerializer
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly


class PostRUDViews(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Post.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {'reguest': self.request}


class PostAPIViews(mixins.CreateModelMixin, generics.ListAPIView):

    lookup_field = 'pk'
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = Post.objects.all()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(title__icontains = query)|Q(content__icontains = query)).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}