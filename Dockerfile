FROM python:3.7

# Create a group and user to run our app
ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# Copy in your requirements file
ADD requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /code/
WORKDIR /code/
ADD . /code/

EXPOSE 8000

# Change to a non-root user
USER ${APP_USER}:${APP_USER}

CMD ["python", "app.py"]
