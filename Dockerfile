FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y python3-pip

RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir torch==2.3.0 --index-url https://download.pytorch.org/whl/cu121

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["python", "-m", "PurifyPixels.app", "--host=0.0.0.0"]
