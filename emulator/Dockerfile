FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY krzysiu_pb2.py emulator.py db.py ./
CMD ["python", "emulator.py"]