# Blogging Platform API

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.17-red.svg)](https://www.django-rest-framework.org/)
[![Docker](https://img.shields.io/badge/Docker-✓-2496ED.svg)](https://docker.com)

REST API для блог-платформы с авторизацией через Google OAuth, системой постов, лайков и комментариев.

## 📋 Оглавление

- [Функциональность](#функциональность)
- [Технологии](#технологии)
- [API Документация](#api-документация)
- [Установка и запуск](#установка-и-запуск)

---

## 🚀 Функциональность

### 🔐 Аутентификация и пользователи
- Регистрация по email и паролю
- Вход по email и паролю с получением JWT токенов
- Вход через Google OAuth 2.0

### 📝 Посты
- Полный CRUD (создание, чтение, обновление, удаление)
- Права доступа: редактировать/удалять может только автор
- Просмотр доступен всем пользователям
- Автоматическое заполнение автора при создании

### ❤️ Лайки
- Поставить лайк посту
- Убрать лайк с поста
- Счётчик лайков для каждого поста
- Информация о том, лайкнул ли текущий пользователь пост

### 💬 Комментарии
- Добавление комментариев к постам
- Просмотр всех комментариев поста
- Счётчик комментариев
- Права доступа: редактировать/удалять может только автор

### 🔍 Фильтрация, поиск и сортировка
- Фильтр по автору (ID)
- Фильтр по дате создания (точная дата или диапазон)
- Поиск по заголовку и содержимому постов
- Сортировка по:
  - Дате создания
  - Заголовку
  - Количеству лайков
  - Количеству комментариев

### 📚 Документация API
- Swagger UI (`http://localhost:8000/api/docs/`)
---

## 🛠️ Технологии

| Технология | Назначение |
|------------|------------|
| Python | Язык программирования |
| Django | Веб-фреймворк |
| Django REST Framework | REST API фреймворк |
| PostgreSQL | База данных |
| Docker & Docker Compose |Контейнеризация |
| Simple JWT | JWT аутентификация |
| Google Auth | Google OAuth |
| drf-spectacular | OpenAPI документация |
| django-filter | Фильтрация |

---

## ⚙️ Установка и запуск

### Предварительные требования

- Docker и Docker Compose
- Git

### 1. Клонировать репозиторий

```bash
git clone git@github.com:Vladdikanov/Blogging-platform.git
cd BloggingPlatform
```
### 2. Создать файл .env
```bash
DB_NAME=blog_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

GOOGLE_CLIENT_ID=<СВОЙ GOOGLE_CLIENT_ID>
GOOGLE_CLIENT_SECRET=<СВОЙ GOOGLE_CLIENT_SECRET>
```

### 3. Запустить Docker контейнеры
```bash
docker-compose up -d --build
```
### 4. Применить миграции
```bash
docker-compose exec web python manage.py migrate
```
### 5. Создать суперпользователя
```bash
docker-compose exec web python manage.py createsuperuser
```
### 6. Проверить работу
Откройте в браузере:
```bash
Swagger: http://localhost:8000/api/docs/
Админка: http://localhost:8000/admin/
```