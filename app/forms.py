from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, FileField, SubmitField
from wtforms.validators import DataRequired






class CameraForm(FlaskForm):
    class Meta:
        csrf = False
    name = StringField('Camera Name', validators=[DataRequired()])
    brand = StringField('Brand', validators=[DataRequired()])
    type = SelectField('Type', choices=[('SLR', 'SLR'), ('Rangefinder', 'Rangefinder'), ('Compact', 'Compact')])
    format = SelectField('Format', choices=[('35mm', '35mm'), ('120', 'Medium Format'), ('Half-frame', 'Half-frame')])
    image = FileField('Camera Image')
    is_public = BooleanField('Make Public')
    submit = SubmitField('Upload')


class LensForm(FlaskForm):
    name = StringField('Lens Name', validators=[DataRequired()])
    brand = StringField('Brand', validators=[DataRequired()])
    mount_type = StringField('Mount Type', validators=[DataRequired()])
    image = FileField('Lens Image')
    is_public = BooleanField('Make Public')
    submit = SubmitField('Upload')


class FilmForm(FlaskForm):
    name = StringField('Film Name', validators=[DataRequired()])
    brand = StringField('Brand', validators=[DataRequired()])
    iso = StringField('ISO', validators=[DataRequired()])
    format = SelectField('Format', choices=[('35mm', '35mm'), ('120', 'Medium Format'), ('Sheet', 'Sheet')])
    image = FileField('Film Image')
    is_public = BooleanField('Make Public')
    submit = SubmitField('Upload')
