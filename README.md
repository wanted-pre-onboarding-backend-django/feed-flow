# FeedFlow

#### **소셜 미디어 통합 Feed 서비스**
[[원티드 백엔드 프리온보딩 인턴십]](https://www.wanted.co.kr/events/pre_ob_be_1_seoul) - 기업 실무 프로젝트 1차 과제

> 언어 및 프레임워크 : Python 3.10 & Django 5.0, DRF 3.15  
RDBMS : PostgreSQL 16.0 \
Server : Nginx, Uvicorn, Gunicorn\
ETC Tools : Docker(Compose), Git & Github, Notion, Discord

- 기간: 24.08.20 ~ 24.08.26

<br>

**목차**
1. [프로젝트 소개](#프로젝트-소개)
2. [프로젝트 구조 및 설계](#프로젝트-구조-및-설계)
3. [주요 기능](#주요-기능)
4. [API 명세서](#API-명세서)

<br>

## 프로젝트 소개
여러 소셜 미디어 플랫폼에 게시된 특정 해시태그가 포함된 게시물들을 한 곳에서 통합하여 보여주는 서비스입니다. \
사용자는 자신의 브랜드나 계정과 관련된 해시태그가 포함된 게시물과 해당 게시물의 통계를 일괄적으로 확인할 수 있습니다. \
이를 통해 개별 플랫폼을 일일이 확인할 필요 없이, 간편하게 브랜드와 관련된 여론, 리뷰, 평가 등을 모니터링할 수 있습니다.

## 프로젝트 구조 및 설계
#### 개발 환경 및 기술 스택
![image](https://github.com/user-attachments/assets/46501415-2656-4924-8588-7e872be2dd64)

### ERD
![image](https://github.com/user-attachments/assets/ad487190-e000-4433-ba9d-84e8bfaf6bf1)

### Service Architecture
![image](https://github.com/user-attachments/assets/9aef30b3-91df-48a0-b7ec-461977e25a1b)


### 디렉토리 구조

<details>
<summary>Directory Structure</summary>
<div markdown="1">

```
feed-flow/
|   .env
|   .flake8
|   .gitignore
|   docker-compose.yml
|   Dockerfile
|   manage.py
|   nginx.conf
|   Pipfile
|   Pipfile.lock
|           
+---article
|   +---apps.py
|   +---urls.py   
|   +---admin   
|   +---migrations
|   +---models
|   |       article.py
|   |       hashtag.py
|   |      
|   +---serializers
|   |       aricle_detail_serializer.py
|   |       article_list_serializer.py
|   |       article_statistics_serializer.py
|   |
|   +---tests
|   +---utils
|   |       article_site_dict.py       
|   \---views
|           article_detail_view.py
|           article_like_views.py
|           article_list_view.py
|           article_share_view.py
|           article_statistics_api_view.py
|           
+---config
|       gunicorn_config.py
\---user
    |   apps.py
    |   tests.py
    |   urls.py
    +---admin    
    +---models
    |       user.py     
    +---serializers
    |       tiny_user_serializer.py
    |       user_serializer.py 
    \---views
            __init__.py
```
</div>
</details>


### Setting Guide (Docker)
* 루트 디렉토리에 `.env` 밑처럼 세팅
```
SECRET_KEY= // 자체 입력
POSTGRES_DB=feedflowdb
POSTGRESQL_HOST=postgres => 해당 부분은 무조건 고정
POSTGRES_USER= // 자체 입력
POSTGRES_PASSWORD= // 자체 입력
TZ=Asia/Seoul
```

* Ubuntu (Debian Linux) 기준
```
-- 프로젝트 경로로 이동
cd [프로젝트 경로]

-- Docker Compose build & 실행 (=> http://127.0.0.1:8000/ 경로로 접속)
docker-compose up --build

-- 컨테이너 중지 및 생성된 컨테이너 삭제
docker-compose down

-- 로컬 도커 이미지 전체 삭제
docker rmi $(docker images -q)
```

### Developing Guide
[Developing Guide Link](https://github.com/wanted-pre-onboarding-backend-django/feed-flow/wiki/Develop-Guide)


## 주요 기능
- **회원가입 및 인증**: 계정 생성, 이메일 인증, JWT를 통한 인증 및 보안 유지.
- **통합 Feed**: 다양한 SNS의 게시물들을 통합하여 해시태그 기반으로 검색 및 필터링.
- **게시물 관리**: 게시물의 조회, 좋아요, 공유 기능 제공. 각 SNS의 API와 연동하여 실제 데이터를 기반으로 처리.
- **통계 기능**: 게시물의 개수, 조회 수, 좋아요 수, 공유 수 등의 통계를 일자별 또는 시간별로 조회 가능.


## API 명세서

| API 명칭            | HTTP 메서드 | 엔드포인트                | 설명                                |
|---------------------|-------------|---------------------------|-------------------------------------|
| 사용자 회원가입     | POST        | /signup                   | 새로운 사용자를 등록합니다.          |
| 사용자 가입승인     | PUT         | /signup-confirm           | 사용자를 가입 승인합니다.            |
| 사용자 로그인       | POST        | /login                    | 사용자를 로그인시킵니다.            |
| 게시물 목록 조회    | GET         | /articles                 | 게시물 목록을 조회합니다.           |
| 게시물 상세 조회    | GET         | /articles/:id             | 특정 게시물의 상세 정보를 조회합니다. |
| 게시물 좋아요       | PATCH       | /articles/:id/like        | 게시물에 좋아요를 추가합니다.       |
| 게시물 공유         | GET         | /articles/:id/share       | 게시물을 공유합니다.                |
| 통계 조회           | GET         | /articles/statistics      | 게시물 통계 정보를 조회합니다.      |

- [API 명세서 노션 링크](https://www.notion.so/034179/FeedFlow-2af2b82c6acc4ae3af8a0c593225ccc4?pvs=4#f5f3c11a023a47bd9a99f4e30335e029)



