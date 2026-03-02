from flask import Flask, render_template, request, redirect, send_from_directory, jsonify, session, Blueprint, url_for
from functools import wraps
from load_json import load_json
from save_json import save_json
from datetime import datetime
from random_string import random_string
import os
from dotenv import load_dotenv
import markdown

#from officez.routes import officez_bp

load_dotenv()

def convert_markdown(text):
    md = markdown.Markdown(extensions=[
        'tables',
        'fenced_code',
        'codehilite',
        'nl2br',
        'sane_lists'
    ], extension_configs={
        'codehilite': {
            'css_class': 'highlight',
            'linenums': False,
            'guess_lang': True
        }
    })
    return md.convert(text)

app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key-change-this')

ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')

def password_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session:
            error = None
            if request.method == 'POST':
                password = request.form.get('password')
                if password == ADMIN_PASSWORD:
                    session['authenticated'] = True
                    return redirect(request.url)
                else:
                    error = 'パスワードが違います'
            
            return f'''
                <!DOCTYPE html>
                <html lang="ja">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link rel="stylesheet" href="/static/style.css">
                    <title>管理者ログイン | トマト</title>
                </head>
                <body>
                    <div class="centre">
                        <div class="black"><h1>トマト</h1></div>
                        <section class="contact-info mt-lg" style="max-width: 500px;">
                            <h3>ここからは管理者画面です。パスワードを入力してください。</h3>
                            <form method="post" style="text-align: left; margin-top: var(--spacing-md);">
                                <input type="password" name="password" placeholder="パスワード" required 
                                       style="padding: var(--spacing-sm); border: 1px solid var(--color-border); 
                                              border-radius: var(--border-radius); width: 100%; font-family: var(--font-family); 
                                              margin-bottom: var(--spacing-md);">
                                {f'<p style="color: #e74c3c; margin-bottom: var(--spacing-md); text-align: center; font-weight: bold;">{error}</p>' if error else ''}
                                <button type="submit" class="btn" style="width: 100%;">ログイン</button>
                            </form>
                            <p style="margin-top: var(--spacing-md); text-align: center;">
                                <a href="/">トップに戻る</a>
                            </p>
                        </section>
                    </div>
                </body>
                </html>
                '''
        return f(*args, **kwargs)
    return decorated_function

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UK_DIR = os.path.join(BASE_DIR, 'en-UK')
US_DIR = os.path.join(BASE_DIR, 'en-US')
KR_DIR = os.path.join(BASE_DIR, 'KR')
KP_DIR = os.path.join(BASE_DIR, 'KP')
TW_DIR = os.path.join(BASE_DIR, 'zh-TW')
CN_DIR = os.path.join(BASE_DIR, 'zh-CN')
ES_DIR = os.path.join(BASE_DIR, 'ES')
DE_DIR = os.path.join(BASE_DIR, 'DE')
SV_DIR = os.path.join(BASE_DIR, 'SV')
AI_DIR = os.path.join(BASE_DIR, 'AI')

# Blueprint
def create_static_blueprint(name, directory, url_prefix=""):
    bp = Blueprint(
        name,
        __name__,
        url_prefix=url_prefix,
        template_folder=f"templates/{name}"
    )

    @bp.route("/")
    def index():
        return render_template("index.html")

    @bp.route("/about")
    def about():
        return render_template("about.html")

    @bp.route("/contents")
    def contents():
        return render_template("contents.html")

    @bp.route("/contact")
    def contact():
        return render_template("contact.html")

    return bp

# Japanese
app.register_blueprint(
    create_static_blueprint("ja", BASE_DIR, "")
)

# English(UK)
app.register_blueprint(
    create_static_blueprint("uk", UK_DIR, "/uk")
)

# English(US)
app.register_blueprint(
    create_static_blueprint("us", US_DIR, "/us")
)

# Korean(Rep. of Korea)
app.register_blueprint(
    create_static_blueprint("kr", KR_DIR, "/kr")
)

# Korean(Munhwa, D.P.R. Korea)
app.register_blueprint(
    create_static_blueprint("kp", KP_DIR, "/kp")
)

# Chines(Taiwan)
app.register_blueprint(
    create_static_blueprint("zh-tw", TW_DIR, "/zh-tw")
)

# Chinese(Mainland)
app.register_blueprint(
    create_static_blueprint("zh-cn", CN_DIR, "/zh-cn")
)

# Spanish(Spain)
app.register_blueprint(
    create_static_blueprint("es", ES_DIR, "/es")
)

# German(Germany)
app.register_blueprint(
    create_static_blueprint("de", DE_DIR, "/de")
)

# Swedish(Sweden)
app.register_blueprint(
    create_static_blueprint("sv", SV_DIR, "/sv")
)

# Ainu language(Hokkaido)
app.register_blueprint(
    create_static_blueprint("ai", AI_DIR, "/ai")
)

# OfficeZルートへ接続
zndquake_bp = Blueprint("zndquake", __name__)

@zndquake_bp.route("/")
def zndquake_main():
    return render_template("zndquake/main.html")

@zndquake_bp.route("/main")
def zndquake_main_rd():
    return render_template("zndquake/main.html")

@zndquake_bp.route("/about")
def zndquake_about():
    return render_template("zndquake/about.html")

@zndquake_bp.route("/dl")
def zndquake_dl():
    return render_template("zndquake/dl.html")

@zndquake_bp.route("/faq")
def zndquake_faq():
    return render_template("zndquake/faq.html")

@zndquake_bp.route("/contact")
def zndquake_contact():
    return render_template("zndquake/contact.html")

@zndquake_bp.route("/discord")
def zndquake_discord():
    return render_template("zndquake/discord.html")

@zndquake_bp.route("/main_zh")
def zndquake_main_zh():
    return render_template("zndquake/main_zh.html")

@zndquake_bp.route("/about_zh")
def zndquake_about_zh():
    return render_template("zndquake/about_zh.html")

@zndquake_bp.route("/dl_zh")
def zndquake_dl_zh():
    return render_template("zndquake/dl_zh.html")

@zndquake_bp.route("/faq_zh")
def zndquake_faq_zh():
    return render_template("zndquake/faq_zh.html")

@zndquake_bp.route("/contact_zh")
def zndquake_contact_zh():
    return render_template("zndquake/contact_zh.html")

@zndquake_bp.route("/discord_zh")
def zndquake_discord_zh():
    return render_template("zndquake/discord_zh.html")
'''
@zndquake_bp.route("/hanzi_map_t2s.json")
def zndquake_zh_hanzi_map_t2s():
    return render_template("zndquake/hanzi_map_t2s.json")

@zndquake_bp.route("/hanzi_map_s2t.json")
def zndquake_zh_hanzi_map_s2t():
    return render_template("zndquake/hanzi_map_s2t.json")'''

app.register_blueprint(zndquake_bp, url_prefix="/officez/products/zndquake")

# Search Routes
@app.route('/search')
def view_search():
    return render_template('search.html')

@app.route('/search/result')
def search_result():
    from search import search_contents
    query = request.args.get('q', '')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    content_type = request.args.get('type', 'all')
    
    results = search_contents(query, start_date, end_date, content_type)
    return render_template('result.html', query=query, results=results, start_date=start_date, end_date=end_date, type=content_type)

import re

def strip_markdown(text):
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)
    # Remove Markdown headers
    text = re.sub(r'#+\s*', '', text)
    # Remove bold/italic symbols
    text = re.sub(r'(\*\*|__|[\*_])', '', text)
    # Remove images and links notation but keep text
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    # Remove table symbols
    text = re.sub(r'\|', ' ', text)
    text = re.sub(r'[-:|]{3,}', ' ', text)
    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.route('/api/articles', methods=['GET'])
def get_articles():
    articles = load_json('articles.json')
    for article in articles:
        article['preview'] = strip_markdown(article.get('main_text', ''))[:150]
    return jsonify(articles)

@app.route('/articles', methods=['GET'])
def view_articles():
    articles = load_json('articles.json')
    for article in articles:
        article['preview'] = strip_markdown(article.get('main_text', ''))[:150]
    return render_template('articles.html', articles=articles)

@app.route('/articles/<article_id>', methods=['GET'])
def view_article(article_id):
    articles = load_json('articles.json')
    for article in articles:
        if article['article_id'] == article_id:
            article['main_text_html'] = convert_markdown(article['main_text'])
            return render_template('article.html', article=article)
    return redirect('/articles')

@app.route('/create', methods=['GET'])
@password_required
def view_create():
    return render_template('create.html')

def parse_comma_separated(text):
    if not text:
        return []
    items = text.split(',')
    processed = []
    for item in items:
        s = item.strip()
        if s:
            # Normalize hierarchy separator: "A>B", "A >B", "A> B" -> "A > B"
            if '>' in s:
                s = ' > '.join([part.strip() for part in s.split('>') if part.strip()])
            processed.append(s)
    return processed

@app.route('/create', methods=['POST'])
@password_required
def create_article():
    author = request.form.get('author', 'トマト')
    title = request.form.get('title', '')
    main_text = request.form.get('main_text', '')
    categories_raw = request.form.get('categories', '')
    tags_raw = request.form.get('tags', '')
    image_data = request.files.get('image_data')
    
    categories = parse_comma_separated(categories_raw)
    tags = parse_comma_separated(tags_raw)
    
    if not categories:
        return render_template('create.html', error='カテゴリは1つ以上入力してください', author=author, title=title, main_text=main_text, categories=categories_raw, tags=tags_raw)
    
    if len(categories) > 5:
        return render_template('create.html', error='カテゴリは最大5個までです', author=author, title=title, main_text=main_text, categories=categories_raw, tags=tags_raw)

    if title:
        articles = load_json('articles.json')
        article_id = random_string(8)
        
        image_name = ""
        if image_data and image_data.filename:
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            image_name = f"{article_id}_{image_data.filename}"
            image_data.save(os.path.join('uploads', image_name))
            
            if main_text:
                main_text = main_text.replace(image_data.filename, f"/uploads/{image_name}")
        
        time_now = datetime.now()
        post_time = time_now.strftime('%Y年%m月%d日 %H:%M')
        
        articles.append({
            'article_id': article_id,
            'author': author,
            'title': title,
            'main_text': main_text,
            'image_name': image_name,
            'time': post_time,
            'categories': categories,
            'tags': tags
        })
        
        save_json('articles.json', articles)
        return redirect('/articles')
    
    return render_template('create.html', error='タイトルは必須です', author=author, title=title, main_text=main_text, categories=categories_raw, tags=tags_raw)

@app.route('/edit/<article_id>', methods=['GET', 'POST'])
@password_required
def edit_article(article_id):
    articles = load_json('articles.json')
    target_article = None
    for article in articles:
        if article['article_id'] == article_id:
            target_article = article
            break
    
    if not target_article:
        return redirect('/articles')

    if request.method == 'POST':
        author = request.form.get('author', target_article['author'])
        title = request.form.get('title', target_article['title'])
        main_text = request.form.get('main_text', target_article['main_text'])
        categories_raw = request.form.get('categories', '')
        tags_raw = request.form.get('tags', '')
        
        categories = parse_comma_separated(categories_raw)
        tags = parse_comma_separated(tags_raw)
        
        if not categories:
            return render_template('edit.html', article=target_article, error='カテゴリは1つ以上入力してください（必須）')
        
        if len(categories) > 5:
            return render_template('edit.html', article=target_article, error='カテゴリは最大5個までです')

        target_article['author'] = author
        target_article['title'] = title
        target_article['categories'] = categories
        target_article['tags'] = tags
        
        image_data = request.files.get('image_data')
        if image_data and image_data.filename:
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            image_name = f"{article_id}_{image_data.filename}"
            image_data.save(os.path.join('uploads', image_name))
            target_article['image_name'] = image_name
            
            if main_text:
                main_text = main_text.replace(image_data.filename, f"/uploads/{image_name}")
        
        target_article['main_text'] = main_text
        
        time_now = datetime.now()
        target_article['updated_time'] = time_now.strftime('%Y年%m月%d日 %H:%M')
        
        save_json('articles.json', articles)
        return redirect(f'/articles/{article_id}')

    article_display = target_article.copy()
    article_display['categories_str'] = ', '.join(target_article.get('categories', []))
    article_display['tags_str'] = ', '.join(target_article.get('tags', []))
    
    return render_template('edit.html', article=article_display)

@app.route('/delete/<article_id>', methods=['POST'])
@password_required
def delete_article(article_id):
    articles = load_json('articles.json')
    new_articles = [a for a in articles if a['article_id'] != article_id]
    
    if len(articles) != len(new_articles):
        save_json('articles.json', new_articles)
        
    return redirect('/articles')

@app.route('/uploads/<image_name>', methods=['GET'])
def view_image(image_name):
    return send_from_directory('uploads', image_name)

# Video Routes

@app.route('/api/videos', methods=['GET'])
def get_videos():
    videos = load_json('video.json')
    for video in videos:
        video['preview'] = strip_markdown(video.get('main_text', ''))[:150]
    return jsonify(videos)

@app.route('/video', methods=['GET'])
def view_videos():
    videos = load_json('video.json')
    for video in videos:
        video['preview'] = strip_markdown(video.get('main_text', ''))[:150]
    return render_template('video.html', videos=videos)

@app.route('/video/summary/<video_id>', methods=['GET'])
def view_video_summary(video_id):
    videos = load_json('video.json')
    for video in videos:
        if video['video_id'] == video_id:
            video['main_text_html'] = convert_markdown(video['main_text'])
            return render_template('video_summary.html', video=video)
    return redirect('/video')

@app.route('/video/create', methods=['GET'])
@password_required
def view_create_video():
    return render_template('create_video.html')

@app.route('/video/create', methods=['POST'])
@password_required
def create_video():
    video_id = request.form.get('video_id', '')
    title = request.form.get('title', '')
    main_text = request.form.get('main_text', '')
    categories_raw = request.form.get('categories', '')
    tags_raw = request.form.get('tags', '')
    image_data = request.files.get('image_data')

    categories = parse_comma_separated(categories_raw)
    tags = parse_comma_separated(tags_raw)

    # バリデーション: 半角数字3文字
    if not video_id.isdigit() or len(video_id) != 3:
        return render_template('create_video.html', error='IDは半角数字3文字(000-999)で入力してください', video_id=video_id, title=title, main_text=main_text, categories=categories_raw, tags=tags_raw)

    # ID重複チェック
    videos = load_json('video.json')
    for v in videos:
        if v['video_id'] == video_id:
             return render_template('create_video.html', error='このIDは既に使用されています', video_id=video_id, title=title, main_text=main_text, categories=categories_raw, tags=tags_raw)

    if not categories:
        return render_template('create_video.html', error='カテゴリは1つ以上入力してください', video_id=video_id, title=title, main_text=main_text, categories=categories_raw, tags=tags_raw)
    
    if len(categories) > 5:
        return render_template('create_video.html', error='カテゴリは最大5個までです', video_id=video_id, title=title, main_text=main_text, categories=categories_raw, tags=tags_raw)

    if title:
        image_name = ""
        if image_data and image_data.filename:
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            image_name = f"{video_id}_{image_data.filename}"
            image_data.save(os.path.join('uploads', image_name))
            
            if main_text:
                main_text = main_text.replace(image_data.filename, f"/uploads/{image_name}")
        
        time_now = datetime.now()
        post_time = time_now.strftime('%Y年%m月%d日 %H:%M')
        
        videos.append({
            'video_id': video_id,
            'title': title,
            'main_text': main_text,
            'image_name': image_name,
            'time': post_time,
            'categories': categories,
            'tags': tags
        })
        
        save_json('video.json', videos)
        return redirect('/video')
    
    return render_template('create_video.html', error='タイトルは必須です', video_id=video_id, title=title, main_text=main_text, categories=categories_raw, tags=tags_raw)

@app.route('/video/edit/<video_id>', methods=['GET', 'POST'])
@password_required
def edit_video(video_id):
    videos = load_json('video.json')
    target_video = None
    for video in videos:
        if video['video_id'] == video_id:
            target_video = video
            break
    
    if not target_video:
        return redirect('/video')

    if request.method == 'POST':
        title = request.form.get('title', target_video['title'])
        main_text = request.form.get('main_text', target_video['main_text'])
        categories_raw = request.form.get('categories', '')
        tags_raw = request.form.get('tags', '')
        
        categories = parse_comma_separated(categories_raw)
        tags = parse_comma_separated(tags_raw)
        
        if not categories:
            return render_template('edit_video.html', video=target_video, error='カテゴリは1つ以上入力してください')
        
        if len(categories) > 5:
            return render_template('edit_video.html', video=target_video, error='カテゴリは最大5個までです')

        target_video['title'] = title
        target_video['categories'] = categories
        target_video['tags'] = tags
        
        image_data = request.files.get('image_data')
        if image_data and image_data.filename:
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            image_name = f"{video_id}_{image_data.filename}"
            image_data.save(os.path.join('uploads', image_name))
            target_video['image_name'] = image_name
            
            if main_text:
                main_text = main_text.replace(image_data.filename, f"/uploads/{image_name}")
        
        target_video['main_text'] = main_text
        
        time_now = datetime.now()
        target_video['updated_time'] = time_now.strftime('%Y年%m月%d日 %H:%M')
        
        save_json('video.json', videos)
        return redirect(f'/video/summary/{video_id}')

    video_display = target_video.copy()
    video_display['categories_str'] = ', '.join(target_video.get('categories', []))
    video_display['tags_str'] = ', '.join(target_video.get('tags', []))

    return render_template('edit_video.html', video=video_display)

@app.route('/video/delete/<video_id>', methods=['POST'])
@password_required
def delete_video(video_id):
    videos = load_json('video.json')
    new_videos = [v for v in videos if v['video_id'] != video_id]
    
    if len(videos) != len(new_videos):
        save_json('video.json', new_videos)
        
    return redirect('/video')

# 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    if not os.path.exists('articles.json'):
        save_json('articles.json', [])
    
    if not os.path.exists('video.json'):
        save_json('video.json', [])
    
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    app.run(debug=True, host='0.0.0.0', port=5000)
