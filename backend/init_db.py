import sqlite3

# 连接到数据库（如果文件不存在，会自动创建）
conn = sqlite3.connect('blog.db')
cursor = conn.cursor()

# 创建文章表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        tags TEXT NOT NULL,
        summary TEXT NOT NULL
    )
''')

# 插入两篇文章（如果表为空的话）
cursor.execute('SELECT COUNT(*) FROM posts')
count = cursor.fetchone()[0]

if count == 0:
    cursor.execute('''
        INSERT INTO posts (title, date, tags, summary)
        VALUES (?, ?, ?, ?)
    ''', ('Hello World · 我的博客开张了', '2026-07-20', '生活,开始', '建站初衷 + 近期计划'))

    cursor.execute('''
        INSERT INTO posts (title, date, tags, summary)
        VALUES (?, ?, ?, ?)
    ''', ('Python 全栈初体验', '2026-07-21', '技术,Python', '第一次用 Flask 写后端 API'))

    print('✅ 已插入两篇文章')
else:
    print('ℹ️ 数据库中已有文章，跳过插入')

# 提交更改并关闭连接
conn.commit()
conn.close()

print('✅ 数据库初始化完成！')