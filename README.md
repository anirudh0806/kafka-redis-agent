# kafka-redis-agent
# Message Processing in Kafka

This is a Python code that processes image URLs from a Kafka topic, downloads the images, resizes them, and stores the result in a Redis database.

## Prerequisites

Before running the script, ensure the installation and functioning of the following components:
1.  Python 3
2. `requests` library for making HTTP requests.
3. `shutil` library for file operations.
4. `kafka-python` library for Kafka integration.
5. `PIL` (Pillow) library for image processing.
6.  Redis server and Kafka server are running.

    You can install the required Python libraries using pip:

    ```bash
    pip install requests kafka-python Pillow redis
    ```

## Execution

1. Start a Kafka producer to send messages with image URLs and output size information to the 'secondtask' Kafka topic.
2. Run the script using Python:

    ```bash
    python code.py
    ```

3. The script will consume messages from the 'secondtask' Kafka topic, download the images, resize them according to the specified dimensions, and store the results in Redis with keys like 'image0', 'image1', and so on.

