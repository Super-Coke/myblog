import sqlite3

conn = sqlite3.connect('blog.db')
cursor = conn.cursor()

# 创建 likes 表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        ip TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(post_id, ip)
    )
''')

conn.commit()
conn.close()

print('✅ likes 表创建成功！')