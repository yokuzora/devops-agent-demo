FROM ubuntu:latest123
WORKDIR /app

# The base image intentionally does not exist.
COPY requirements.txt ./
RUN apt-get update && apt-get install -y python3 python3-pip \
    && python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python3", "app.py"]
