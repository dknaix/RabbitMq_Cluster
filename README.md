
# RabbitMQ LAB

Lab for learning working of Message Broker RabbitMQ


# Folder Structure
Since there are not much files in this project no folder used 


# Description
For demonstration we will use 
1. 3-Node Rabbit Cluster (docker containers) on same physical host.

2. A Nginx Container which will load balance the requests to all 3 nodes

3. Python Code to pub/sub rabbit queue by connection to only 1 node of a cluster

# Purpose

We will test that in a cluster environment will are achieve High Availability with and without the Nginx Balancer.

# Conclusion

1. If Node1 is Down the Cluster is unreachable as in code Node1 is hardcoded as single connection point.

2. If Node2 or Node3 is Down or both are down Cluster is still reachable and running smoothly.

3. After Adding the TCP Load Balancer, if any 2 Nodes are down Network is still reachable, so using load balancer is recommended as chances of load balancer instance going down is far less

4. To overcome the shortcomings of Load balancer Failing, we can use multiple loadbalancer setup in case of very high throughput and large setup. 

