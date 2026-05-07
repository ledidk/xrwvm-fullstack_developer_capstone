# Stage 1: Build React frontend
FROM node:18-slim AS frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Stage 2: Django backend
FROM python:3.12.0-slim-bookworm

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

ENV APP=/app

WORKDIR $APP

COPY requirements.txt $APP

RUN pip3 install -r requirements.txt

COPY . $APP

# Copy React build output from stage 1
COPY --from=frontend-build /frontend/build ./frontend/build

EXPOSE 8000

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
