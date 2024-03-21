FROM python:3.10.13
ENV PYTHONUNBUFFERED True

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV APP_HOME /app
WORKDIR $APP_HOME
# RUN mkdir $APP_HOME/models
COPY /app $APP_HOME/app
# COPY /models $APP_HOME/models

EXPOSE 8080
# uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]