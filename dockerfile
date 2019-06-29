FROM python:3.6-slim
COPY . /root
WORKDIR /root
RUN pip install flask
RUN pip install gunicorn
RUN pip install numpy sklearn scipy pandas
RUN pip install joblib flask_wtf wtforms