import re
import requests
import markdown
from flask import Flask, render_template
from waitress import serve

app = Flask(__name__)

# GitHub repo info
GITHUB_REPO = "IMYdev/blog_posts"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"

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
    month_name = MONTHS.get(month.zfill(2), None)
    if not month_name:
        return 'Unknown Date'

    if len(year) == 2:
        year = '20' + year

    day = str(int(day))
    return f"{month_name} {day}, {year}"

def parse_post(filename, content):
    all_lines = content.split('\n')
    
    first_non_empty_line = None
    first_line_index = -1
    for i, line in enumerate(all_lines):
        if line.strip():
            first_non_empty_line = line.strip()
            first_line_index = i
            break
            
    content_to_render = content
    
    if first_non_empty_line and re.match(r'^\d{1,2}/\d{1,2}/\d{2,4}$', first_non_empty_line):
        date = format_date(first_non_empty_line)
        content_to_render = '\n'.join(all_lines[first_line_index + 1:])
    else:
        date = 'Unknown Date'
        
    html_content = markdown.markdown(content_to_render)
    clean_text = re.sub('<[^<]+?>', '', html_content)
    preview = clean_text[:50] + '...' if len(clean_text) > 50 else clean_text

    title = filename.replace('.md', '').replace('-', ' ').title()

    return {
        'title': title,
        'filename': filename,
        'date': date,
        'preview': preview,
        'content': html_content
    }

def get_posts():
    try:
        res = requests.get(GITHUB_API_URL)
        res.raise_for_status()
        files = res.json()
    except Exception as e:
        print("Error fetching posts:", e)
        return []

    posts = []
    for file in files:
        if file['name'].endswith('.md'):
            raw_url = f"{RAW_BASE_URL}/{file['name']}"
            try:
                content = requests.get(raw_url).text
                post_data = parse_post(file['name'], content)
                posts.append(post_data)
            except Exception as e:
                print(f"Error fetching {file['name']}: {e}")

    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts

def render_post(filename):
    raw_url = f"{RAW_BASE_URL}/{filename}"
    try:
        content = requests.get(raw_url).text
        return parse_post(filename, content)
    except Exception as e:
        print(f"Error fetching post {filename}: {e}")
        return None

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
