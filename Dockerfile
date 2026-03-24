FROM python:3.11-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /app


RUN apk add --update --no-cache \
    jpeg-dev \
    zlib-dev \
    libjpeg

COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN mkdir -p /vol/web/media /vol/web/static


RUN adduser --disabled-password --no-create-home django-user


RUN chown -R django-user:django-user /app/ /vol/
RUN chmod -R 755 /vol/web/

USER django-user