FROM alpine:3.7

### 2. Get Java via the package manager
RUN apk update \
&& apk upgrade \
&& apk add --no-cache bash \
&& apk add --no-cache --virtual=build-dependencies unzip \
&& apk add --no-cache curl \
&& apk add --no-cache openjdk8-jre

### 3. Get Python, PIP

RUN apk add --no-cache python3 \
&& python3 -m ensurepip \
&& pip3 install --upgrade pip setuptools \
&& rm -r /usr/lib/python*/ensurepip && \
if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
rm -r /root/.cache

####
#### OPTIONAL : 4. SET JAVA_HOME environment variable, uncomment the line below if you need it

ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk"
ENV PYTHONPATH="/usr/bin/python3"
ENV PYSPARK_PYTHON="/usr/bin/python3"
ENV PYSPARK_DRIVER_PYTHON="/usr/bin/python3"



####

WORKDIR /consumerservice

ADD ./requirements.txt ./
RUN pip install -r requirements.txt
ADD ./ ./

COPY kafka_consumer.py /usr/bin/kafka_consumer.py
COPY etl_driver.py /usr/bin/etl_driver.py
CMD ["python3","-u","/usr/bin/kafka_consumer.py"]




