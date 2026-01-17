FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

# Guild config persistence (mount a volume here)
RUN mkdir -p /app/runtime

CMD ["python", "main.py"]
