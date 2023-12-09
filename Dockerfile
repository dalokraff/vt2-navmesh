FROM python:3.12.1-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV PORT=2503
EXPOSE $PORT
# for development, remove reload for prod
CMD uvicorn main:app --reload --host 0.0.0.0 --port $PORT