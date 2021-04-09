FROM python:3.7-slim
LABEL maintainer="EGM"

# update / upgrade
RUN apt-get update -y && \
    apt-get upgrade -y

# set the working directory for containers
WORKDIR  /mlaas/

# Installing python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ctes.py .
COPY bentoml_proxy.py .

EXPOSE 5000

# Running Python Application
ENTRYPOINT ["python3", "/mlaas/bentoml_proxy.py"]
