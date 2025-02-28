
# PythonBlog

Простой блог на Python с использованием Flask. Этот проект включает в себя базовые функции для создания и управления постами, а также систему просмотров и аутентификации.

## Установка и настройка

### 1. Клонирование репозитория
Склонируйте репозиторий на ваш локальный компьютер:
```bash
git clone https://github.com/DarkShyMW/PythonBlog.git
cd PythonBlog
```

### 2. Создание виртуального окружения
Создайте виртуальное окружение для изоляции зависимостей:
```bash
python -m venv venv
```

### 3. Активация виртуального окружения
- **Для Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **Для macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 4. Установка зависимостей
Установите все необходимые зависимости из файла `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 5. Запуск приложения
Запустите Flask-приложение:
```bash
python app.py
```
После этого приложение будет доступно по адресу: [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Используемые технологии
- **Flask** — микрофреймворк для создания веб-приложений.
- **Werkzeug** — библиотека для работы с безопасностью (хеширование паролей).
- **Markdown** — преобразование Markdown-текста в HTML.
- **SQLite** — база данных для хранения постов и пользователей.

---

## Структура проекта
```
PythonBlog/
├── app.py                # Основной файл приложения
├── requirements.txt      # Список зависимостей
├── venv/                 # Виртуальное окружение (не включено в репозиторий)
├── templates/            # HTML-шаблоны
│   ├── admin.html
│   ├── article.html
│   └── base.html
│   └── edit.html
│   └── index.html
│   └── login.html
├── static/               # Статические файлы (CSS, JS, изображения)
│   └── styles.css
└── database.py           # Модуль для работы с базой данных.
└── tux_ascii.py          # Забавный модуль над которым идет работа 
```

---

## Лицензия
Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

---

## Автор
- **DarkShyMW** — [GitHub](https://github.com/DarkShyMW)

---

Если у вас есть вопросы или предложения, создайте [issue](https://github.com/DarkShyMW/PythonBlog/issues) или свяжитесь со мной.

---
