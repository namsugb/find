from rest_framework import serializers
from .models import Category, Skill, User, Material

class SkillSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Skill
        fields = ['id', 'name', 'description', 'category']

class CategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'skills']


class UserSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'profile_picture', 'skills']


class MaterialSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    class Meta:
        model = Material
        fields = ['id', 'title', 'link', 'description', 'created_at', 'skills']


class UserDetailSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'profile_picture', 'skills', 'materials']


from scraper.models import Channel, Playlist, Video
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'title', 'channel_id', 'profile_image_url']


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'title', 'playlist_id']        

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'video_id']        