FROM python:3.8

# USER root

RUN apt-get update && \
       apt-get install -y \
       libgl1-mesa-glx \
       libglib2.0-0 && \
       apt-get clean && \
       rm -rf /var/lib/apt/lists/*


# Install Tesseract OCR
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# layer caching for faster builds
COPY requirements.txt /
RUN pip install -r /requirements.txt

#COPY app.py /app.py
ADD . /worker
WORKDIR /worker

# # Copy the entire ML_app into the Docker image
# COPY ../ML_app /worker/ML_app

ENTRYPOINT celery -A tasks worker --loglevel=info
#-Q celery_worker
#ENTRYPOINT ['celery','-A','test_celery', 'worker', '--loglevel=info']