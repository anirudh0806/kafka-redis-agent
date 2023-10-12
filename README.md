# kafka-redis-agent
# Message Processing in Kafka

This is a Python code that processes image URLs from a Kafka topic, downloads the images, resizes them, and stores the result in a Redis database.

## Prerequisites
1. Docker
2. Kafka
3. Redis
4. Python

### Installing Docker on Windows

This guide will help you install Docker on your Windows machine.

Before you begin, make sure your system meets the following requirements:

- Windows 10 Pro, Enterprise, or Education edition.
- Virtualization must be enabled in BIOS/UEFI settings.
- At least 4GB of RAM.

### Installation Steps

1. Download Docker Desktop for Windows from the official website: [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop).

2. Run the installer and follow the on-screen instructions.

3. During installation, you may be prompted to enable Hyper-V and Windows Subsystem for Linux (WSL). Allow these features if prompted.

4. Once the installation is complete, launch Docker Desktop.

5. Docker should now be up and running on your Windows machine.

6. Open a command prompt or PowerShell and verify Docker is installed by running:

     ```bash
     docker --version
     ```

Docker Desktop includes Docker Compose along with Docker Engine and Docker CLI which are Compose prerequisites.

### Installing Kafka and Redis on Docker using Docker Compose


1. Find `docker-compose-combined.yml` file in the sub-folder named ‘deploy’. 

2. Save the `docker-compose-combined.yml` file in your project directory.

3. Open a terminal or command prompt and navigate to the directory where your `docker-compose-combined.yml` file is located.

4. Run the following command to start the Redis, Kafka and ZooKeeper containers:

    ```bash
    docker-compose -f docker-compose-combined.yml up -d
    ```

5. To verify that the containers are running, you can run the following command:

    ```bash
    docker ps
    ```


### Using Kafka and Redis

Both Redis and Kafka are now up and running in Docker.

##### Running and Configuration of Kafka server and Redis:
- Start the Kafka server by typing this in the Kafka terminal

    ```bash
    docker exec -it kafka /bin/sh
    ```
- Redis CLI can also be used [Optional]
    ```bash
    docker exec -it redis redis-cli
    ```
    Configure redis on http://localhost:8001

  
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

1. Start a Kafka producer to send messages with image URLs and output size information to the Kafka topic.
   ```bash
    cd /opt/kafka_2.13-2.8.1/bin 
    ```
   Produce a message to your topic using the Kafka console producer:
    ```bash
    kafka-console-producer.sh --broker-list kafka:9092 --topic <topicname> 
    ```
2. Run the script using Python:

    ```bash
    python code.py
    ```

3. The script will consume messages from the 'secondtask' Kafka topic, download the images, resize them according to the specified dimensions, and store the results in Redis with keys like 'image0', 'image1', and so on.

