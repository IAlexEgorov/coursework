FROM python:3.8

WORKDIR /srv

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python3 db_install.py

COPY classes/ .classes/
COPY static/ .static/
COPY templates/ .templates/

COPY app.py .
COPY db_install.py .


CMD [ "python", "./app.py" ]