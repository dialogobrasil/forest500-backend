from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .models import *
from .documents import *

class TestSerializer(serializers.Serializer):
    nodes = serializers.ListField()
    links = serializers.ListField()


class StatusDocumentSerializer(DocumentSerializer):
    class Meta:
        document = StatusDocument
        fields = '__all__'

class StatusDocumentSerializer2(DocumentSerializer):
    class Meta:
        document = StatusDocument
        fields = '__all__'

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = "__all__"

class UserMentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMention
        fields = ['screen_name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['screen_name']

class OthertStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"

class StatusSerializer(serializers.ModelSerializer):   
    #retweet_status = OthertStatusSerializer(read_only=True)
    #quoted_status = OthertStatusSerializer(read_only=True)
    #hashtags = HashtagSerializer(read_only=True, many=True)
    user_mentions = UserMentionSerializer(read_only=True, many=True)
    user_screen_name = serializers.CharField(source='user.screen_name')

    class Meta:
        model = Status
        fields =['user_mentions','user_screen_name']