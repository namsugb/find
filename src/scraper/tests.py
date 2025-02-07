from googleapiclient.discovery import build

# API 키 입력 (YouTube Data API 키)
API_KEY = "AIzaSyAhGdo72nzBIcPFDl-VSGfBaNt6YIaLcHw"

# YouTube API 클라이언트 생성
youtube = build("youtube", "v3", developerKey=API_KEY)

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

# 테스트할 채널 ID (예: Google Developers 채널)
channel_id = "UCReNwSTQ1RqDZDnG9Qz_gyg"

# 채널의 재생목록 제목 가져오기
playlists = get_channel_playlists(channel_id)

if playlists:
    print("재생목록 제목:")
    for playlist in playlists:
        print(f"- {playlist['title']} (ID: {playlist['id']})")
else:
    print("재생목록을 가져올 수 없습니다.")