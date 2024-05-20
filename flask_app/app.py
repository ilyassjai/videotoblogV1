from flask import Flask, jsonify, request
from celery import Celery
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
simple_app = Celery('worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.route('/')
def start():
    return "app is running"

@app.route('/process-youtube-link', methods=['POST'])
def process_youtube_link():
    data = request.get_json()
    youtube_link = data.get('youtubeLink')
    print(youtube_link)
    app.logger.info("Invoking Method ")
    #  queue name in task folder.function name
    r = simple_app.send_task('tasks.youtube_link_process', kwargs={'youtube_link': youtube_link})
    app.logger.info(r.backend)
    return jsonify({'taskId': r.id}) 

@app.route('/simple_start_task')
def call_method():
    app.logger.info("Invoking Method ")
    # queue name in task folder.function name
    r = simple_app.send_task('tasks.longtime_add', kwargs={'x': 1, 'y': 2})
    app.logger.info(r.backend)
    return r.id


@app.route('/simple_task_status/<task_id>')
def get_status(task_id):
    status = simple_app.AsyncResult(task_id, app=simple_app)
    print("Invoking Method ")
    return "Status of the Task " + str(status.state)


@app.route('/simple_task_result/<task_id>')
def task_result(task_id):

    result = simple_app.AsyncResult(task_id).result
    return jsonify({"result" : result})

@app.route('/all_tasks_status')
def all_tasks_status():
    all_info = []
    i = simple_app.control.inspect()
    all_info.append(i.registered())
    all_info.append(i.active())
    all_info.append(i.scheduled())
    all_info.append(i.reserved())

    return jsonify({"all_tasks": all_info})
