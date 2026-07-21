import sqlite3

conn = sqlite3.connect('blog.db')
cursor = conn.cursor()

# 1. 添加 content 字段（如果不存在）
try:
    cursor.execute('ALTER TABLE posts ADD COLUMN content TEXT')
    print('✅ 已添加 content 字段')
except sqlite3.OperationalError:
    print('ℹ️ content 字段已存在，跳过')

# 2. 给 id=1 的文章填充正文
cursor.execute('''
    UPDATE posts SET content = ? WHERE id = 1
''', ('欢迎来到我的个人博客。这里是我记录思考、生活和学习的地方。今天，我正式把这个小站点亮了。\n\n我一直觉得，写东西是整理自己最好的一种方式。把自己学到的、想到的写下来，既能巩固记忆，也能和别人分享。这个博客就是一个安静的小角落，没有推送，没有算法，只有文字。\n\n"写作是思考的延伸，也是最好的自我对话方式。"\n\n接下来，我可能会写一些技术笔记、读书感想、或者生活里的小事。如果你偶然路过，欢迎你停下看看。\n\n近期计划：\n- 给博客换一套好看的模板\n- 写一篇关于 Git 入门的文章\n- 收集一些有意思的博客友链',))

# 3. 给 id=2 的文章填充正文
cursor.execute('''
    UPDATE posts SET content = ? WHERE id = 2
''', ('Python 是一门非常优雅的语言，而 Flask 是 Python 生态中最轻量、最灵活的 Web 框架之一。\n\n在这篇文章里，我记录了自己第一次用 Flask 写后端 API 的经历。从安装 Flask、创建虚拟环境，到写第一个路由、返回 JSON 数据，整个过程比我想象中要顺畅得多。\n\n通过这次实践，我理解了什么是 API、什么是路由、什么是 JSON，也明白了前后端分离是怎么一回事。\n\n下一步，我打算接入数据库，让文章数据持久化存储。',))

conn.commit()
conn.close()

print('✅ 文章正文内容已更新！')