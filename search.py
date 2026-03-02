from load_json import load_json
from datetime import datetime

def parse_date(date_str):
    # Parses "2026年02月08日 10:34" format
    try:
        return datetime.strptime(date_str.split(' ')[0], '%Y年%m月%d日')
    except:
        return None

def search_contents(query, start_date=None, end_date=None, content_type='all'):
    if not query and not start_date and not end_date:
        return []

    articles = load_json('articles.json') if content_type in ['all', 'article'] else []
    videos = load_json('video.json') if content_type in ['all', 'video'] else []
    
    results = []
    query = query.lower() if query else ""
    
    start_dt = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
    end_dt = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

    # Search in articles
    for article in articles:
        text = (article.get('article_id', '') + 
                article.get('title', '') + 
                article.get('main_text', '') + 
                article.get('author', '') +
                ' '.join(article.get('categories', [])) +
                ' '.join(article.get('tags', []))).lower()
        
        post_dt = parse_date(article.get('time', ''))
        
        date_match = True
        if start_dt and (not post_dt or post_dt < start_dt): date_match = False
        if end_dt and (not post_dt or post_dt > end_dt): date_match = False
        
        if query in text and date_match:
            item = article.copy()
            item['type'] = 'article'
            item['id'] = article['article_id']
            item['url'] = f"/articles/{article['article_id']}"
            from app import strip_markdown
            item['preview'] = strip_markdown(article.get('main_text', ''))[:150]
            results.append(item)

    # Search in videos
    for video in videos:
        text = (video.get('video_id', '') + 
                video.get('title', '') + 
                video.get('main_text', '') +
                ' '.join(video.get('categories', [])) +
                ' '.join(video.get('tags', []))).lower()
        
        post_dt = parse_date(video.get('time', ''))
        
        date_match = True
        if start_dt and (not post_dt or post_dt < start_dt): date_match = False
        if end_dt and (not post_dt or post_dt > end_dt): date_match = False

        if query in text and date_match:
            item = video.copy()
            item['type'] = 'video'
            item['id'] = video['video_id']
            item['url'] = f"/video/summary/{video['video_id']}"
            from app import strip_markdown
            item['preview'] = strip_markdown(video.get('main_text', ''))[:150]
            results.append(item)

    return results
