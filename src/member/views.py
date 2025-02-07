from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, User, Skill, Material
from .serializers import CategorySerializer, UserSerializer, UserDetailSerializer, MaterialSerializer, SkillSerializer
from django.shortcuts import render
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

###주요페이지

def main(request):
    return render(request, 'explain.html')

def user_detail_view(request, user_id):
    page_owner = get_object_or_404(User, id=user_id)
    is_owner = request.user.is_authenticated and request.user.id == page_owner.id

    context = {
        'page_owner': page_owner,
        'is_owner': is_owner,
    }
    return render(request, 'user_detail.html', context)

def skill_resources_view(request, user_id, skill_id):
    page_owner = get_object_or_404(User, id=user_id)
    is_owner = request.user.is_authenticated and request.user.id == page_owner.id
    context = {
        'page_owner': page_owner,
        'is_owner': is_owner,
    }

    return render(request, 'skill_resources.html', context)

def findChannelView(request):
    return render(request, 'findChannel.html')


####### resful api

class CategorySkillListView(APIView):
    def get(self, request):
        categories = Category.objects.prefetch_related('skills').all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    

#메인 화면에서 Search 버튼을 누르면, 선택한 스킬을 가진 유저들을 보여주는 기능
class SkillUserSearchView(APIView):
    def get(self, request):

        skill_ids = request.query_params.getlist('skills', [])


        if not skill_ids:
            return Response({"error": "No skills provided"}, status=400)

        users = User.objects.filter(skills__id__in=skill_ids).distinct()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetailView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserDetailSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
class CategorySkillView(APIView):
    """
    특정 카테고리에 속하는 기술 목록 반환
    """
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        skills = category.skills.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class AddSkillView(APIView):
    """
    사용자에게 기술 추가
    """
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        skill_id = request.data.get('skill_id')


        if not skill_id:
            return Response({"error": "Skill ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            skill = Skill.objects.get(id=skill_id)
            user.skills.add(skill)
            user.save()
        except Skill.DoesNotExist:
            return Response({"error": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    

class SkillResourcesView(APIView):
    """
    특정 사용자의 특정 기술에 대한 자료 목록 반환
    """
    def get(self, request, user_id, skill_id):
        user = get_object_or_404(User, id=user_id)
        skill = get_object_or_404(Skill, id=skill_id)
        materials = user.materials.filter(skill=skill)
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)    
    
    def post(self, request, user_id, skill_id):
        skill = get_object_or_404(Skill, id=skill_id)
        user = get_object_or_404(User, id=user_id)  # URL에서 user_id로 사용자 객체 가져오기
        data = request.data
        data['skill'] = skill.id
        data['user'] = user.id  # user 필드 추가
        serializer = MaterialSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            materials = Material.objects.filter(skill=skill)
            return Response(MaterialSerializer(materials, many=True).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveSkillView(APIView):
    """
    사용자 기술 삭제 API
    """
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        skill_id = request.data.get('skill_id')

        if not skill_id:
            return Response({"error": "Skill ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            skill = Skill.objects.get(id=skill_id)
            user.skills.remove(skill)
            user.save()
        except Skill.DoesNotExist:
            return Response({"error": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    

class ResourceDeleteView(APIView):
    def delete(self, request, user_id, skill_id, resource_id):
        material = get_object_or_404(Material, id=resource_id)
        material.delete()
        skill = get_object_or_404(Skill, id=skill_id)
        materials = Material.objects.filter(skill=skill)
        return Response(MaterialSerializer(materials, many=True).data, status=status.HTTP_200_OK)


from scraper.services import get_channel_info, get_channel_playlists, get_videos_from_playlist, get_video_comments
from scraper.models import Channel, Playlist, Video, Comment, Score, candidate
from .serializers import ChannelSerializer, PlaylistSerializer


class addCandidateChannelView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        channel_id = request.data.get('channel_id')
        if not channel_id:
            return Response({"error": "Channel ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        if candidate.objects.filter(channel_id=channel_id).exists():
            return Response({"error": "Channel already exists :)"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            candidate(channel_id=channel_id).save()
            return Response({"success": "Channel added successfully"}, status=status.HTTP_201_CREATED)
        
        
class AddChannelView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "로그인 해야 채널 추가 가능"}, status=status.HTTP_401_UNAUTHORIZED)
        
        channel_id = request.data.get('channel_id')
        if not channel_id:
            return Response({"error": "Channel ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        if Channel.objects.filter(channel_id=channel_id).exists():
            return Response({"error": "Channel already exists :)"}, status=status.HTTP_400_BAD_REQUEST)

        # 채널 정보 가져오기
        channel_info = get_channel_info(channel_id)
        if not channel_info:
            return Response({"error": "Channel not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 채널 저장
        channel = Channel.objects.create(
            channel_id=channel_id,
            title=channel_info['channel_title'],
            profile_image_url=channel_info["profile_image_url"]
        )

        # 플레이리스트 가져오기
        playlists = get_channel_playlists(channel_id)
        playlist_instances = []
        for playlist in playlists:
            playlist_instances.append(Playlist(
                channel=channel,
                channel_title=channel.title,
                playlist_id=playlist["id"],
                title=playlist["title"]
            ))
        Playlist.objects.bulk_create(playlist_instances)

        # 비디오 및 댓글 저장
        video_instances = []
        comment_instances = []
        score_instances = []

        for playlist in playlist_instances:
            videos = get_videos_from_playlist(playlist.playlist_id)
            for video in videos:
                video_obj = Video(
                    playlist=playlist,
                    video_id=video["id"],
                    title=video["title"],
                    Channel=channel
                )
                video_instances.append(video_obj)

        Video.objects.bulk_create(video_instances)

        # 댓글 및 점수 저장
        for video in video_instances:
            comments = get_video_comments(video.video_id)
            for comment in comments:
                comment_instances.append(Comment(video=video, content=comment["text"]))
            
            num_of_thx_comments = sum(1 for c in comments if '감사' in c["text"])
            score_instances.append(Score(Channel=channel, Playlist=video.playlist, Video=video, thx_comment=num_of_thx_comments))

        Comment.objects.bulk_create(comment_instances)
        Score.objects.bulk_create(score_instances)

        serializer = ChannelSerializer(channel)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


from django.db.models import Q    
import time
from django.db.models import Count, Sum
class SearchChannelView(APIView):
    def post(self, request):
        tech = request.data.get('tech', '').lower()  # 검색 키워드 (소문자로 변환)
        
        # 동의어 사전 (수동 설정)
        SYNONYM_DICT = {
            "db": ["데이터베이스", "database"],
            "ai": ["인공지능", "머신러닝", "딥러닝"],
            "네트워크": ["network"],
            "big data": ["빅데이터"],
            "nlp": ["자연어 처리", "언어 모델"],
        }


        # ✅ 동의어 목록 확장
        keywords = set([tech])  # 기본 키워드 포함
        for key, synonyms in SYNONYM_DICT.items():
            if tech in synonyms or tech == key:
                keywords.update(synonyms)  # 동의어 추가
                keywords.add(key)

        print(f"🔍 확장된 검색어 목록: {keywords}")

        # ✅ 1. 플레이리스트와 비디오에서 키워드 검색
        query = Q()
        for keyword in keywords:
            query |= Q(title__icontains=keyword)  # 여러 개의 키워드로 OR 조건을 추가

        playlists = Playlist.objects.filter(query).select_related("channel").prefetch_related("videos")

        videos = Video.objects.filter(query).select_related("Channel").annotate(
            thanks_count=Count("comments", filter=Q(comments__content__icontains="감사"))
        )

        # ✅ 2. 채널별로 데이터 그룹화
        grouped_data = {}

        # ✅ 3. 플레이리스트 그룹화
        # 검색된 플레이리스트의 채널들을 grouped_data에 추가
        for playlist in playlists:
            channel_id = playlist.channel.id
            if channel_id not in grouped_data:
                grouped_data[channel_id] = {
                    "channel_id": playlist.channel.channel_id,
                    "channel_title": playlist.channel.title,
                    "playlists": [],
                    "videos": [],
                }

            # ✅ 해당 플레이리스트에 포함된 모든 동영상을 가져옴
            playlist_videos = videos.filter(playlist=playlist)

            # ✅ 플레이리스트 추가 (모든 동영상 포함)
            grouped_data[channel_id]["playlists"].append({
                "id": playlist.id,
                "title": playlist.title,
                "videos_in_playlist": [
                    {
                        "id": video.id,
                        "title": video.title,
                        "thanks_count": video.thanks_count
                    }
                    for video in playlist_videos
                ]
            })

        # ✅ 중복 비디오 ID 추출
        playlist_video_ids = {
            video["id"]
            for channel in grouped_data.values()
            for playlist in channel["playlists"]
            for video in playlist["videos_in_playlist"]
        }

        # ✅ 4. 비디오 그룹화
        for video in videos:
            if video.id in playlist_video_ids:
                continue  # 이미 playlist에 포함된 비디오는 제외

            channel_id = video.Channel.id
            if channel_id not in grouped_data:
                grouped_data[channel_id] = {
                    "channel_id": video.Channel.channel_id,
                    "channel_title": video.Channel.title,
                    "playlists": [],
                    "videos": [],
                }

            # ✅ 비디오 추가 (감사 댓글 수 포함)
            grouped_data[channel_id]["videos"].append({
                "id": video.id,
                "title": video.title,
                "thanks_count": video.comments.filter(content__icontains="감사").count()
            })

       
        # 5. 채널별로 감사 댓글 수 합산
        for channel_id, data in grouped_data.items():
            total_thanks_count = 0
            for playlist in data["playlists"]:
                for video in playlist["videos_in_playlist"]:
                    total_thanks_count += video["thanks_count"]
            for video in data["videos"]:
                total_thanks_count += video["thanks_count"]
            data["total_thanks_count"] = total_thanks_count     
            print(data["channel_title"])
            print(data["total_thanks_count"])
       

        # 6. 감사 댓글 수 기준으로 내림차순 정렬
        sorted_data = sorted(grouped_data.values(), key=lambda x: x["total_thanks_count"], reverse=True)

        sorted_channel_ids = [data["channel_id"] for data in sorted_data]
        
        sorted_channels_queryset = Channel.objects.filter(channel_id__in=sorted_channel_ids)
        
        sorted_channels = sorted(sorted_channels_queryset, key=lambda channel: sorted_channel_ids.index(channel.channel_id))
        serializer = ChannelSerializer(sorted_channels, many=True)
        return Response(serializer.data)
        
        