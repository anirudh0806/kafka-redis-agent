import argparse
import requests
import shutil
from kafka import KafkaConsumer
import json
import redis
from PIL import Image
from pathlib import Path


class ImageProcessor:

    def __init__(self, kafka_topic, redis_host, redis_port):
        self.kafka_topic = kafka_topic
        self.kafka_bootstrap_servers = 'localhost:9092'
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = 0

    def process_image_message(self, message, counter):
        """
        Processes a Kafka message containing image information, downloads the image,
        resizes it, and stores it in Redis.
        """

        # Extracts relevant information from the message
        url = message[6]["image_url"]
        file_name = "newfile.jpg"
        dimension = message[6]["output_size"]
        new_file_loc = f"{Path.cwd()}/newfile-resized.jpeg"

        # Downloads the image
        res = requests.get(url, stream=True)

        if res.status_code == 200:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image successfully downloaded:', file_name)
        else:
            print("Image couldn't be retrieved")
            
        # Resizing the image
        image = Image.open('newfile.jpg')
        print(f"Original size: {image.size}")
        width, height = map(int, dimension.split("x"))
        image_resized = image.resize((width, height))
        image_resized.save("newfile-resized.jpeg")
        print(f"New size: {dimension}")

        content = message[6]
        z = content
        y = {"output_image_path": new_file_loc}
        z.update(y)
        print(json.dumps(z))

        # Stores it in Redis
        r = redis.Redis(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        key_val = f"image{counter}"
        counter += 1

        r.set(key_val, json.dumps(z))

        return new_file_loc

    def run_consumer(self):
        # Creates a KafkaConsumer for the given parameters
        consumer = KafkaConsumer(
            self.kafka_topic,
            bootstrap_servers=[self.kafka_bootstrap_servers],
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        counter = 0

        for message in consumer:
            self.process_image_message(message, counter)
            counter += 1

def main(args):
    image_processor = ImageProcessor(
        kafka_topic=args.kafka_topic,
        redis_host=args.redis_host,
        redis_port=args.redis_port
    )
    image_processor.run_consumer()

if __name__ == "__main__":
    # Command Line Arguments
    parser = argparse.ArgumentParser(description="Kafka Image Processor")
    parser.add_argument('--kafka-topic', default='secondtask', help='Kafka topic name')
    parser.add_argument('--redis-host', default='localhost', help='Redis host')
    parser.add_argument('--redis-port', type=int, default=6379, help='Redis port')

    args = parser.parse_args()
    main(args)
