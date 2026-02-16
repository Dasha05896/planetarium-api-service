FROM python:3.11-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Для SQLite нам потрібні лише базові бібліотеки для роботи з зображеннями (якщо є ImageField)
RUN apk add --update --no-cache \
    jpeg-dev \
    zlib-dev \
    libjpeg

COPY requirements.txt .

# Встановлюємо залежності без зайвих PostgreSQL пакетів
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Створюємо папки для медіа та статики
RUN mkdir -p /vol/web/media /vol/web/static

# Створюємо не-root користувача (це стандарт безпеки для Portfolio Project)
RUN adduser --disabled-password --no-create-home django-user

# ВАЖЛИВО для SQLite: користувач повинен мати права на запис у папку /app,
# де лежить файл db.sqlite3
RUN chown -R django-user:django-user /app/ /vol/
RUN chmod -R 755 /vol/web/

USER django-user