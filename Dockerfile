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

# Installing pytorch !
RUN pip install torch==1.6.0+cpu torchvision==0.7.0+cpu \
    -f https://download.pytorch.org/whl/torch_stable.html

# Copy all the files from the project’s root to the working directory
COPY *.py ./
COPY stellio-dev-access.token ./
WORKDIR /mlaas/pytorch-models-wheat
COPY ./pytorch-models-wheat ./

WORKDIR /mlaas

EXPOSE 5000

# Running Python Application
ENTRYPOINT ["python3", "/mlaas/app.py"]
