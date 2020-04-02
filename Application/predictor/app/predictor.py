from app import app, db
from app import s3Client, S3Name
from app.models import mlModels, predictions
import threading
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import numpy as np
from sklearn import preprocessing

#S3 
import boto3
import pymysql
import json
import os
import io
import csv


# TODO:
	# UBYTE
	# KERAS DATASETS
	

class predictor(threading.Thread):

	def __init__(self, id):
		threading.Thread.__init__(self)
		self.id = id

	def getAssingment(self):
		task = predictions.query.get(self.id)
		self.modelId = task.model_id
		self.dataKey = task.data
		self.date = task.creationdate

		model = mlModels.query.get(self.modelId)
		self.dataType = json.loads(model.data)['dataType']
		self.mapping = model.mapping

	def loadModel(self):
		s3Client.download_file(S3Name, str(self.modelId) + 'model.h5', 'temp.h5')
		self.model= keras.models.load_model('temp.h5')
		os.remove('temp.h5')
	
	def loadData(self):
		if self.dataType == 'CSV':
			data = s3Client.get_object(Bucket=S3Name, Key=str(self.date) + self.dataKey)
			dataframe = pd.read_csv(io.BytesIO(data['Body'].read()), header=None) 

			return self.prepCSV(dataframe)

	def prepCSV(self,data):
		return data

	def labelConverter(self, data):
		lables = self.mapping[2:-2].split("' '")
		return [[lables[i.argmax()]] for i in data ]

	def saveResults(self, data):
		with open('temp.csv', 'w', newline='\n') as temp:
			wr = csv.writer(temp)
			for i in data:
				wr.writerow(i)
		s3Client.upload_file("temp.csv", S3Name, str(self.id) + 'results.txt')
		os.remove("temp.csv")


	def run(self):
		self.getAssingment()
		self.loadModel()
		data = self.loadData()
		pred = self.model.predict(data, verbose=1)
		pred = self.labelConverter(pred)
		print(pred)
		self.saveResults(pred)
		task = predictions.query.get(self.id)
		task.completed = True
		db.session.commit()

def main():
	model = predictor(1)
	model.start()

if __name__ == '__main__':
    main()


