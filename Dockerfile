FROM python:3.9

WORKDIR /srv

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . . 

RUN ls -la
EXPOSE 5000

CMD [ "python", "./app.py" ]