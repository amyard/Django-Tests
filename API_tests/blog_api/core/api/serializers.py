from rest_framework import serializers
from core.models import Post


class PostSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['url', 'pk', 'user', 'title', 'content', 'timestamp']
        read_only_fields = ['user']


    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        qs = Post.objects.filter(title__iexact == value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('The title muat be unique')
        return value