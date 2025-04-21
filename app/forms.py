from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, FileField, SubmitField
from wtforms.validators import DataRequired

class CameraForm(FlaskForm):
    name = StringField('Camera Name', validators=[DataRequired()])
    brand = StringField('Brand', validators=[DataRequired()])
    type = SelectField('Type', choices=[('SLR', 'SLR'), ('Rangefinder', 'Rangefinder'), ('Compact', 'Compact')])
    format = SelectField('Format', choices=[('35mm', '35mm'), ('120', 'Medium Format'), ('Half-frame', 'Half-frame')])
    image = FileField('Camera Image')
    is_public = BooleanField('Make Public')
    submit = SubmitField('Upload')
