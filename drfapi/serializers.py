from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Value, Skill, Experience
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class ValueSerializer(serializers.HyperlinkedModelSerializer):
    experience_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Value
        fields = ['id', 'url', 'name', 'experiences', 'experience_names']
    
    def get_experience_names( self, obj):
        names = []
        for experience in obj.experiences.all():
            names.append(str(experience))
        return names
        
class SkillSerializer(serializers.HyperlinkedModelSerializer):
    experience_names = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = ['id', 'url', 'name', 'experiences', 'experience_names']
    
    def get_experience_names( self, obj):
        names = []
        for experience in obj.experiences.all():
            names.append(str(experience))
        return names
        
class ExperienceSerializer(serializers.HyperlinkedModelSerializer):
    skill_names = serializers.SerializerMethodField()
    value_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Experience
        fields = ['id', 'url', 'name', 'skill_names', 'value_names', 'skill_set', 'value_set']
        
    def get_skill_names( self, obj):
        names = []
        for skill in obj.skill_set.all():
            names.append(str(skill))
        return names
        
    def get_value_names( self, obj):
        names = []
        for value in obj.value_set.all():
            names.append(str(value))
        return names
        
class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator( queryset=User.objects.all() )])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password', 'password2']
        
    def validate(self, data):
        if ( data['password'] != data['password2'] ):
            raise serializers.ValidationError({ "Passwords do not match" })
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username']
        )
        
        user.set_password( validated_data['password'] )
        user.save()
        return (user)
        
class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator( queryset=User.objects.all() )])
    password = serializers.CharField(write_only=True, validators=[validate_password], required=False)
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password', 'password2']
        
    def validate(self, data):
        password = data.get('password', False)
        password2 = data.get('password2', False)

        if ( password != password2 ):
            raise serializers.ValidationError({ "Passwords do not match" })
        return data
        
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        
        password = validated_data.get('password', False)
        if (password != False):
            instance.set_password( password )
            
        instance.save()
        return (instance)