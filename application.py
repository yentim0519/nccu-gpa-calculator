import flask
from flask import request, jsonify, session, redirect, url_for, flash
import os
from bs4 import BeautifulSoup
import time
import json 
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge


application = flask.Flask(__name__)

# 一定要加這行，幫session簽名 
application.secret_key = b'_5#y2L"F4Q8z\n\xec]/' #最好遮掉


UPLOAD_FOLDER = '/tmp' #folder route of uploading file
ALLOWED_EXTENSIONS = set(['html', 'htm']) # limitation of upload file format
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB


@application.route('/', methods=["GET", "POST"])
def index(): 
    try:
        if request.method == 'POST':
            
                file = request.files.get('file', None) 

                if file.filename == '':
                    flash("No file upload!")
                    return redirect(request.url)

                if file and allowed_file(file.filename): # allowed_file會根據allow extension限制
                    filename = secure_filename(file.filename) # never trust user input
                    if file.filename == '':
                        flash('No selected file')
                    file_path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                else:
                    flash("Wrong Format! The format has to be HTML or HTM.")
                    return redirect(request.url) 


                with open(file_path, encoding="utf-8") as f:
                    data0 = f.read()
                    soup = BeautifulSoup(data0, 'html.parser')

                # 將data存到一個list中
                data = [] 
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
    except RequestEntityTooLarge:
        flash("The file is too large! The limit is 1MB.")
        return redirect(request.url) 
        




def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



if __name__ == '__main__':
    # application.debug=True
    application.run(host='0.0.0.0',threaded=True)


# Must:
# tutorial




# Nice to have:
# handle 一個學期全選
# 紀錄使用人次
# 等文字load完再呈現頁面

