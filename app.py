import sqlite3
from flask import Flask, request, redirect
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts")
    posts = c.fetchall()
    conn.close()
    html = """
    <html>
    <head>
        <title>Blog cá nhân</title>
        <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css'>
        <style>
            body { 
                background: url('https://media.giphy.com/media/Hh9sPYeSWhAUx6NDBM/giphy.gif?cid=ecf05e471tvzchttvpgtwoup5r03dcxbku1rzirmwsvjc1vm&ep=v1_gifs_search&rid=giphy.gif&ct=g') no-repeat center center fixed; 
                background-size: cover; 
                font-family: Arial, sans-serif; 
            }
            .container { max-width: 800px; margin: 50px auto; }
            .post-title { margin-top: 20px; }
            .btn-custom { margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class='container'>
            <h1 class='text-center'>Blog cá nhân</h1>
            <a class='btn btn-primary btn-custom' href='/add'>Thêm bài viết</a>
            """
    for post in posts:
        html += f"""
        <h2 class='post-title'><a href='/post/{post[0]}'>{post[1]}</a></h2>
        """
    html += "</div></body></html>"
    return html

@app.route('/post/<int:post_id>')
def post(post_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = c.fetchone()
    conn.close()
    if post:
        return f"""
        <html>
        <head>
            <title>{post[1]}</title>
            <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css'>
            <style>
                body {{ 
                    background: url('https://media.giphy.com/media/Hh9sPYeSWhAUx6NDBM/giphy.gif?cid=ecf05e471tvzchttvpgtwoup5r03dcxbku1rzirmwsvjc1vm&ep=v1_gifs_search&rid=giphy.gif&ct=g') no-repeat center center fixed; 
                    background-size: cover; 
                    font-family: Arial, sans-serif; 
                }}
                .container {{ max-width: 800px; margin: 50px auto; }}
            </style>
        </head>
        <body>
            <div class='container'>
                <h1>{post[1]}</h1>
                <p>{post[2]}</p>
                <a class='btn btn-danger' href='/delete/{post[0]}'>Xóa bài viết</a>
                <a class='btn btn-secondary' href='/'>Quay lại</a>
            </div>
        </body>
        </html>
        """
    else:
        return "<html><body><h1>Không tìm thấy bài viết</h1><a href='/'>Quay lại</a></body></html>"
@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        return redirect('/') 
    return """
    <html>
    <head>
        <title>Thêm bài viết</title>
        <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css'>
        <style>
            body { 
                background: url('https://media.giphy.com/media/Hh9sPYeSWhAUx6NDBM/giphy.gif?cid=ecf05e471tvzchttvpgtwoup5r03dcxbku1rzirmwsvjc1vm&ep=v1_gifs_search&rid=giphy.gif&ct=g') no-repeat center center fixed; 
                background-size: cover; 
                font-family: Arial, sans-serif; 
            }
            .container { max-width: 600px; margin: 50px auto; }
        </style>
    </head>
    <body>
        <div class='container'>
            <h1>Thêm bài viết mới</h1>
            <form method='POST'>
                <input class='form-control' type='text' name='title' placeholder='Tiêu đề' required><br>
                <textarea class='form-control' name='content' placeholder='Nội dung' required></textarea><br>
                <button class='btn btn-success' type='submit'>Đăng bài</button>
            </form>
            <a class='btn btn-secondary' href='/'>Quay lại</a>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    init_db()
    # Lấy port từ biến môi trường, mặc định là 5000 nếu chạy local
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)