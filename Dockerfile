FROM python:3.12.0-alpine3.18
COPY ./app /app
WORKDIR /app
#RUN pip3 install --use-pep517 -r /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]