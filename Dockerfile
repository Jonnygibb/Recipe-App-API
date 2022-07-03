FROM python:3.10.5-alpine3.15
LABEL maintainer="Jonathan Gibbons"

# No buffering of commands to console. Recommneded when running python in container.
ENV PYTHONUNBUFFERED 1

# Copy requirements and app source from local machine to container.
COPY ./requirements.txt /tmp/requirements.txt
COPY /requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

# Set working directory to app. Commands will run from here.
WORKDIR /app
# Allow access to this port in the container from local machine.
EXPOSE 8000

# Default dev build to false.
ARG DEV=false
# Create virtual python env and install dependencies there.
# Add a new user 'django-user' to avoid running on root user.
# Combine commands into one run command to prevent excess image layers.
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Add python instance to path environment.
ENV PATH="/py/bin:$PATH"

# Switch to lower privilege user.
USER django-user
