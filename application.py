import flask
from flask import request, jsonify, session, redirect, url_for, flash
from flask_session import Session
import os
from bs4 import BeautifulSoup
import time
import json 
from werkzeug.utils import secure_filename


application = flask.Flask(__name__)

# 一定要加這行，幫session簽名 
application.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


UPLOAD_FOLDER = '/tmp' #folder route of uploading file
ALLOWED_EXTENSIONS = set(['html', 'htm']) # limitation of upload file format
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB


@application.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        print("2222", request.files)
        file = request.files.get('file', None) # 這邊一直get不到file
        print("1111",file)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if file.filename == '':
                flash('No selected file')
            file_path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)


        with open(file_path, encoding="utf-8") as f:
            data0 = f.read()
            soup = BeautifulSoup(data0, 'html.parser')

        data = [] #要存進database
        all_table = soup.find_all("table")
        for table in all_table[5:]:
            
            table_data = []
            all_tr = table.find_all("tr")
            for tr in all_tr[2:]:
                
                tr_data = []
                all_td = tr.find_all("td")
                for td in all_td:
                    tr_data.append(td.string)

                table_data.append(tr_data)
            data.append(table_data)
        
        return flask.render_template('page1.html', data_all = data)
    else:
        return flask.render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
        
    

            


if __name__ == '__main__':
    # application.debug=True
    application.run(host='0.0.0.0',threaded=True)


# Must:
# handle result要按很多次才能跑出來
# 手機版的可以把不重要的資訊拿掉，讓table變小


# Nice to have:
# handle 一個學期全選
# handle 在generate時refresh
# 符合各平台版本 --> 在手機上要大一點
# 紀錄使用人次
# 中間弄個進度條，讓人知道等待時間
