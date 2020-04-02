from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SelectField, IntegerField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class BuildForm(FlaskForm):
	name = StringField('Model Name', validators=[DataRequired()])
	model_desc = TextAreaField('Model Description', validators=[DataRequired()])
	data = FileField('Data', validators=[FileRequired()])
	labels = FileField('Lables')
	dataType = SelectField('Data Type', choices=[('CSV', 'CSV'), ('IMG', 'Zipped Images'), ('UBYTE', 'UBYTE')], validators=[DataRequired()])
	custom = BooleanField('Custom Model')
	customDesc = TextAreaField('Custom Model Desc')
	layers = IntegerField('Number of Layers', validators=[DataRequired()])
	sampling = IntegerField('Sampling Distribution', validators=[DataRequired()])
	buildModel = SubmitField('Build Model')

class PredictForm(FlaskForm):
	data = FileField('Data', validators=[FileRequired()])
	predict = SubmitField('Predict')