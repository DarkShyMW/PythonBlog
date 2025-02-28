from flask import Flask, render_template, request, redirect, url_for, session, Response
from werkzeug.security import generate_password_hash, check_password_hash
import os
import markdown
from functools import wraps
from database import init_db, get_views, increment_views, get_all_views, delete_views
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'very-secure-random-key')  # Используйте переменную окружения

# Конфигурация
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = generate_password_hash("secure_password123")  # Замените на свой пароль
ARTICLES_DIR = "articles"
BASE_URL = "http://localhost:5000/"  # Замените на ваш реальный домен

# Декоратор для проверки авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Получение первых 60 символов контента для мета-описания
def get_description(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    return content[:60] + "..." if len(content) > 60 else content

# Главная страница
@app.route('/')
def index():
    articles = []
    views = get_all_views()
    for filename in os.listdir(ARTICLES_DIR):
        if filename.endswith('.md'):
            articles.append({
                'filename': filename,
                'title': filename[:-3].replace('-', ' ').title(),
                'views': views.get(filename, 0)
            })
    return render_template('index.html', 
                         articles=articles, 
                         title="Мой Блог - Главная",
                         description="Добро пожаловать в мой блог с интересными статьями.")

# Страница статьи
@app.route('/article/<filename>')
def article(filename):
    filepath = os.path.join(ARTICLES_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = markdown.markdown(f.read())
        increment_views(filename)
        views = get_views(filename)
        title = filename[:-3].replace('-', ' ').title()
        description = get_description(filepath)
        return render_template('article.html', 
                             content=content, 
                             title=title,
                             description=description,
                             views=views)
    return "Article not found", 404

# Страница логина
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['logged_in'] = True
            return redirect(url_for('admin'))
        return render_template('login.html', 
                             error="Неверные учетные данные",
                             title="Вход - Мой Блог",
                             description="Вход для администратора блога.")
    return render_template('login.html', 
                         title="Вход - Мой Блог",
                         description="Вход для администратора блога.")

# Выход
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

# Админ-панель
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create' or action == 'edit':
            title = request.form.get('title').lower().replace(' ', '-')
            content = request.form.get('content')
            filename = f"{title}.md"
            with open(os.path.join(ARTICLES_DIR, filename), 'w', encoding='utf-8') as f:
                f.write(content)
            return redirect(url_for('admin'))
        
        elif action == 'delete':
            filename = request.form.get('filename')
            os.remove(os.path.join(ARTICLES_DIR, filename))
            delete_views(filename)
            return redirect(url_for('admin'))

    articles = []
    views = get_all_views()
    for filename in os.listdir(ARTICLES_DIR):
        if filename.endswith('.md'):
            articles.append({
                'filename': filename,
                'title': filename[:-3].replace('-', ' ').title(),
                'views': views.get(filename, 0)
            })
    return render_template('admin.html', 
                         articles=articles,
                         title="Админ-панель - Мой Блог",
                         description="Панель управления статьями блога.")

# Редактирование статьи
@app.route('/edit/<filename>', methods=['GET', 'POST'])
@login_required
def edit(filename):
    filepath = os.path.join(ARTICLES_DIR, filename)
    if not os.path.exists(filepath):
        return "Article not found", 404
        
    if request.method == 'POST':
        content = request.form.get('content')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return redirect(url_for('admin'))
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    title = filename[:-3].replace('-', ' ').title()
    description = get_description(filepath)
    return render_template('edit.html', 
                         content=content, 
                         filename=filename,
                         title=f"Редактировать: {title} - Мой Блог",
                         description=description)

# Генерация sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Главная страница
    url = ET.SubElement(urlset, "url")
    ET.SubElement(url, "loc").text = BASE_URL
    ET.SubElement(url, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(url, "priority").text = "1.0"
    
    # Страницы статей
    for filename in os.listdir(ARTICLES_DIR):
        if filename.endswith('.md'):
            url = ET.SubElement(urlset, "url")
            ET.SubElement(url, "loc").text = f"{BASE_URL}/article/{filename}"
            ET.SubElement(url, "lastmod").text = datetime.fromtimestamp(
                os.path.getmtime(os.path.join(ARTICLES_DIR, filename))
            ).strftime("%Y-%m-%d")
            ET.SubElement(url, "priority").text = "0.8"

    xml_str = minidom.parseString(ET.tostring(urlset)).toprettyxml(indent="  ")
    return Response(xml_str, mimetype='application/xml')

# Robots.txt
@app.route('/robots.txt')
def robots():
    robots_content = f"""User-agent: *
Allow: /
Disallow: /admin
Disallow: /edit/
Disallow: /login
Sitemap: {BASE_URL}/sitemap.xml
"""
    return Response(robots_content, mimetype='text/plain')

if __name__ == '__main__':
    if not os.path.exists(ARTICLES_DIR):
        os.makedirs(ARTICLES_DIR)
    init_db()
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)  # Для Windows