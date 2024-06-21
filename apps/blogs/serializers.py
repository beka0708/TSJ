from rest_framework import serializers
from django_ckeditor_5.fields import CKEditor5Field
from .models import News


class CurrentNewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'type', 'title', 'description', 'link', 'is_approve')


class NewsSerializer(serializers.ModelSerializer):
    views_count = serializers.SerializerMethodField()
    description = CKEditor5Field()

    class Meta:
        model = News
        fields = ('id', 'type', 'title', 'description', 'link', 'views_count')

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        tsj_id = self.context['request'].user.profile.current_tsj_id
        request_vote = News.objects.create(
            from_user_id=user_id,
            tsj_id=tsj_id,
            **validated_data
        )
        return request_vote

    def get_views_count(self, obj):
        return obj.views.count()
