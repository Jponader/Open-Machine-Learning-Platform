from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import boto3
import sys
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

if app.config['LOCAL']:
	sys.path.append('/Users/jonathanponader/Desktop/Open-Machine-Learning-Platform/Application')
	from localFile import localFile as boto3

s3Client = boto3.client('s3')
S3Name = app.config['S3NAME']

SQS = boto3.client('sqs')
buildQueue = SQS.get_queue_url(QueueName=app.config['BUILD_Q'])['QueueUrl']
predictQueue = SQS.get_queue_url(QueueName=app.config['PREDICT_Q'])['QueueUrl']


from app import routes