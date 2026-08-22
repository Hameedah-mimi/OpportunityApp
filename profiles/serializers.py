from rest_framework import serializers
from .models import StudentProfile, Skill, Interest


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            'id',
            'name',
        ]


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = [
            'id',
            'name',
        ]


class StudentProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    interests = InterestSerializer(many=True, read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id',
            'user',
            'university',
            'course',
            'graduation_year',
            'profile_image',
            'languages',
            'bio',
            'linkedin',
            'github',
            'portfolio',
            'cv',
            'skills',
            'interests',
        ]

        read_only_fields = [
            'user',
        ]