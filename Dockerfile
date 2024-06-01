FROM python:3.10

WORKDIR /usr/src/app

EXPOSE 8000

COPY requirements.txt ./

COPY . .

RUN pip install -r requirements.txt

