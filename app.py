from flask import Flask, render_template
import os
import re
import markdown
from datetime import datetime
from waitress import serve

app = Flask(__name__)

POSTS_DIR = 'posts'

def get_posts():
    posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(POSTS_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            title = filename.replace('.md', '').replace('-', ' ').title()
            date = datetime.fromtimestamp(os.path.getctime(filepath))
            
            html_content = markdown.markdown(content)
            clean_text = re.sub('<[^<]+?>', '', html_content)
            preview = clean_text[:50] + '...' if len(clean_text) > 50 else clean_text
            
            posts.append({
                'title': title,
                'filename': filename.replace('.md', ''),
                'date': date.strftime('%B %d, %Y'),
                'preview': preview,
                'content': html_content
            })
    
    return sorted(posts, key=lambda x: x['date'], reverse=True)

def render_post(filename):
    filepath = os.path.join(POSTS_DIR, f"{filename}.md")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    html_content = markdown.markdown(content)
    title = filename.replace('-', ' ').title()
    
    return {
        'title': title,
        'content': html_content,
        'filename': filename
    }

@app.route('/')
def index():
    posts = get_posts()
    return render_template('index.html', posts=posts)

@app.route('/post/<filename>')
def post(filename):
    post_data = render_post(filename)
    return render_template('post.html', post=post_data)

if __name__ == '__main__':
    serve(app)