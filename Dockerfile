FROM zauberzeug/nicegui:latest

COPY requirement.txt /requirement.txt
RUN pip3 install -r /requirement.txt

COPY app /app
WORKDIR /app

