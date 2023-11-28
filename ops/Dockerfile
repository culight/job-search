FROM python:3.11

RUN virtualenv venv

ENTRYPOINT bin/bash

RUN /bin/bash -c "source venv/bin/activate"

RUN pip install requirements.txt