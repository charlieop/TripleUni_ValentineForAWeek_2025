from rest_framework import serializers
from ..models import Image

class GetImageSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()
    def get_path(self, obj):
        return obj.image.url
    
    class Meta:
        model = Image
        fields = ["id", "path"]
        read_only_fields = fields

    def to_representation(self, instance):
        if instance.deleted:
            return None
        return super().to_representation(instance)