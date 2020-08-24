from .models import Content
from rest_framework import serializers


class ContentSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.DateField(required=False, allow_null=True, format='%m/%d/%Y', input_formats=['%m/%d/%Y'])
    class Meta:
        model = Content
        fields = ['id' ,'content_type', 'url', 'author', 'date', 'title', 'content']