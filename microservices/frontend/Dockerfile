FROM python:3.12-alpine
RUN adduser -D -u 10001 appuser
COPY app.py /app.py
USER 10001
EXPOSE 5000
CMD ["python3", "/app.py"]
