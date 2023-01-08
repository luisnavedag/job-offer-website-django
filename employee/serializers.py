from rest_framework import serializers
from .models import Employee, Skill
from . import validators
from user.models import User


class SkillSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Skill
        fields = [
            'name',
        ]

    def create(self, validated_data):
        Skill.objects.get_or_create(name=validated_data.get('name'))
        return Skill.objects.get(name=validated_data.get('name'))


class EmployeeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user = serializers.SerializerMethodField()
    city = serializers.CharField(allow_null=True, required=False, validators=[validators.validate_city])
    skills = SkillSerializer(many=True, required=False)

    class Meta:
        model = Employee
        fields = [
            'id',
            'user',
            'skills',
            'tags',
            'city',
            'linkdin',
            'status',
            'about_yourself'
        ]

    def create(self, validated_data):
        if validated_data.get('skills', None):
            skills = validated_data.pop('skills')
            instance = Employee.objects.create(**validated_data)
            for skill in skills:
                Skill.objects.get_or_create(name=skill['name'])
                s1 = Skill.objects.get(name=skill['name'])
                s1.save()
                instance.skills.add(s1)
            return instance
        else:
            return Employee.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('skills', None):
            instance.skills.clear()
            skills = validated_data.pop('skills')
            for skill in skills:
                s1, _ = Skill.objects.get_or_create(name=skill['name'])
                s1.save()
                instance.skills.add(s1)

        instance.tags = validated_data.get('tags', instance.tags)
        instance.city = validated_data.get('city', instance.city)
        instance.linkdin = validated_data.get('linkdin', instance.linkdin)
        instance.status = validated_data.get('status', instance.status)
        instance.about_yourself = validated_data.get('about_yourself', instance.about_yourself)
        instance.save()

        return instance

    def get_user(self, obj):
        return User.objects.get(email=obj.user).id
