# 베이스 이미지 설정
# 모든 Dockerfile은 FROM 지시어를 반드시 한 번 이상 입력해야 함
# 이미지 이름의 포맷은 docker run에서 사용하는 이미지 이름과 동일함
FROM python:3.10-slim

# LABEL은 해당 Dockerfile에 대한 설명이라 할 수 있음
LABEL maintainer="Ju-Yeon Lim <rundollyrun8@gmail.com>"
LABEL description="Feedflow's Django Server"

# 작업 디렉터리(명령어를 실행할 디렉토리) 설정(create)
# 후속 명령들은 해당 디렉터리에서 실행
WORKDIR /app

# 필요한 패키지 설치
# Pipfile과 Pipfile.lock을 /app 디렉터리로 복사
COPY Pipfile Pipfile.lock /app/

# pipenv 설치 뒤, Pipfile.lock에 명시된 패키지 설치
# --deploy: 패키지를 잠금 파일에서만 설치하게 함
# --ignore-pipfile: Pipfile을 무시하고 Pipfile.lock만 참조
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# 프로젝트 소스 복사
# 현재 로컬 디렉터리의 모든 파일을 컨테이너의 /app 디렉터리로 복사
COPY . /app/

# CMD: 해당 이미지로 컨테이너 실행 시 어떤 명령어를 수행할 것인지 결정 => 딱 한 번만 사용 가능
# Gunicorn을 통해 Uvicorn을 실행하도록 설정
CMD ["pipenv", "run", "gunicorn", "--config", "/app/config/gunicorn_config.py", "config.asgi:application"]
