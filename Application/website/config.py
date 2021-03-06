import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'key'

	basedir = os.path.abspath(os.path.dirname(__file__))

	if 'RDS_HOSTNAME' in os.environ:
	  DATABASE = {
		'NAME': os.environ['RDS_DB_NAME'],
		'USER': os.environ['RDS_USERNAME'],
		'PASSWORD': os.environ['RDS_PASSWORD'],
		'HOST': os.environ['RDS_HOSTNAME'],
		'PORT': os.environ['RDS_PORT'],
	  }
	  database_url = 'mysql+pymysql://%(USER)s:%(PASSWORD)s@%(HOST)s:%(PORT)s/%(NAME)s' % DATABASE
	  LOCAL = False
	else:
	  database_url = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
	  LOCAL = True


	SQLALCHEMY_DATABASE_URI = database_url
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	S3NAME = 'open-ml-bucket'
	POSTS_PER_PAGE = 5

	PREDICT_Q = 'predictQueue'
	BUILD_Q = 'builderQueue'
