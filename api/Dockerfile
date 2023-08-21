FROM python:3.11

WORKDIR /api
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

ADD . .

CMD ["python", "api.py"]