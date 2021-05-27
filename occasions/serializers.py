from rest_framework import serializers

from authentication.serializers import CustomUserSerializer
from occasions.models import Occasion, Comment, Resolutions


class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = ['id', 'created_at', 'title', 'image', 'lat', 'lng', 'description', 'severity', 'updated_at', 'status',
                  'resolved', 'rejected']


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    reply_to = RecursiveField(many=False, read_only=True, required=False)
    occasion = OccasionSerializer(many=False, read_only=True)
    user = CustomUserSerializer(many=False, read_only=True)
    occasion_id = serializers.IntegerField(write_only=True)
    reply_to_id = serializers.IntegerField(write_only=True, required=False)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'text', 'reply_to', 'occasion', 'user', 'occasion_id', 'reply_to_id', 'user_id']


class ResolutionsSerializer(serializers.ModelSerializer):
    resolved = serializers.IntegerField(required=False, default=0)
    rejected = serializers.IntegerField(required=False, default=0)
    occasion_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Resolutions
        fields = ['id', 'resolved', 'rejected', 'occasion_id', 'user_id']


class ResolutionsResponseSerializer(serializers.Serializer):
    option = serializers.CharField(max_length=100)
    resolved = serializers.IntegerField()
    rejected = serializers.IntegerField()
