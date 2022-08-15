FROM python:3.10
WORKDIR /app
COPY ./new-cat-drop-notifier .
RUN ["pip", "install", "-r", "requirements.txt"]
CMD ["python", "main.py"]
