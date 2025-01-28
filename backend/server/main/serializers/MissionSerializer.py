from rest_framework import serializers
from ..models import Mission

class GetMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ["title", "content", "link"]
        read_only_fields = fields
