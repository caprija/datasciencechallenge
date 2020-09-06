Welcome to the datasciencechallenge [test1](https://github.com/caprija/datasciencechallenge/wiki/test1)!

## How to run this project:


To run the following tasks please follow below instructions:

This assignment includes two projects. `producerservice` and `consumerservice`. These services contains python scripts that are used to run the services inside a docker container.

Docker Compose will help build and start all the services that are part of this assignment. By running `docker-compose up --build` from the root folder of this project you can start kafka, zookeeper, the producerservice and consumerservice. 
`docker ps` will show you the currently running docker containers.
In case you would like to terminate all containers, run `docker-compose down`

From within the docker containers all nodes are available by their name in the docker-compose file. (f.e. Kafka can be reached via `kafka:9092` from any docker container in the docker-compose).

So just go to the root folder of this project and run following command:
docker-compose up --build

It will start zookeeper, kafka and producer and consumer services.
Meanwhile for this assignment I have print all desired results of tasks in the docker logs.

So just wait and after installation & on startup of these services you can see results.
Consumer service will pick user records after every 1 minute, process then and print them in console. Meanwhile in docker producer and consumer start at same time, consumer took some time to create spark context and create connection with kafka, so i can discuss its solution too in next step.

### 1. Write a simple producer app in Python that reads the data in the given file and writes it as messages to a kafka topic. Take into account that this file could be of several MB.

producerservice read data from file and write on kafka topic named "user"
For consideration of processing of several MBs file I have used ijson (Iterative JSON parser with a standard Python iterator interface) That means that instead of loading the whole file into memory and parsing everything at once, it uses iterators to lazily load the data. In that way, when we pass by a key that we don’t need, we can just ignore it and the generated object can be removed from memory.

you can find code related to this is in 'producerservice' folder.


### 2. Write a simple consumer app in PySpark streaming that reads the kafka stream and does the following:

consumerservice reads data from kafka topic named "user" and do following processing using pyspark.

- Cleans and conform user data using following rules
- Country fields always start with capital letter
- Date field has always the same format

Computes some measures of the data on the fly: 
- Most and least represented country, 
- Number of unique users in the current window

you can find code related to this is in 'consumerservice' folder.

### 3. Plus Task : Write a simple monitoring app/module to check (partly) if the system is working as expected. An example to do this could be: check if the number of messages processed by the consumer is equal to the number of messages pushed by the producer.

Although i didn't get enough time to do this task, but we can discuss solution in next stage if it is ok with you         

### 4. Containerization
I have package my all code by using docker file which is responsible to install all dependencies to run this project.
