# Data Engineering Test

We as a data engineering team want to gather data from various sources in our company, enrich the collected data and deliver it to our stakeholders.
One of our backend teams developed a new microservice for payment transactions and we would like to utilize the data for analysis.

The payment microservice publishes a new message into a kafka topic for every completed payment done through the mytaxi app.


## Tasks
For any of the following tasks please use git to track the status and progress of your development.

The task includes two predefined projects. `paymentservice` and `myservice`. These service create a jar that is used to run the service inside a docker container.
Make sure you recreate the Docker Image whenever you do a change in the code and do not used a cached version of the old code.

Docker Compose will help you build and start all the services that are part of this assignment. By running `docker-compose up --build` from the root folder of this project you can start kafka, zookeeper, the paymentservice and your new service. `docker ps` will show you the currently running docker containers.
In case you would like to terminate all containers, run `docker-compose down`

From within the docker containers all nodes are available by their name in the docker-compose file. (f.e. Kafka can be reached via `kafka:9092` from any docker container in the docker-compose).


### 1. Consume and Print
 As initial task we would like to consume the payment events from kafka and simply print them to the log. 
 
 We have provided a skeleton for your new spark project in the `myservice` folder. You can use this project to start writing your spark code.
 If you would prefer to finish the assignment in a different language, you are free to bootstrap a new project in the language of your favor.
 Just make sure to add the new project to the `docker-compose.yml`.


### 2. Running Aggregate on Tour Value
We would like to know how much value a driver is generating over his whole lifetime. On every batch iteration sum the tour_value coming from the payment service and calculate a cumulative sum.

Take your application from task 1. and extend it with a function to print the cumulative sum of tour values per driver to the log.

### 3. Time Based Aggregate
In order to evaluate the driver's more recent performance life time aggregates do not really help. We would like to understand how drivers perform more recently though.
Please aggregate in a 1 minute interval the performance of drivers based on their tour value and the number of tours they did. (each payment event == successful tour)

Now we need to take action based on this window. Whenever a driver crosses the threshold of 200 Euro per 1 minute window we would like to report him. For starters just print him to the log.

### 4. Produce Kafka Message
We need to inform another service about the drivers we identified in task 3. Please write a kafka producer, that sends an event for every driver identified in task 3. into a new topic.
