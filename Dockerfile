FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /data/

RUN pip install --upgrade pip
COPY requirements.txt /data/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /data/

EXPOSE 8000
CMD ["python", "main.py"]