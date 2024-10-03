import pika
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='rabbitmq_sender.log',  # Log file
    level=logging.INFO,  # Log level (can be DEBUG, INFO, WARNING, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

def send_message(message):
    try:
        # Log the attempt to connect to RabbitMQ
        connection_params = pika.ConnectionParameters(host='localhost')
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()

        # Log queue declaration
        channel.queue_declare(queue='task_queue')

        # Log the message to be sent
        logging.info(f"Publishing message: '{message}'")
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )

        logging.info(f"Message sent successfully: '{message}'")
    except Exception as e:
        logging.error(f"Error sending message: {e}")
    finally:
        # Close the connection and log it
        if connection.is_open:
            connection.close()
            logging.info('Connection to RabbitMQ closed')

if __name__ == '__main__':
    # Send a message with a timestamp and log it
    message = f'Hello RabbitMQ! at - {datetime.now()}'
    logging.info(f'Starting message send: {message}')
    print(f'Starting message send: {message}')
    send_message(message)
    logging.info('Message send operation completed')
