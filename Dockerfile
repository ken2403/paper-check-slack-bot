FROM python:3.10.10-slim-bullseye

COPY . /app
WORKDIR /app
RUN pip install -U pip && \
    pip install -r requirements.txt

ENTRYPOINT [ "python3", "main.py" ]
CMD [ "args_mi.json" ]
