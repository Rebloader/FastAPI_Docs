FROM python:3.11

WORKDIR .

RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-rus

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x scripts/*.sh

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]