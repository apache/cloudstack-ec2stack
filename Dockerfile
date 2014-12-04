FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN apt-get clean all

RUN pip install ec2stack
RUN pip install --upgrade requests

EXPOSE 5000

CMD ["ec2stack"]
