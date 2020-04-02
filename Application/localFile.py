import requests 
import json

storage = "VTS3/"

class localFile():

	class client():

		def __init__(self, type):
			self.type = type

		#s3Client.put_object(Bucket=S3Name, Key= str(model.creationdate)+ form.data.data.filename, Body=form.data.data)
		def put_object(self,Bucket = None, Key = None, Body = None):
			#Key = hash(Key)
			Body.save(storage + str(Key))

		#Need to make sure teh file goes to the right place
		#s3Client.download_file(S3Name, str(predict.pred_id) + 'results.txt',str(predict.pred_id) + 'results.txt')
		def download_file(self, Bucket=None, Key=None, Filename=None):
			#Key = hash(Key)
			f = open(storage + str(Key),"rb")
			body = f.read()
			f.close()
			f = open(Filename, "wb")
			f.write(body)
			f.close()
		

		#s3Client.upload_file("temp.h5", S3Name, str(self.id) + 'model.h5')
		def upload_file(self, filename, Bucket, Key):
			#Key = hash(Key)
			f = open(filename, "rb")
			body = f.read()
			f.close()
			f = open(storage + str(Key), "wb")
			f.write(body)
			f.close()

		#s3Client.get_object(Bucket=S3Name, Key= str(self.createdDate) + self.data['data'])
		def get_object(self, Bucket, Key):

			class response():
				def __init__(self, data):
					self.data = data

				def read(self):
					return self.data

			#Key = hash(Key)
			f = open(storage + str(Key),"rb")
			body = f.read()
			f.close()
			return {'Body':response(body)}

		def get_queue_url(self, QueueName=None):
			return {'QueueUrl':QueueName}

		def send_message(self,MessageBody = None, QueueUrl = None):
					if QueueUrl == 'predictQueue':
						requests.post(url ='http://0.0.0.0:5002/predict', json = json.loads(MessageBody))
					if QueueUrl == 'builderQueue':
						requests.post(url ='http://0.0.0.0:5001/build', json = json.loads(MessageBody))
		

		


		




















