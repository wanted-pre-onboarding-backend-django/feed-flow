## Feed Flow

**소셜 미디어 통합 Feed 서비스**

> 언어 및 프레임워크 : Python 3.10 & Django 5.0, DRF 3.15

## Dev Environment Setting

### 프로젝트 폴더 바로 아래에 .env 파일을 만들고 아래 내용을 넣어주세요.
```
SECRET_KEY=your-secret-key
```

### 프로젝트 환경설정
아래의 명령어를 순서대로 실행해주세요.
```shell
# 1. 가상환경 만들기 (초기 설정 시 1회 실행)
> pipenv install
> pipenv install --dev

# 2. 가상환경 실행
> pipenv shell

# 3. pre-commit 실행 (초기 설정 시 1회 실행)
> pipenv run pre-commit install

# 4. django 실행하기
> python manage.py migrate
> python manage.py runserver
```


### 개발 명령어 모음

```shell
# formatter 실행
> black .

# linter 실행
> flake8

# 가상환경 종료
> deactivate

# 가상환경 삭제
> pipenv --rm

# 추가 패키지 설치 (가상환경 활성화 후 실행)
> pipenv install 패키지명

# 패키지 라이브러리 버전 확인
> pip show 패키지

# 관리자 계정 생성
> python manage.py createsuperuser
```

### Conventional Commits
```markdown
- feat: 새로운 기능을 추가할 때 사용.
- fix: 버그를 수정할 때 사용.
- docs: 문서에 대한 변경 사항을 기록할 때 사용 (코드 변경 없음).
- style: 코드의 의미에 영향을 주지 않는 변경 사항 (포맷팅, 세미콜론 누락 등).
- refactor: 코드 리팩토링 (기능 추가나 버그 수정 없음).
- test: 테스트 추가나 기존 테스트 수정.
- chore: 빌드 프로세스나 패키지 매니저 설정 등, 그 외의 변경 사항.
```


## 문서화 확인하는 방법
- [127.0.0.1:8000/swagger](127.0.0.1:8000/swagger) 또는 [127.0.0.1:8000/redoc](127.0.0.1:8000/redoc) 접속하기
