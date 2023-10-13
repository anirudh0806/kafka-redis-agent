from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'Kafka Message Processing Agent'
LONG_DESCRIPTION = 'Processes kafka messages and stores it in Redis'

# Setting up
setup(
    name="kafkaredis_agent",
    version=VERSION,
    author="Anirudh",
    author_email="<anirudh@hotmail.com>",
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "KafkaConsumer", "json",
              "redis", "PIL", "ImageProcessingAgent"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
