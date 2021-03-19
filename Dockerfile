FROM python:3.7-stretch
LABEL maintainer="didier.dumet@egm.io"

# update / upgrade
RUN apt-get update -y && \
    apt-get upgrade -y

# set the working directory for containers
WORKDIR  /mlaas/

# Installing python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the files from the project’s root to the working directory
COPY *.py ./
COPY stellio-dev-access.token ./

WORKDIR /mlaas

EXPOSE 5000

# Running Python Application
ENTRYPOINT ["python3", "/mlaas/app.py"]
