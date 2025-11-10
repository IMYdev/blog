import re
import requests
import markdown
import datetime
from flask import Flask, render_template
from waitress import serve

app = Flask(__name__)

GITHUB_REPO = "IMYdev/blog_posts"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"

MONTHS = {
    '01': 'January', '02': 'February', '03': 'March', '04': 'April',
    '05': 'May', '06': 'June', '07': 'July', '08': 'August',
    '09': 'September', '10': 'October', '11': 'November', '12': 'December'
}

def parse_date_info(date_str):
    if not date_str:
        return datetime.date.min, 'Unknown Date'
        
    try:
        parts = date_str.strip().split('/')
        if len(parts) != 3:
            raise ValueError("Invalid date format")

        day, month, year = parts
        
        if len(year) == 2:
            year = '20' + year
        
        day_num = int(day)
        month_num = int(month)
        year_num = int(year)
        
        month_name = MONTHS.get(month.zfill(2), None)
        if not month_name:
            raise ValueError("Invalid month")

        formatted_date = f"{month_name} {day_num}, {year_num}"
        sortable_date = datetime.date(year_num, month_num, day_num)
        
        return sortable_date, formatted_date

    except Exception as e:
        print(f"Error parsing date '{date_str}': {e}")
        return datetime.date.min, 'Unknown Date'

def parse_post(filename, content):
    all_lines = content.split('\n')
    
    metadata = {}
    content_lines = []
    in_header = True
    
    for line in all_lines:
        if in_header:
            if line.strip() == "":
                in_header = False
            elif ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip().lower()] = value.strip()
        else:
            content_lines.append(line)
            
    title = metadata.get('title', 'Untitled Post')
    date_str = metadata.get('date', None)
    
    sortable_date, display_date = parse_date_info(date_str)
    
    slug = filename.replace('.md', '')
    
    content_to_render = '\n'.join(content_lines)
    html_content = markdown.markdown(content_to_render)
    clean_text = re.sub('<[^<]+?>', '', html_content)
    preview = clean_text[:150] + '...' if len(clean_text) > 150 else clean_text

    return {
        'title': title,
        'filename': filename,
        'slug': slug,
        'date': display_date,
        'sort_date': sortable_date,
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
                if content.strip() != "404: Not Found":
                    post_data = parse_post(file['name'], content)
                    posts.append(post_data)
            except Exception as e:
                print(f"Error fetching {file['name']}: {e}")

    posts.sort(key=lambda x: x['sort_date'], reverse=True)
    return posts

def render_post(filename):
    raw_url = f"{RAW_BASE_URL}/{filename}"
    try:
        res = requests.get(raw_url)
        res.raise_for_status() 
        content = res.text
        return parse_post(filename, content)
    except requests.exceptions.HTTPError as e:
        print(f"Post not found {filename}: {e}")
        return None
    except Exception as e:
        print(f"Error fetching post {filename}: {e}")
        return None

@app.route('/')
def index():
    posts = get_posts()
    return render_template('index.html', posts=posts)

@app.route('/post/<slug>')
def post(slug):
    filename = slug + '.md' 
    post_data = render_post(filename)
    
    if post_data is None:
        return "Post not found", 404
        
    return render_template('post.html', post=post_data)

if __name__ == '__main__':
    serve(app)