FROM python:3.10-slim

WORKDIR /code

COPY ./* ./
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python3", "main.py" ]