# syntax=docker/dockerfile:1

FROM python:3.14-slim
RUN useradd --create-home --shell /bin/bash app_user
WORKDIR /home/app_user
ENV PYTHONUNBUFFERED=1
USER app_user
COPY . .
CMD ["python", "-m", "send", "--config", "data/config.json", "--schedule"]
