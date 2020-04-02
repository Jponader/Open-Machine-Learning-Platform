from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
import boto3
import sys

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

if app.config['LOCAL']:
	sys.path.append('/Users/jonathanponader/Desktop/Open-Machine-Learning-Platform/Application')
	from localFile import localFile as boto3

s3Client = boto3.client('s3')
S3Name = app.config['S3NAME']

from app import routes