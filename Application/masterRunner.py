import subprocess
import threading
import os

class webServer(threading.Thread):
	def run(self):
		subprocess.call(['python',"website/application.py"])

class builderServer(threading.Thread):
	def run(self):
		subprocess.call(['python',"builder/application.py"])


class predictorServer(threading.Thread):
	def run(self):
		subprocess.call(['python',"predictor/application.py"])


if __name__ == '__main__':
	if not os.path.exists('VTS3'):
		os.makedirs('VTS3')

	web = webServer()
	build = builderServer()
	pred = predictorServer()

	web.start()
	build.start()
	pred.start()