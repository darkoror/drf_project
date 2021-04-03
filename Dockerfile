FROM python:3.8

WORKDIR /app

COPY . /app

RUN export PIPENV_DONT_USE_PYENV=1
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
