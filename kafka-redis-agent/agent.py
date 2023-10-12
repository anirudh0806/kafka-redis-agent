import argparse
import requests
import shutil
from kafka import KafkaConsumer
import json
import redis
from PIL import Image

class Agent:
    def __init__(self, kafka_topic, processing_function):
        # Initializes the agent with the Kafka topic and processing function
        self.kafka_topic = kafka_topic
        self.consumer = KafkaConsumer(
            self.kafka_topic,
            bootstrap_servers=['localhost:9092'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        self.counter = 0
        self.processing_function = processing_function

    def run(self):
        # Runs the Kafka message processing loop
        for message in self.consumer:
            processed_data = self.processing_function(message)
            if processed_data is not None:
                r = redis.Redis(host='localhost', port=6379, db=0)
                key_val = f"image{self.counter}"
                self.counter += 1
                r.set(key_val, json.dumps(processed_data))


if __name__ == "__main__":
    # Command Line Arguments for Input
    parser = argparse.ArgumentParser(description="Kafka Image Processing Agent")
    parser.add_argument('--kafka-topic', default='secondtask', help='Kafka topic name')
    args = parser.parse_args()

    # Message processing function
    def processing_function(message):
        # Process a Kafka message containing image information
        url = message[6]["image_url"]
        file_name = "newfile.jpg"
        dimension = message[6]["output_size"]
        width, height = map(int, dimension.split("x"))

        res = requests.get(url, stream=True)
        if res.status_code == 200:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image successfully Downloaded:', file_name)
        else:
            print('Image Couldn\'t be retrieved')
            return None

        image = Image.open('newfile.jpg')
        image_resized = image.resize((width, height))
        image_resized.save('newfile-resized.jpeg')
        print(f"Original size: {image.size}")
        print(f"New size: {dimension}")

        content = message[6]
        new_file_loc = "test/newfile-resized.jpeg"
        z = content
        y = {"output_image_path": new_file_loc}
        z.update(y)

        return z

    # Initializes the agent with the Kafka topic and processing function
    agent = Agent(kafka_topic=args.kafka_topic, processing_function=processing_function)

    # Starts processing messages from the Kafka topic
    agent.run()
