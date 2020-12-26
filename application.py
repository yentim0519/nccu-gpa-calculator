import flask
from flask import request, jsonify, session, redirect, url_for, flash
from flask_session import Session
import os
from bs4 import BeautifulSoup
import time
from rq import Queue
from rq.job import Job
from rq.registry import StartedJobRegistry
from worker import conn
import json 
from werkzeug.utils import secure_filename


application = flask.Flask(__name__)
q = Queue(connection=conn)

# 一定要加這行，幫session簽名 
application.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


UPLOAD_FOLDER = '/tmp' #folder route of uploading file
ALLOWED_EXTENSIONS = set(['html', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']) # limitation of upload file format
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB


@application.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
            
        file = request.files.get('file', None) # 這邊一直get不到file
        
        if file and allowed_file(file.filename):
            print(2)
            filename = secure_filename(file.filename)
            if file.filename == '':
                flash('No selected file')

            file_path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            print(4)
            file.save(file_path)
            print(5)

        task = q.enqueue(generate_data_thread, file_path)
        task_id = task.get_id()
        return flask.render_template('loading_page.html', task_id=task_id)
    else:
        return flask.render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS





# get data
def generate_data_thread(html_file_path):
    
    with open(html_file_path, encoding="utf-8") as f:
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
    
    return json.dumps(data) # 這邊要轉成json檔，result才能decode回來

    

    

@application.route('/thread_status/', methods=["POST"])
def thread_status():
    if request.method == 'POST':
        task_id = flask.request.form['task_id']
        print(task_id)
        task = Job.fetch(task_id, connection=conn)
        print(task.get_status())
        print(task.is_finished)
        registry = StartedJobRegistry('default', connection=conn)
        running_job_ids = registry.get_job_ids() 
        print(running_job_ids)

        if(task.get_status() == "failed"):
            return flask.render_template('error_page.html')
        
        if task.is_finished:
            return "true"
        else:
            return "false"
    
        
    



@application.route('/result', methods=["POST", "GET"]) 
def result():  
    task_id = flask.request.form['task_id']
    print("result", task_id)
    task = Job.fetch(task_id, connection=conn)
    # print(task.result)
    result_list = json.loads(task.result) 
    # print(result_list)

    return flask.render_template('page1.html', data_all = result_list)
    

            


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
