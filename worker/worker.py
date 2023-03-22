import os
from celery import Celery
import requests
import time

broker_url  = os.environ.get("CELERY_BROKER_URL"),
res_backend = os.environ.get("CELERY_RESULT_BACKEND")

celery_app = Celery(name = 'job_tasks',
                    broker = broker_url,
                    result_backend = res_backend)

@celery_app.task
def countWordsTask(text):
    word_count = len(text.split())
    time.sleep(word_count)
    return word_count