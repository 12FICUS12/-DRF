from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        status = data.get("status")
        count_advertisements = Advertisement.objects.filter(status="OPEN",
            creator=self.context["request"].user).count()
        if count_advertisements > 10 and self.context["request"].method == "POST" or status == "CLOSED" and \
                self.context["request"].method == "PUT":
            raise serializers.ValidationError(
                "Вы можете открыть не более 10 объявлений."
            )
        return data

