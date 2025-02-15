find는 개발 관련 유튜브 채널을 검색할 수 있는 웹 사이트입니다.

유저들이 추천하고 싶은 채널을 등록신청 할 수 있으며, 
공부하고 싶은 내용을 검색하면 내부 알고리즘에 의해 퀄리티가 좋은 순으로 정렬되어 채널들이 검색됩니다.



주요 코드들의 상세 위치입니다 참고 바랍니다 !!!!

**
src/member/views.py
**

가장하단에

AddChannelView == 채널 추가 로직

SearchChannelView == 채널 서치 로직



**
src/scraper/models.py
**

유튜브에서 가져온 데이터 저장한 모델


**
src/scraper/services.py
**

유튜브 api를 이용해 데이터 가져오는 코드
