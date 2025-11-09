import os
import re
import markdown
from flask import Flask, render_template
from waitress import serve

app = Flask(__name__)

POSTS_DIR = 'posts'

MONTHS = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}

def format_date(date_str):
    parts = date_str.strip().split('/')
    if len(parts) != 3:
        return 'Unknown Date'

    day, month, year = parts
    month_name = MONTHS.get(month, None)
    if not month_name:
        return 'Unknown Date'

    if len(year) == 2:
        year = '20' + year

    day = str(int(day))

    return f"{month_name} {day}, {year}"

def parse_post(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = [line.strip() for line in content.split('\n') if line.strip()]
    if lines and re.match(r'^\d{1,2}/\d{1,2}/\d{2,4}$', lines[0]):
        date = format_date(lines[0])
        content = '\n'.join(lines[1:])
    else:
        date = 'Unknown Date'

    html_content = markdown.markdown(content)
    clean_text = re.sub('<[^<]+?>', '', html_content)
    preview = clean_text[:50] + '...' if len(clean_text) > 50 else clean_text

    filename = filepath.split("/")[1]
    title = filename.replace('.md', '').replace('-', ' ').title()

    return {
        'title': title,
        'filename': filename,
        'date': date,
        'preview': preview,
        'content': html_content
    }

def get_posts():
    posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(POSTS_DIR, filename)
            post_data = parse_post(filepath)
            posts.append(post_data)
    
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts

def render_post(filename):
    filepath = os.path.join(POSTS_DIR, f"{filename}")
    return parse_post(filepath)

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
