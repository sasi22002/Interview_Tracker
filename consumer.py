import pika
from datetime import datetime

# Define the task to be performed when a message is received
def process_task(body):
    
    #NEED TO CUSTOMIZE THIS PART
    print(f"Received message: {body}")
    print("Message Received successfully.")

# Connect to RabbitMQ
def main():
    # Define the RabbitMQ connection parameters
    connection_params = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    # Declare the queue (create if it doesn't exist)
    channel.queue_declare(queue='task_queue')

    # Callback function when a message is received
    def callback(ch, method, properties, body):
        print("Message received, processing...")
        process_task(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge message

    # Set up subscription on the queue
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    print('Waiting for messages. To exit press CTRL+C')
    # Start consuming messages from RabbitMQ
    channel.start_consuming()

if __name__ == '__main__':
    main()
