from rest_framework import serializers
from ..models import Task
from .ImageSerializer import GetImageSerializer

class GetTaskSerializer(serializers.ModelSerializer):
    imgs = serializers.SerializerMethodField()
    def get_imgs(self, obj):
        return GetImageSerializer(obj.imgs.filter(deleted=False), many=True, read_only=True).data
    
    class Meta:
        model = Task
        fields = [
            "day", "submit_text", "submit_by",
            "basic_completed", "basic_score",
            "bonus_score", "daily_score",
            "created_at", "updated_at",
            "imgs"
        ]
        read_only_fields = fields
        


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "match", "day", "submit_text", "submit_by",
        ]