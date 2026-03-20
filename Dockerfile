FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.docker.txt ./requirements.docker.txt
RUN pip install --upgrade pip && pip install -r requirements.docker.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "comparator.py", "--server.address=0.0.0.0", "--server.port=8501"]
