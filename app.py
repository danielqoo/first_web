from flask import Flask, render_template, url_for, redirect, request, session, send_from_directory
from flask_caching import Cache
import sqlite3 as sql
from datetime import datetime
import os

# 기본 설정
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
app.config.from_mapping(config)

# 파비콘 Windows8 and 10
@app.route("/browserconfig.xml")
def browserconfig() :
    return send_from_directory(os.path.join(app.root_path, 'static'), 'browserconfig.xml')

@app.route("/mstile-150x150.png")
def mstile() :
    return send_from_directory(os.path.join(app.root_path, 'static'), 'mstile-150x150.png')

# Android Chrome
@app.route("/android-chrome-192x192.png")
def android192() :
    return send_from_directory(os.path.join(app.root_path, 'static'), 'android-chrome-192x192.png')

# Android Chrome
@app.route("/android-chrome-512x512.png")
def android512() :
    return send_from_directory(os.path.join(app.root_path, 'static'), 'android-chrome-512x512.png')



# 카탈로그
@app.route("/educenter/intro")
def education_center() : 
    return render_template('catalog.html')

#문의폼
@app.route("/form_page", methods = ['POST', 'GET'])
def form_page() : 
    return render_template('form_page.html')

@app.route("/form_page_e", methods = ['POST', 'GET'])
def form_page_e() : 
    return render_template('form_page_e.html')


# 원페이지 Ver 0.0.1
@app.route("/")
@app.route("/home")
def home() : 
    return render_template('onepage.html')

@app.route("/service_center")
def service_center() : 
    return render_template('service_center.html')



# 영문 홈페이지
@app.route("/eng")
def eng() : 
    return render_template('onepage_eng.html')

@app.route("/contact")
def contact() : 
    return render_template('contact.html')


#게시판
@app.route('/educenter/homework', methods = ['POST', 'GET'])
def noticeboard() :
    if 'nickname' in session :
        conn = sql.connect('homework.db')
        c = conn.cursor()
        c.execute('select * from noticeboard')
        rows = c.fetchall()
        rows.reverse()
        return render_template('homework_board.html', nickname = session['nickname'], rows = rows)
    
#게시판작성페이지
@app.route('/educenter/writepage')
def writepage() :
    if 'nickname' in session :
        return render_template('게시글작성.html', nickname = session['nickname'])
    
#게시판작성내용데이터베이스로 옮기기
@app.route('/educenter/write', methods = ['POST', 'GET'])
def write() :
    if request.method == 'POST' and 'nickname' in session:
        title = request.form['title']
        content = request.form['content']
        nickname = session['nickname']
        if len(title) == 0 :
            return render_template('제목오류.html')
        if len(content) == 0 :
            return render_template('내용오류.html')
        conn = sql.connect('게시판.db')
        c = conn.cursor()
        c.execute(f'insert into noticeboard(title, content, nickname, datetime) values ("{title}", "{content}", "{nickname}", datetime("now"))')
        conn.commit()
        conn.close()
        return redirect(url_for('noticeboard', nickname = session['nickname']))

#게시판내용보기
@app.route('/educenter/noticeinformation', methods=['POST', 'GET'])
def noticeinformation() :
    if request.method == 'POST' and 'nickname' in session:
        title = request.form['title']
        conn = sql.connect('homework.db')
        c = conn.cursor()
        c.execute('select * from noticeboard')
        rows = c.fetchall()
        for row in rows :
            if title == row[0].replace(' ', '') + row[3].replace(' ', '') :
                title = row[0]
                content = row[1]
                writer = row[2]
                time = row[3]
                return render_template('게시판상세정보.html', title = title, content = content \
                    ,writer = writer, time = time, nickname = session['nickname'])

#게시판내용검색
@app.route('/educenter/searchnotice', methods = ['POST', 'GET'])
def searchnotice() :
    if 'nickname' in session and request.method == 'POST' :
        title = request.form['title']
        conn = sql.connect('homework.db')
        c = conn.cursor()
        c.execute(f'select * from noticeboard where title like "%{title}%"')
        rows = c.fetchall()
        rows.reverse()
        return render_template('게시판.html', nickname = session['nickname'], rows = rows)



if __name__ == "__main__":              
    app.run(host="0.0.0.0", port="80")
    #app.run(host="127.0.0.1", port="3000")