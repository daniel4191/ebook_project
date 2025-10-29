FROM python:3.13-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사
COPY . /app/

# 정적 파일 수집을 위한 collectstatic 명령 실행을 위한 명령 추가
RUN python manage.py collectstatic --noinput || true

# 포트 노출
EXPOSE 8000

# Django 서버 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ebook_project.wsgi:application"]

