from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__, static_folder='../frontend', static_url_path='/static')
CORS(app, resources={r"/api/*": {"origins": ["https://super-coke.github.io", "*"]}})

def get_db_connection():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

# ===== 首页路由：返回前端 index.html =====
@app.route('/')
def index():
    with open('../frontend/index.html', 'r', encoding='utf-8') as f:
        return f.read()

# ===== 静态文件路由：让 Flask 能提供 frontend 文件夹里的图片 =====
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('../frontend', filename)

# ===== API 1：获取所有文章列表 =====
@app.route('/api/posts', methods=['GET'])
def get_posts():
    conn = get_db_connection()
    posts_db = conn.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    conn.close()

    posts = []
    for row in posts_db:
        posts.append({
            'id': row['id'],
            'title': row['title'],
            'date': row['date'],
            'tags': row['tags'].split(',') if row['tags'] else [],
            'summary': row['summary']
        })
    return jsonify(posts)

# ===== API 2：文章详情页 =====
@app.route('/post/<int:post_id>')
def get_post_detail(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    if post is None:
        return '<h1>404 - 文章未找到</h1><p><a href="/">返回首页</a></p>', 404

    # 安全处理 content
    if post['content'] is not None:
        content_html = post['content'].replace('\n', '<br>')
    else:
        content_html = '（暂无正文内容）'

    # 安全处理 tags
    tags_list = post['tags'].split(',') if post['tags'] else []
    tags_html = ''.join([f'<span class="tag"># {tag.strip()}</span>' for tag in tags_list if tag.strip()])

    html = f'''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{post['title']} · 我的博客</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                max-width: 800px;
                margin: 60px auto;
                padding: 0 20px;
                line-height: 1.8;
                background-image: url('/static/detail-bg.png');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                color: #1a1a2e;
            }}
            .post-card {{
                background: rgba(255,255,255,0.25);
                backdrop-filter: blur(6px);
                -webkit-backdrop-filter: blur(6px);
                border-radius: 20px;
                padding: 40px 48px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.08);
                border: 1px solid rgba(255,255,255,0.2);
                position: relative;
            }}
            .back-icon {{
                position: absolute;
                top: 20px;
                left: 24px;
                font-size: 24px;
                color: #1a1a2e;
                text-decoration: none;
                transition: transform 0.2s;
                z-index: 10;
            }}
            .back-icon:hover {{
                transform: scale(1.1);
                color: #4a6cf7;
            }}
            h1 {{
                font-size: 32px;
                line-height: 1.3;
                margin-bottom: 10px;
                margin-top: 10px;
                padding-left: 30px;
            }}
            .meta {{
                color: #666;
                font-size: 14px;
                margin-bottom: 30px;
                display: flex;
                gap: 12px;
                align-items: center;
                flex-wrap: wrap;
                padding-left: 30px;
            }}
            .tag {{
                background: rgba(74,108,247,0.12);
                color: #4a6cf7;
                padding: 2px 12px;
                border-radius: 20px;
                font-size: 12px;
            }}
            .content {{
                font-size: 17px;
                color: #f0f0f0;
                padding-left: 30px;
            }}
            .content p {{
                margin-bottom: 20px;
            }}
            .like-area {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid rgba(255,255,255,0.2);
                display: flex;
                align-items: center;
                gap: 12px;
                padding-left: 30px;
            }}
            .like-area .like-text {{
                font-size: 15px;
                color: #ddd;
            }}
            .like-area .like-btn {{
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 24px;
                cursor: pointer;
            }}
            .like-area .like-btn i {{
                color: #f0f0f0;
                transition: transform 0.2s;
            }}
            .like-area .like-btn i:hover {{
                transform: scale(1.2);
            }}
            .like-area .like-count {{
                font-size: 16px;
                color: #ddd;
                font-weight: 500;
            }}
            .footer {{
                margin-top: 40px;
                text-align: center;
                font-size: 14px;
                color: #888;
                padding: 16px 0;
                border-top: 1px solid rgba(0, 0, 0, 0.06);
            }}
            .footer a {{
                color: #4a6cf7;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="post-card">
            <a class="back-icon" href="https://super-coke.github.io/myblog/" title="返回首页">
                <i class="fas fa-arrow-left"></i>
            </a>

            <h1>{post['title']}</h1>
            <div class="meta">
                <span><i class="far fa-clock" style="margin-right:4px;"></i> {post['date']}</span>
                {tags_html}
            </div>
            <div class="content">
                {content_html}
                <p>—— 本篇完 ——</p>
            </div>
            <div class="like-area">
                <span class="like-text">觉得不错？点个赞吧</span>
                <div class="like-btn" onclick="toggleLike({post_id})">
                    <i class="far fa-heart" id="detail-like-icon-{post_id}"></i>
                    <span class="like-count" id="detail-like-count-{post_id}">0</span>
                </div>
            </div>
        </div>
        <div class="footer">
            © 2026 · 使用 GitHub Pages 搭建 ·
            <a href="https://github.com/Super-Coke" target="_blank">Super-Coke 的主页</a>
        </div>

        <script>
            function loadDetailLikes(postId) {{
                fetch('/api/posts/' + postId + '/likes')
                    .then(response => response.json())
                    .then(data => {{
                        const countEl = document.getElementById('detail-like-count-' + postId);
                        if (countEl) {{
                            countEl.textContent = data.likes;
                        }}
                    }})
                    .catch(error => console.error('获取点赞数失败:', error));

                fetch('/api/posts/' + postId + '/like-status')
                    .then(response => response.json())
                    .then(data => {{
                        const icon = document.getElementById('detail-like-icon-' + postId);
                        if (icon) {{
                            if (data.liked) {{
                                icon.className = 'fas fa-heart';
                            }} else {{
                                icon.className = 'far fa-heart';
                            }}
                        }}
                    }})
                    .catch(error => console.error('获取点赞状态失败:', error));
            }}

            function toggleLike(postId) {{
                const icon = document.getElementById('detail-like-icon-' + postId);
                const countEl = document.getElementById('detail-like-count-' + postId);
                const isLiked = icon.classList.contains('fas');

                if (isLiked) {{
                    icon.className = 'far fa-heart';
                    countEl.textContent = parseInt(countEl.textContent) - 1;
                }} else {{
                    icon.className = 'fas fa-heart';
                    countEl.textContent = parseInt(countEl.textContent) + 1;
                }}

                fetch('/api/posts/' + postId + '/like', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }}
                }})
                .then(response => response.json())
                .then(data => {{
                    const currentIsLiked = icon.classList.contains('fas');
                    if (data.liked !== currentIsLiked) {{
                        if (data.liked) {{
                            icon.className = 'fas fa-heart';
                            countEl.textContent = parseInt(countEl.textContent) + 1;
                        }} else {{
                            icon.className = 'far fa-heart';
                            countEl.textContent = parseInt(countEl.textContent) - 1;
                        }}
                    }}
                    fetch('/api/posts/' + postId + '/likes')
                        .then(response => response.json())
                        .then(data => {{
                            countEl.textContent = data.likes;
                        }})
                        .catch(error => console.error('获取点赞数失败:', error));
                }})
                .catch(error => {{
                    console.error('点赞操作失败:', error);
                    if (isLiked) {{
                        icon.className = 'fas fa-heart';
                        countEl.textContent = parseInt(countEl.textContent) + 1;
                    }} else {{
                        icon.className = 'far fa-heart';
                        countEl.textContent = parseInt(countEl.textContent) - 1;
                    }}
                }});
            }}

            document.addEventListener('DOMContentLoaded', function() {{
                loadDetailLikes({post_id});
            }});
        </script>
    </body>
    </html>
    '''
    return html

# ============================================================
# ===== 点赞功能 =====
# ============================================================

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

@app.route('/api/posts/<int:post_id>/likes', methods=['GET'])
def get_post_likes(post_id):
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) FROM likes WHERE post_id = ?', (post_id,)).fetchone()[0]
    conn.close()
    return jsonify({'post_id': post_id, 'likes': count})

@app.route('/api/posts/<int:post_id>/like-status', methods=['GET'])
def get_like_status(post_id):
    ip = get_client_ip()
    conn = get_db_connection()
    exists = conn.execute('SELECT 1 FROM likes WHERE post_id = ? AND ip = ?', (post_id, ip)).fetchone()
    conn.close()
    return jsonify({'liked': exists is not None})

@app.route('/api/posts/<int:post_id>/like', methods=['POST'])
def toggle_like(post_id):
    ip = get_client_ip()
    conn = get_db_connection()
    
    existing = conn.execute('SELECT 1 FROM likes WHERE post_id = ? AND ip = ?', (post_id, ip)).fetchone()
    
    if existing:
        conn.execute('DELETE FROM likes WHERE post_id = ? AND ip = ?', (post_id, ip))
        conn.commit()
        conn.close()
        return jsonify({'liked': False, 'message': '已取消点赞'})
    else:
        conn.execute('INSERT INTO likes (post_id, ip) VALUES (?, ?)', (post_id, ip))
        conn.commit()
        conn.close()
        return jsonify({'liked': True, 'message': '点赞成功'})

# ============================================================
# ===== 管理员功能 =====
# ============================================================

ADMIN_PASSWORD = '@2006331'

@app.route('/api/admin/verify', methods=['POST'])
def verify_admin():
    data = request.get_json()
    password = data.get('password', '')
    if password == ADMIN_PASSWORD:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': '密码错误'}), 401

@app.route('/api/admin/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    password = data.get('password', '')
    
    if password != ADMIN_PASSWORD:
        return jsonify({'success': False, 'message': '密码错误'}), 401
    
    title = data.get('title', '').strip()
    date = data.get('date', '').strip()
    tags = data.get('tags', '').strip()
    summary = data.get('summary', '').strip()
    content = data.get('content', '').strip()
    
    if not title or not date:
        return jsonify({'success': False, 'message': '标题和日期不能为空'}), 400
    
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO posts (title, date, tags, summary, content) VALUES (?, ?, ?, ?, ?)',
        (title, date, tags, summary, content)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': '文章发布成功'})

@app.route('/api/admin/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    data = request.get_json()
    password = data.get('password', '')
    
    if password != ADMIN_PASSWORD:
        return jsonify({'success': False, 'message': '密码错误'}), 401
    
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    if post is None:
        conn.close()
        return jsonify({'success': False, 'message': '文章不存在'}), 404
    
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': '文章已删除'})

# ============================================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)