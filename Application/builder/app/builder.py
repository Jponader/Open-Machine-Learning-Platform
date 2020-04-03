from app import app, db
from app import s3Client, S3Name
from app.models import mlModels
import threading
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.callbacks.callbacks import EarlyStopping
import pandas as pd
import numpy as np
from sklearn import preprocessing
from math import ceil, log

#S3 
import boto3
import json
import os
import io

#Datamodes: Combined All in one, Seperated Has label set Always List

# Assumption, Clean data no trash, missing values and all numerical
# CSV, format -> <data>,<data>,<data>,...,<Label>
# UBYTE

#dataTypes: CSV, UBYTE

# TODO:
	# UBYTE
	# KERAS DATASETS
	# CUSTOM BUILDS
	# BETER AUTO BUILDS

class builder(threading.Thread):

	def __init__(self, id):
		threading.Thread.__init__(self)
		self.id = id

	def modelSave(self, model):
		model.save("temp.h5")
		s3Client.upload_file("temp.h5", S3Name, str(self.id) + 'model.h5')
		os.remove("temp.h5")

	def storeMapping(self, map):
		model = mlModels.query.get(self.id)
		model.mapping = str(map)
		db.session.commit()

	def getRecord(self):
		model = mlModels.query.get(self.id)
		self.config = json.loads(model.dict)
		self.data = json.loads(model.data)
		self.createdDate = model.creationdate

	def customModel():
		# parse cutom model to get model built by user
		pass

	def loadData(self):
		if self.data['dataType'] == 'CSV':
			data = s3Client.get_object(Bucket=S3Name, Key= str(self.createdDate) + self.data['data'])
			dataframe = pd.read_csv(io.BytesIO(data['Body'].read()), header=None) 
			if self.data['seperated'] and self.data['labels'] != None:
				data = s3Client.get_object(Bucket=S3Name, Key= str(self.createdDate) + self.data['labels'])
				labels = pd.read_csv(io.BytesIO(data['Body'].read()), header=None) 
				dataframe.merge(labels, left_index=True, right_index=True)

			return self.prepCSV(dataframe)


	def mapLabels(self, data):
		le = preprocessing.LabelEncoder()
		data.iloc[:,-1] = le.fit_transform(data.iloc[:,-1])
		print(type(le.classes_))
		self.storeMapping(le.classes_)
		return data

	def prepCSV(self,data):
		data = self.mapLabels(data)
		
		# Modify col that are not usable data to int or floats

		# Add sampling distribution to config
		train = data.sample(frac=(self.config['sampling']/100))
		test = data.sample(frac=(1 - (self.config['sampling']/100)))
		((xTrain,yTrain),(xTest, yTest))=((train.iloc[:,:-1], train.iloc[:,-1]), (test.iloc[:,:-1], test.iloc[:,-1]))

		self.localConfig = {
				'input': (xTrain.shape)[1],
				'output':len(data.iloc[:,-1].unique())
		}

		return ((xTrain,yTrain),(xTest, yTest))

	def layerSizes(self):
		layers = self.config['layers']
		inpow = int(ceil(log(self.localConfig['input'],2)))
		outpow = int(ceil(log(self.localConfig['output'],2)))
		powdif = abs(outpow - inpow)

		layerSet = []
		change = powdif / self.config['layers']

		if change < 1:
			change = 1

		if inpow > outpow:
			up = (layers - powdif)/2
		else:
			up = ceil(layers + powdif)/2

		for l in range(layers):
			if up > 0:
				inpow += change
				up -= 1
				layerSet.append(inpow)
			else:
				inpow -= change
				layerSet.append(inpow)
		return layerSet

	def buildModel(self):
		if self.config['custom']:
			model = customModel(self.config['model'])

		else: 
			layerSet = self.layerSizes()
			inputs = keras.Input(shape=self.localConfig['input'])
			x = inputs

			for i in range(self.config['layers']):
				x= layers.Dense(2**layerSet[i], activation='relu')(x)

			output = layers.Dense(self.localConfig['output'], activation='softmax')(x)
			model = keras.Model(inputs=inputs, outputs=output)

		return model



	def run(self):
		self.getRecord()
		((xTrain,yTrain),(xTest, yTest)) = self.loadData()
		model = self.buildModel()
		model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
		stop =EarlyStopping(monitor='val_loss', min_delta=0, patience=2, verbose=0, mode='auto', baseline=None, restore_best_weights=False)
		model.fit(xTrain, yTrain, epochs=1000, validation_data =(xTest, yTest), callbacks=[stop])
		model.summary()
		test_loss, test_acc = model.evaluate(xTest, yTest)
		print('Test accuracy:', test_acc)
		self.modelSave(model)
		model = mlModels.query.get(self.id)
		model.trained = True
		model.acc = float(test_acc)
		db.session.commit()

def main():
	model = builder(int(1))
	model.start()


if __name__ == '__main__':
	main()


