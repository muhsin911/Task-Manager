FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install debugpy

COPY . .

CMD [ "python", "-Xfrozen_modules=off", "-m", "debugpy", "--listen", "0.0.0.0:5678", "manage.py", "runserver", "0.0.0.0:8000" ]