from rest_framework import serializers
from django_ckeditor_5.fields import CKEditor5Field
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    views_count = serializers.SerializerMethodField()
    description = CKEditor5Field()

    class Meta:
        model = News
        fields = ('id', 'type', 'title', 'description', 'link', 'tsj', 'views_count')

    def create(self, validated_data):
        user_id = self.context['user_id']
        request_vote = News.objects.create(from_user_id=user_id, **validated_data)
        return request_vote

    def get_views_count(self, obj):
        return obj.views.count()
