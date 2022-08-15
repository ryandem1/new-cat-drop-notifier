FROM python:3.10
WORKDIR /app
COPY ./new-cat-drop-notifier .
CMD ["python", "main.py"]
