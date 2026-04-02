# EduSphere — платформа адаптивного обучения

![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)
![Django](https://img.shields.io/badge/django-4.2-green?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)
![Status](https://img.shields.io/badge/status-прототип-orange?style=flat-square)

## Обзор проекта

**EduSphere** — веб-прототип образовательной платформы с **адаптивным обучением**: пользователи проходят курсы и викторины по урокам, система вычисляет **средний балл** по викторинам и обновляет **уровень** обучающегося (Beginner / Intermediate / Advanced), после чего предлагает **персональные рекомендации** курсов.

Проект выполнен в рамках **университетской работы** с использованием **ИИ-ассистированной разработки** (vibe coding в Cursor): ускорены каркас приложений, модели, представления, шаблоны и REST API при сохранении стека **Django**, **шаблонов**, **Bootstrap 5** и **Django REST Framework**.

**Ключевые возможности:** обновление уровня через **сигналы Django**, прохождение викторин с отправкой ответов в **DRF**, **виртуальный класс** с встраиванием видео и **чатом с опросом по HTTP**, **личный кабинет** с записями на курсы, историей викторин и рекомендациями.

---

## Возможности

Ниже перечислено то, что **реально реализовано** в коде.

### Пользователи

- **Регистрация** и **вход** на стандартной аутентификации Django (`accounts/views.py`, `accounts/urls.py`, `LoginView` / `LogoutView`).
- **Профиль** (`accounts.models.UserProfile`): уровень адаптации, поле **total_score** (средний процент по викторинам), **quizzes_taken**, **last_activity**.
- Страница профиля: `/accounts/profile/` (только для авторизованных).

### Курсы

- **Каталог курсов** с фильтром по сложности через параметр запроса `level` (`courses/views.py`).
- **Карточка курса** со списком уроков и кнопкой записи (`courses/templates/courses/detail.html`).
- Модель **Enrollment** с уникальностью пара «пользователь + курс».
- **Уроки**: заголовок, текст, опционально `video_url`, порядок `order` (`courses.models.Lesson`).

### Викторины

- **Одна викторина на урок** (`quizzes.models.Quiz` — связь `OneToOne` с `Lesson`).
- **Вопросы** с вариантами A–D (`quizzes.models.Question`).
- **Оценка** — доля верных ответов в процентах (`api.views.submit_quiz_api`); результат в `UserQuizResult` (**одна запись на пару пользователь–викторина**, повторная сдача **обновляет** существующую запись).
- Веб-интерфейс загружает вопросы через `GET /api/quizzes/<id>/`, отправка — `POST /api/quizzes/<id>/submit/` (`quizzes/templates/quizzes/take.html`).

### Адаптивное обучение

- Три уровня: **Beginner**, **Intermediate**, **Advanced** (`accounts.models.LEVEL_CHOICES`).
- После сохранения результата викторины **сигнал** пересчитывает **среднее** по всем `UserQuizResult` пользователя и выставляет уровень по порогам ≤50, 51–75, ≥76 (`adaptive/signals.py`).
- **Рекомендации:** курсы с `difficulty_level`, совпадающим с текущим уровнем пользователя, без уже записанных, не более 5 штук (`dashboard/views.py`, `api.views.recommendations_api`).

### Виртуальный класс

- В шаблонах урока и класса видео встраивается через `iframe` по полю `lesson.video_url` (например, embed YouTube).
- **Чат** по уроку: `GET` — список сообщений, `POST` — отправка; на фронте опрос каждые **3 секунды** (`classroom/templates/classroom/virtual.html`).

### Личный кабинет (дашборд)

- `/dashboard/`: уровень, записи на курсы с полем прогресса, история викторин, рекомендации (`dashboard/views.py`).

### REST API

- Представления DRF в `api/views.py`, маршруты — `api/urls.py`.
- Аутентификация: **сессия** и **токен** (`rest_framework.authtoken` в `Core/settings.py`). Часть эндпоинтов требует входа.

---

## Технологический стек

| Категория        | Технологии                                      |
|------------------|-------------------------------------------------|
| Бэкенд           | Django 4.x, Django REST Framework               |
| База данных      | SQLite по умолчанию (`db.sqlite3`)              |
| Фронтенд         | Django Templates, Bootstrap 5                   |
| Аутентификация   | Встроенная auth Django + DRF (Session, Token)   |
| Стили            | Bootstrap 5 (CDN)                             |
| Разработка       | Python 3.8+ (рекомендуется)                     |

---

## Структура проекта

Пакет настроек Django называется **`Core`** (модуль: `Core.settings`).

```text
EduSphere/                 # корень репозитория (имя папки после clone может отличаться)
├── manage.py
├── requirements.txt
├── Core/                    # настройки проекта и корневые URL
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                # регистрация, вход, профиль
├── courses/                 # курсы, уроки, записи; команда seed
├── quizzes/                 # викторины, вопросы, результаты
├── adaptive/                # сигналы адаптивной логики
├── classroom/               # виртуальный класс
├── dashboard/               # дашборд пользователя
├── api/                     # эндпоинты DRF
├── templates/               # общие шаблоны (например base.html)
└── static/                  # локальная статика (при необходимости)
```

---

## Установка и запуск

```bash
# Клонирование репозитория
git clone https://github.com/alirzw-mhjr/EduSphere.git
cd EduSphere

# Виртуальное окружение
python -m venv venv
# Linux / macOS:
source venv/bin/activate
# Windows (cmd):
venv\Scripts\activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Зависимости
pip install -r requirements.txt

# Миграции
python manage.py migrate

# Суперпользователь (опционально, для /admin/)
python manage.py createsuperuser

# Сервер разработки
python manage.py runserver
```

После запуска: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) — для гостей редирект на список курсов, для авторизованных — на дашборд (`Core/urls.py`).

---

## Демо-данные

Команда управления создаёт примеры курсов, уроков, викторин и вопросов:

```bash
python manage.py seed_edusphere
```

Реализация: `courses/management/commands/seed_edusphere.py`.

Альтернатива — заполнение через **админку** Django: `/admin/` после `createsuperuser`.

---

## API (эндпоинты)

Базовый префикс (локально): `http://127.0.0.1:8000/api/`

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/api/register/` | Регистрация; в ответе **токен** |
| POST | `/api/login/` | Вход; сессия + **токен** |
| GET | `/api/courses/` | Список курсов |
| GET | `/api/courses/<id>/` | Детали курса |
| POST | `/api/enroll/` | Запись на курс (тело: `course_id`) |
| GET | `/api/quizzes/<id>/` | Викторина и **вопросы** (нужна авторизация) |
| POST | `/api/quizzes/<id>/submit/` | Отправка ответов: `{ "answers": { "<id_вопроса>": "A" } }` |
| GET | `/api/recommendations/` | До 5 рекомендованных курсов (нужна авторизация) |
| GET | `/api/chat/<lesson_id>/` | Сообщения чата урока (нужна авторизация) |
| POST | `/api/chat/<lesson_id>/` | Отправить сообщение (поле `message`) |

Для скриптов: заголовок `Authorization: Token <ключ>` после регистрации или входа.

---

## Логика адаптивного обучения

1. У нового пользователя создаётся **UserProfile** (по умолчанию уровень **Beginner**) — сигнал при создании пользователя или ленивое создание в части представлений.
2. Каждая сдача викторины сохраняет **процент** 0–100 в `UserQuizResult`.
3. Сигнал пересчитывает **среднее** по всем результатам пользователя и задаёт уровень:
   - **≤ 50%** — Beginner  
   - **51%–75%** — Intermediate  
   - **≥ 76%** — Advanced  
4. Рекомендации: курсы с `difficulty_level`, равным текущему уровню, без уже записанных.

---

## Тестирование

```bash
python manage.py test

python manage.py test accounts
python manage.py test adaptive
python manage.py test api
```

В приложениях файлы `tests.py` по сути **заглушки**; для отчёта имеет смысл дополнить сценарии ручной проверки или написать `TestCase` для сигналов и API.

---

## Развёртывание

Сейчас конфигурация ориентирована на **разработку** (`DEBUG=True`, `SECRET_KEY` в коде — **не** для публичного продакшена).

Перед выкладкой:

- `DEBUG=False`, настройка **`ALLOWED_HOSTS`**
- **`SECRET_KEY`** и параметры БД из **переменных окружения**
- для нагрузки — **PostgreSQL** вместо SQLite
- **`python manage.py collectstatic`** и раздача статики через веб-сервер / CDN
- HTTPS, настройки CSRF и безопасных cookie

---

## Статус проекта

### Реализовано (прототип)

- Шесть предметных приложений + `api`, миграции SQLite, регистрация моделей в админке  
- Сигналы и обновление уровня, дашборд и API рекомендаций  
- Викторины через UI и DRF, виртуальный класс с опросом чата  
- Сессия + токен для API  

### Ограничения

- Доступ к урокам/викторинам/чату **не привязан жёстко** к факту записи на курс во всех местах (прототип)  
- Чат: **опрос HTTP**, не WebSockets; в шаблоне сообщения выводятся через `innerHTML` — для продакшена нужна санитизация  
- SQLite подходит для разработки, ограничена при высокой конкуренции записи  
- Поле **`max_score`** у модели викторины в расчёте процента **не используется**  
- **Один результат** на пару пользователь–викторина — повторы перезаписывают предыдущий результат  

### Возможное развитие

- Проверки прав: только для записанных на курс  
- Автотесты сигналов и API  
- PostgreSQL, настройки через env, WebSockets для чата  

---

## Благодарности

- Разработка с использованием **[Cursor](https://cursor.com/)** (vibe coding).  
- Идеи и итерации дизайна — с поддержкой **ChatGPT / LLM**.  
- Университетский учебный проект.  

---

## Лицензия

**MIT License**

---

## Автор

- **Имя:** [укажите своё имя]  
- **GitHub:** [@alirzw-mhjr](https://github.com/alirzw-mhjr)  
- **Репозиторий:** [https://github.com/alirzw-mhjr/EduSphere](https://github.com/alirzw-mhjr/EduSphere)  
