FROM python:3.11

WORKDIR /api
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

ADD . .

EXPOSE 3001

CMD ["python", "api.py"]