FROM zauberzeug/nicegui:2.19.0

COPY requirement.txt /requirement.txt
RUN pip3 install -r /requirement.txt

COPY app /app
WORKDIR /app

