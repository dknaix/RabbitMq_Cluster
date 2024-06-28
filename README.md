
# RabbitMQ LAB

Lab for testing High Availability Cluster for Message Broker RabbitMQ



# Description
For demonstration we will use 
1. 3-Node Rabbit Cluster (docker containers) on same physical host.

2. A Nginx Container which will load balance the requests to all 3 nodes

3. Python Code to pub/sub rabbit queue by connection to only 1 node of a cluster

# Purpose

We will test that in a cluster environment will are achieve High Availability with and without the Nginx Balancer.



## Run Locally

Clone the project

```bash
  git clone https://github.com/dknaix/RabbitMq_Cluster.git
```

Create Venv

```bash
  python -m venv venv
```

Install dependencies

```bash
  pip install -r requirements.txt
```



## Deployment

Create Docker Network

```bash
docker network create rabbitmq-network
```

Run 3 Rabbit Conatiners
```bash
docker run -d --name rabbitmq-node1 --hostname rabbitmq-node1 --network rabbitmq-network -p 5672:5672 -p 15672:15672 -e RABBITMQ_ERLANG_COOKIE='secretcookie' -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3-management

docker run -d --name rabbitmq-node2 --hostname rabbitmq-node2 --network rabbitmq-network -p 5673:5672 -p 15673:15672 -e RABBITMQ_ERLANG_COOKIE='secretcookie' -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3-management

docker run -d --name rabbitmq-node3 --hostname rabbitmq-node3 --network rabbitmq-network -p 5674:5672 -p 15674:15672 -e RABBITMQ_ERLANG_COOKIE='secretcookie' -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3-management
```

RESTARTING SERVICES

```bash
docker exec -it rabbitmq-node1 rabbitmqctl stop_app
docker exec -it rabbitmq-node1 rabbitmqctl reset
docker exec -it rabbitmq-node1 rabbitmqctl start_app

docker exec -it rabbitmq-node2 rabbitmqctl stop_app
docker exec -it rabbitmq-node2 rabbitmqctl reset
docker exec -it rabbitmq-node2 rabbitmqctl start_app

docker exec -it rabbitmq-node3 rabbitmqctl stop_app
docker exec -it rabbitmq-node3 rabbitmqctl reset
docker exec -it rabbitmq-node3 rabbitmqctl start_app
```

JOINING THE CLUSTER
```bash
docker exec -it rabbitmq-node1 rabbitmqctl join_cluster rabbit@rabbitmq-node2
docker exec -it rabbitmq-node1 rabbitmqctl join_cluster rabbit@rabbitmq-node3

docker exec -it rabbitmq-node2 rabbitmqctl join_cluster rabbit@rabbitmq-node1
docker exec -it rabbitmq-node2 rabbitmqctl join_cluster rabbit@rabbitmq-node3

docker exec -it rabbitmq-node3 rabbitmqctl join_cluster rabbit@rabbitmq-node1
docker exec -it rabbitmq-node3 rabbitmqctl join_cluster rabbit@rabbitmq-node2
```

Start Subscriber code

```bash
python recv.py
```

Start Producer code

```bash
python prod.py
```
## Conclusion

If Node1 is Down the Cluster is unreachable as in code Node1 is hardcoded as single connection point.

If Node2 or Node3 is Down or both are down Cluster is still reachable and running smoothly.

After Adding the TCP Load Balancer, if any 2 Nodes are down Network is still reachable, so using load balancer is recommended as chances of load balancer instance going down is far less

#### To overcome the shortcomings of Load balancer Failing, we can use multiple loadbalancer setup in case of very high throughput and large setup. 
