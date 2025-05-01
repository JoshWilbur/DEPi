FROM python:3.10-alpine
RUN pip install flask redis
COPY . .
CMD ["python", "stats.py"]