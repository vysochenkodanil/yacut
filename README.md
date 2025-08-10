YaCut - Сервис сокращения ссылок
Описание проекта

YaCut - это веб-сервис для создания коротких псевдонимов для длинных URL-адресов. Аналог популярных сервисов типа Bit.ly или TinyURL. Проект реализован на Flask и предоставляет как веб-интерфейс, так и REST API.
Основные возможности

    Создание коротких ссылок для длинных URL

    Возможность указания своего варианта короткой ссылки

    Веб-интерфейс с формой для создания ссылок

    REST API для интеграции с другими сервисами

    Перенаправление по коротким ссылкам

    Валидация вводимых данных

Технологии

    Python 3.7+

    Flask 2.0+

    Flask-WTF

    Flask-SQLAlchemy

    PostgreSQL (или SQLite для разработки)

    HTML5, Bootstrap 5

Установка и запуск

    Клонируйте репозиторий:



git clone https://github.com/vysochenkodanil/yacut.git
cd yacut

    Создайте и активируйте виртуальное окружение:



python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows

    Установите зависимости:



pip install -r requirements.txt

    Настройте окружение:
    Создайте файл .env в корне проекта:



FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=postgresql://username:password@localhost/yacut
SECRET_KEY=your-secret-key

    Инициализируйте базу данных:


flask db init
flask db migrate
flask db upgrade

    Запустите сервер:

flask run

Использование
Веб-интерфейс

Откройте в браузере http://localhost:5000 и используйте форму для создания коротких ссылок.
API

Пример запроса к API:
bash

curl -X POST -H "Content-Type: application/json" -d '{"url":"https://example.com/long-url"}' http://localhost:5000/api/id/
