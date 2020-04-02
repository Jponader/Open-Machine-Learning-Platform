from app import db
import datetime


class mlModels(db.Model):
	model_id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(64), index=True)
	model_desc = db.Column(db.String(256))
	creationdate = db.Column(db.DateTime(), index=True, default=datetime.datetime.utcnow)
	acc = db.Column(db.Float(), index=True, default = '0')
	data = db.Column(db.String(256))
	mapping = db.Column(db.String(256), default = '')
	trained = db.Column(db.Boolean(), default= False)
	dict = db.Column(db.String(256))
	pred = db.relationship('predictions', backref='modelUsed', lazy='dynamic')

	def __repr__(self):
		return '<ID {}, name {}>'.format(self.model_id, self.name)


class predictions (db.Model):
	pred_id = db.Column(db.Integer(), primary_key=True)
	model_id = db.Column(db.Integer(), db.ForeignKey('ml_models.model_id'))
	creationdate = db.Column(db.DateTime(), index=True, default=datetime.datetime.utcnow)
	data = db.Column(db.String(64))
	completed = db.Column(db.Boolean(), default= False)

	def __repr__(self):
		return '<ID {}, Model Used {}>'.format(self.pred_id, self.model_id)