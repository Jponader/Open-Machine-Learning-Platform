README.txt

LOCAL
	Create Virtual Python environment
	Start virtual environment
	install all dependencies in requirments.txt


	run the following commands:

		cd website
		flask db init
		flask db migrate
		flask db upgrade
		cd ../
		python masterRunner.py



AWS
	Behind the Scenes
		Create S3 'open-ml-bucket'
		Create 2 SQS Queues: 'predictQueue', 'builderQueue'
		Create IAM profile, with Elastic Beanstalk Full Access privileges

		After all components are created add access right to the database for all components in AWS

	Website
		Create .ebextensions/01_pass.config

			option_settings:
			 aws:elasticbeanstalk:application:environment:
			   AWS_ACCESS_KEY_ID: <IAM Pass ID>
			   AWS_SECRET_ACCESS_KEY: <IAM Pass Key>

		Zip all files in the website folder

		Create Elastic Beanstalk Environment, with Mysql Database


	Build and Predictor
		Zip all files in the respected folder
		Create Elastic beanstalk for each 
		Add Queue to the environments, and /build or /predict
		After creation edit configuration, filling in database password, username and URL