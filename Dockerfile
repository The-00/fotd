FROM dotriver/alpine-s6

RUN apk add python3 py3-pillow py3-pip

RUN pip install bottle Paste

ADD conf/ /
