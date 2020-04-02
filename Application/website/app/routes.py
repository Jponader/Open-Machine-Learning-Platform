from app import app, db
from app import s3Client, S3Name, buildQueue, predictQueue, SQS
from app.models import *

from flask import render_template,flash, redirect, url_for, request, send_file
from app.forms import BuildForm, PredictForm
import json
import os
import io

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/build', methods=['GET', 'POST'])
def build():
	form = BuildForm()
	if form.validate_on_submit():

		if form.labels.data is None:
			seperated  = False
			lablesFileName = 'None'
		else:
			seperated = True
			lablesFileName = form.labels.data.filename

		model = mlModels(
			name = form.name.data, 
			model_desc = form.model_desc.data,
			data = json.dumps({'seperated': seperated, 'dataType': form.dataType.data, 'data': form.data.data.filename, 'labels': lablesFileName}),
			dict = json.dumps({'layers': form.layers.data, 'sampling': form.sampling.data ,'custom':form.custom.data, 'model':form.customDesc.data}))

		db.session.add(model)
		db.session.commit()

		s3Client.put_object(Bucket=S3Name, Key= str(model.creationdate)+ form.data.data.filename, Body=form.data.data)

		if seperated:
			s3client.put_object(Bucket=S3Name, Key= str(model.creationdate) + lablesFileName, Body=form.labels.data)

		SQS.send_message(QueueUrl =buildQueue, MessageBody = json.dumps({'id':model.model_id}))

		return redirect(url_for('model', id = model.model_id))
	return render_template('build.html', form=form)


@app.route('/predict')
def predict():
	page = request.args.get('page', 1, type=int)
	models = mlModels.query.paginate(page, app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('predict', page=models.next_num) if models.has_next else None
	prev_url = url_for('predict', page=models.prev_num) if models.has_prev else None
	return render_template('predict.html', models = models.items, next_url=next_url,
						   prev_url=prev_url)

@app.route('/model/<id>', methods=['GET', 'POST'])
def model(id):
	model = mlModels.query.get(id)
	form = PredictForm()
	if form.validate_on_submit():
		task = predictions(data = form.data.data.filename, model_id = id)
		db.session.add(task)
		db.session.commit()

		s3Client.put_object(Bucket=S3Name, Key= str(task.creationdate)+ form.data.data.filename, Body=form.data.data)

		SQS.send_message(QueueUrl =predictQueue, MessageBody = json.dumps({'id':task.pred_id}))

		return redirect(url_for('results', id = task.pred_id))
	data = json.loads(model.data)
	dictionary = json.loads(model.dict)
	return render_template('model.html', form = form, model=model, date = model.creationdate.strftime("%m/%d/%Y, %H:%M:%S"), layers = dictionary['layers'], sampling = dictionary['sampling'], custom = dictionary['custom'], customDesc = dictionary['model'], dataType = data['dataType'])


@app.route('/results/<id>')
def results(id):
	predict = predictions.query.get(id)
	model = mlModels.query.get(predict.model_id)
	return render_template('results.html', predict= predict, model = model, filename = str(predict.pred_id) + 'results.txt')


@app.route('/download/<filename>')
def download(filename):
	data = s3Client.get_object(Bucket=S3Name, Key= filename)
	data =io.BytesIO(data['Body'].read())
	return send_file(data, as_attachment=True,
					 attachment_filename='results.txt',
					 mimetype='text/plain')


@app.route('/downloadh5/<filename>')
def downloadh5(filename):
	data = s3Client.get_object(Bucket=S3Name, Key= filename)
	data =io.BytesIO(data['Body'].read())
	return send_file(data, as_attachment=True,
					 attachment_filename='model.h5',
					 mimetype='application/x-hdf5')


