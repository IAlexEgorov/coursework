FROM python:3.9

WORKDIR /srv

COPY requirements.txt requirements.txt
COPY db_install.py db_install.py
COPY app.py app.py

COPY ./static ./static 
COPY ./templates ./templates


RUN pip install -r requirements.txt
RUN python3 db_install.py

RUN ls -la
EXPOSE 5000

CMD [ "python", "./app.py" ]