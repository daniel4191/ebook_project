# Ebook 프로젝트

Django 기반의 전자책 판매 및 열람 플랫폼

## 프로젝트 개요

이 프로젝트는 Toss 포트폴리오 맞춤형으로, 복잡도 높은 Django 기반의 전자책 판매 및 열람 플랫폼입니다.

### 주요 기술 스택
- **Backend**: Django 5.2.7
- **Database**: PostgreSQL (운영), SQLite (개발)
- **인증**: django-allauth (소셜 로그인: 카카오, 구글, 네이버)
- **Frontend**: HTML, CSS, JavaScript (토스 브랜드 디자인)
- **배포**: Docker, AWS Lightsail, GitHub Actions CI/CD

## 프로젝트 구조

```
ebook_project/
├── ebook_project/          # 프로젝트 설정
├── users/                  # 사용자 앱
├── posts/                  # 포스트 앱
├── ebooks/                 # 전자책 앱
├── inquiries/              # 문의 앱
├── templates/              # HTML 템플릿
├── static/                 # 정적 파일 (CSS, JS, 이미지)
├── media/                  # 업로드된 파일
├── Dockerfile              # Docker 이미지 설정
├── docker-compose.yml      # Docker Compose 설정
└── requirements.txt        # Python 의존성

```

## 앱 구성

### 1. users 앱
- 커스텀 User 모델 (이메일 기반 인증)
- 소셜 로그인 (카카오, 구글, 네이버)
- 프로필 관리
- 비밀번호 정책: 숫자, 문자, 특수문자 필수, 3개 이상 연속 문자 불가

### 2. posts 앱
- 포스트 목록 (10개씩 pagination)
- 포스트 상세 (댓글 기능)
- 댓글 작성/수정/삭제
- 조회수 추적

### 3. ebooks 앱
- 전자책 목록 (3개씩 배열, 총 9개)
- 전자책 상세 (구매, 리뷰)
- 결제 시스템 (카카오페이, 네이버페이, 페이팔, 장바구니, 바로결제)
- 리뷰 시스템 (구매자만 작성 가능)
- 도서 읽기 (구매한 책만 접근 가능)
- Ebook 뷰어 (DRM/보안 기능)
  - 캡처 방지
  - 복사/붙여넣기 추적
  - 필기/하이라이트
  - 책갈피 기능

### 4. inquiries 앱
- 문의하기 (로그인 필수)
- 이메일 자동 전송

## 설치 및 실행

### 1. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 편집하여 필요한 설정 입력
```

### 2. Docker로 실행
```bash
docker-compose up -d
```

### 3. 마이그레이션
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### 4. 관리자 계정 생성
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. 정적 파일 수집
```bash
docker-compose exec web python manage.py collectstatic
```

### 6. 서버 접속
http://localhost:8000

## 개발 환경 설정

### 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 의존성 설치
```bash
pip install -r requirements.txt
```

### 데이터베이스 설정
```bash
python manage.py makemigrations
python manage.py migrate
```

### 슈퍼유저 생성
```bash
python manage.py createsuperuser
```

### 서버 실행
```bash
python manage.py runserver
```

## 배포

### AWS Lightsail 배포
1. GitHub에 코드 푸시
2. GitHub Actions가 자동으로 빌드 및 배포
3. 환경 변수는 GitHub Secrets에 설정

### 환경 변수 설정 필요 사항
- `DJANGO_SECRET_KEY`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `KAKAO_CLIENT_ID`, `KAKAO_SECRET`
- `GOOGLE_CLIENT_ID`, `GOOGLE_SECRET`
- `NAVER_CLIENT_ID`, `NAVER_SECRET`

## 주요 기능

### 인증 및 보안
- 이메일 기반 회원가입 (이메일 인증)
- 소셜 로그인 (카카오, 구글, 네이버)
- 비밀번호 정책 강제
- CSRF 보호

### 전자책 관리
- 전자책 CRUD
- 구매 관리
- 리뷰 시스템 (구매자만 작성 가능)
- 평점 자동 계산

### Ebook 뷰어 보안
- 캡처 방지 기술
- 복사/붙여넣기 추적 및 기록
- 필기 및 하이라이트
- 책갈피 기능

### 콘텐츠 관리
- 포스트 게시
- 댓글 시스템
- 조회수 추적

## 디자인 컨셉

토스 브랜드 색상을 활용한 깔끔하고 기분 좋은 디자인
- 주 색상: 파란색 (#4285F4)
- 보조 색상: 하늘색 (#90CAF9), 솜사탕색 (#FFD0EC)
- 반응형 웹 (모바일 호환)
- 햄버거 메뉴 (모바일)

## 다음 단계

1. 템플릿 디자인 완성
2. Ebook 뷰어 보안 기능 완성
3. 결제 시스템 연동
4. 테스트 코드 작성
5. 성능 최적화

## 라이선스

MIT License
