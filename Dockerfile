FROM python:3.12.0-slim
COPY ./app /app
WORKDIR /app

#ARG POETRY_VERSION=1.7.0
RUN python3 -m pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Instalo Poetry
#RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local/poetry python3 - --version ${POETRY_VERSION}
#ENV POETRY_HOME="/usr/local/poetry/bin"
#ENV PATH="$PATH:$POETRY_HOME"

#CMD ["python3", "-m", "poetry", "--version"]
#CMD ["python3", "--version"]
#RUN #!/bin/sh \
    #if [ -f "./app/pyproject.toml" ]; then \ 
      #poetry install \ 
    #else \
      #echo "Poetry no se inicio en este proyecto" \
    #fi

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
