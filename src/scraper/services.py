from googleapiclient.discovery import build

# API 키 입력 (YouTube Data API 키)
API_KEY = "AIzaSyAhGdo72nzBIcPFDl-VSGfBaNt6YIaLcHw"

# YouTube API 클라이언트 생성
youtube = build("youtube", "v3", developerKey=API_KEY)


def get_channel_info(channel_id):
    """
    채널 ID로 채널 제목,  프로필 이미지를 가져오는 함수
    """
    # 채널 정보 요청
    request = youtube.channels().list(
        part="snippet,contentDetails",
        id=channel_id
    )
    response = request.execute()

    print(response)

    # 결과 파싱
    if "items" in response and len(response["items"]) > 0:
        channel_data = response["items"][0]
        channel_title = channel_data["snippet"]["title"]  # 채널 제목
        profile_image_url = channel_data["snippet"]["thumbnails"]["high"]["url"]  # 프로필 이미지 (고해상도)

        return {
            "channel_title": channel_title,
            "profile_image_url": profile_image_url
        }
    else:
        return None


def get_channel_playlists(channel_id):
    """
    채널 ID로 채널의 재생목록 제목들을 가져오는 함수
    """
    playlists = []
    request = youtube.playlists().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50  # 한 번에 가져올 수 있는 최대 개수
    )
    while request:
        response = request.execute()
        for item in response.get("items", []):
            playlist_title = item["snippet"]["title"]
            playlist_id = item["id"]
            playlists.append({"title": playlist_title, "id": playlist_id})
        # 다음 페이지가 있는지 확인
        request = youtube.playlists().list_next(request, response)
        
    return playlists


def get_videos_from_playlist(playlist_id):
    """
    플레이리스트 ID를 사용하여 비공개 영상 및 회원 전용 영상을 제외한 비디오 정보를 가져오는 함수
    """
    videos = []

    # API 요청 초기화
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults=50  # 한 번에 가져올 수 있는 최대 결과 수
    )

    # 모든 페이지의 비디오 정보 가져오기
    while request:
        response = request.execute()

        # 각 비디오 데이터 파싱
        for item in response.get("items", []):
            # 비공개 영상 및 회원 전용 영상 제외 조건
            snippet = item.get("snippet", {})
            if not snippet or snippet.get("title", "").lower() in ["private video", "this video is unavailable"]:
                continue

            # 회원 전용 영상은 'videoOwnerChannelTitle' 또는 기타 필드가 누락될 가능성이 있음
            if "videoOwnerChannelTitle" not in snippet:
                continue

            video_title = snippet.get("title")
            video_id = item["contentDetails"]["videoId"]
            published_at = item["contentDetails"]["videoPublishedAt"]

            videos.append({
                "title": video_title,
                "id": video_id,
                "published_at": published_at
            })

        # 다음 페이지 요청
        request = youtube.playlistItems().list_next(request, response)

    return videos


def get_video_comments(video_id):
    """
    비디오 ID로 해당 비디오의 댓글을 가져오는 함수 (예외 처리 포함)
    """
    comments = []

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100  # 한 번에 가져올 수 있는 최대 댓글 수
        )

        while request:
            try:
                response = request.execute()

                # 댓글 데이터 파싱
                for item in response.get("items", []):
                    comment = item["snippet"]["topLevelComment"]["snippet"]
                    text = comment.get("textDisplay", "N/A")  # 댓글 내용
                    author = comment.get("authorDisplayName", "Unknown Author")  # 작성자 이름
                    published_at = comment.get("publishedAt", "Unknown Date")  # 댓글 작성 시간

                    comments.append({
                        "author": author,
                        "text": text,
                        "published_at": published_at
                    })

                # 다음 페이지가 있는 경우 요청
                request = youtube.commentThreads().list_next(request, response)
            
            except Exception as e:
                print(f"댓글 요청 중 오류 발생 (비디오 ID: {video_id}): {e}")
                break

    except Exception as e:
        print(f"댓글 가져오기 실패 (비디오 ID: {video_id}): {e}")
        return []  # 오류 발생 시 빈 리스트 반환

    return comments




result = get_channel_info("UCReNwSTQ1RqDZDnG9Qz_gyg")

print(result)
