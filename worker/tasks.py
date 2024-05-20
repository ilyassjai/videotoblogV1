from celery import Celery
from celery.utils.log import get_task_logger

import subprocess
import time
import json
from pathlib import Path

logger = get_task_logger(__name__)

app = Celery('tasks', broker='redis://redis:6379/0',
             backend='redis://redis:6379/0')


def read_file_content(file_path):
    path = Path(file_path)
    if path.is_file():
        with path.open('r') as file:
            content = file.read()
        return content
    else:
        return f"The file '{file_path}' does not exist."

@app.task()
def longtime_add(x, y):
    logger.info('Got Request - Starting work ')
    time.sleep(10)
    logger.info('Work Finished ')
    return x * y

@app.task()
def youtube_link_process(youtube_link):
    logger.info('Got Request - Starting video process ')
    result = subprocess.run(['python3', 'core_app/src/api_entry.py',
                   youtube_link], capture_output=True)
    if result.returncode != 0:
        logger.error('Subprocess failed')
        return {'error': 'Subprocess failed'}
    
    file_content = read_file_content('merged_output.md')
    
    # Parse the JSON output
    output = json.loads(result.stdout)
    logger.info('Work Finished ')

    if file_content:
        return output
    else:
        return "Error reading the output file."

