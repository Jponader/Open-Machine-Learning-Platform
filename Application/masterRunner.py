import subprocess
import threading

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
	web = webServer()
	build = builderServer()
	pred = predictorServer()

	web.start()
	build.start()
	pred.start()