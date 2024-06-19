import pika
import threading as t
# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5000, '/', pika.PlainCredentials('user', 'password')))
channel = connection.channel()

# Declare the queue again in case it doesn't exist (idempotent)
channel.queue_declare(queue='hello')

# Define a callback function to handle incoming messages
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

# Tell RabbitMQ to call the callback function whenever a message is received
channel.basic_consume(queue='hello',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

# Start consuming messages
t.Thread(target=channel.start_consuming).start()
print("Main thred exiting")
