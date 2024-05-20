import pytesseract
from PIL import Image
from celery import Celery

from src.config import BASE_DIR


celery = Celery('tasks', broker="amqp://guest:guest@rabbitmq:5672")
celery.conf.broker_connection_retry_on_startup = True
celery.conf.result_backend = 'rpc://'


@celery.task
def task_analyze_document(filename) -> str:
    path = f'documents/{filename}'
    print(path)
    # path = f'{BASE_DIR}/documents/{filename}'
    img = Image.open(path)
    text = pytesseract.image_to_string(img, lang='rus', config='--oem 3 --psm 6')
    return text
