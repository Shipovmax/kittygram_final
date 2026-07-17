from __future__ import annotations

import base64
import datetime as dt
from typing import Any

import webcolors
from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Achievement, AchievementCat, Cat


class Hex2NameColor(serializers.Field):
    """Custom DRF field converting a hex colour string to its CSS name.

    On read, the stored CSS name is returned as-is. On write, an incoming
    hex value (e.g. ``#ff0000``) is resolved to the closest exact CSS
    colour name via ``webcolors``; unmatched hex values are rejected.
    """

    def to_representation(self, value: str) -> str:
        return value

    def to_internal_value(self, data: str) -> str:
        try:
            data = webcolors.hex_to_name(data)
        except ValueError as exc:
            raise serializers.ValidationError(
                'No matching CSS name for this colour'
            ) from exc
        return data


class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name')


class Base64ImageField(serializers.ImageField):
    """Accepts an image either as a multipart upload or as a base64 data URI.

    A ``data:image/<ext>;base64,<payload>`` string is decoded into a
    ``ContentFile`` before delegating to the standard ``ImageField``
    validation/handling.
    """

    def to_internal_value(self, data: Any) -> Any:
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CatSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(required=False, many=True)
    color = Hex2NameColor()
    age = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(
        'get_image_url',
        read_only=True,
    )

    class Meta:
        model = Cat
        fields = (
            'id', 'name', 'color', 'birth_year', 'achievements',
            'owner', 'age', 'image', 'image_url'
        )
        read_only_fields = ('owner',)

    def get_image_url(self, obj: Cat) -> str | None:
        if obj.image:
            return obj.image.url
        return None

    def get_age(self, obj: Cat) -> int:
        return dt.datetime.now().year - obj.birth_year

    def create(self, validated_data: dict[str, Any]) -> Cat:
        if 'achievements' not in self.initial_data:
            cat = Cat.objects.create(**validated_data)
            return cat
        achievements = validated_data.pop('achievements')
        cat = Cat.objects.create(**validated_data)
        for achievement in achievements:
            current_achievement, _created = (
                Achievement.objects.get_or_create(**achievement)
            )
            AchievementCat.objects.create(
                achievement=current_achievement, cat=cat
            )
        return cat

    def update(self, instance: Cat, validated_data: dict[str, Any]) -> Cat:
        instance.name = validated_data.get('name', instance.name)
        instance.color = validated_data.get('color', instance.color)
        instance.birth_year = validated_data.get(
            'birth_year', instance.birth_year
        )
        instance.image = validated_data.get('image', instance.image)

        if 'achievements' not in validated_data:
            instance.save()
            return instance

        achievements_data = validated_data.pop('achievements')
        lst = []
        for achievement in achievements_data:
            current_achievement, _created = (
                Achievement.objects.get_or_create(**achievement)
            )
            lst.append(current_achievement)
        instance.achievements.set(lst)

        instance.save()
        return instance
