FROM python:3.10-alpine
RUN pip install flask redis requests
COPY . .
CMD ["python", "resource_monitor.py"]