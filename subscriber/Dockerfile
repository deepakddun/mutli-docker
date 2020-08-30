# Specify the base image

FROM python:alpine

# specify the working directory

#WORKDIR /usr/app

# copy the requiremnts file

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

RUN python ./subscriber.py &

CMD ["python","./subscriber2.py"]

