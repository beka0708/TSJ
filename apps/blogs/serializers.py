from rest_framework import serializers
from django_ckeditor_5.fields import CKEditor5Field
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    views_count = serializers.SerializerMethodField()
    description = CKEditor5Field()

    class Meta:
        model = News
        fields = '__all__'

    def get_views_count(self, obj):
        return obj.views.count()
