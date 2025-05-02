from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, FileField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional

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
    class Meta:
        csrf = False
    name = StringField('Lens Name', validators=[DataRequired()])
    brand = StringField('Brand', validators=[DataRequired()])
    mount_type = StringField('Mount Type', validators=[DataRequired()])
    image = FileField('Lens Image')
    is_public = BooleanField('Make Public')
    submit = SubmitField('Upload')

class FilmForm(FlaskForm):
    class Meta:
        csrf = False
    name = StringField('Film Name', validators=[DataRequired()])
    brand = StringField('Brand', validators=[DataRequired()])
    iso = StringField('ISO', validators=[DataRequired()])
    format = SelectField('Format', choices=[('35mm', '35mm'), ('120', 'Medium Format'), ('Sheet', 'Sheet')])
    image = FileField('Film Image')
    is_public = BooleanField('Make Public')
    submit = SubmitField('Upload')

class RollForm(FlaskForm):
    class Meta:
        csrf = False
    roll_name = StringField('Roll Name', validators=[Optional()])
    film_id = SelectField('Film Used', coerce=int, validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    status = SelectField('Status', choices=[('in use', 'In Use'), ('finished', 'Finished')], validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Roll')

class PhotoForm(FlaskForm):
    class Meta:
        csrf = False
    shot_date = DateField('Shot Date', validators=[Optional()])
    shutter_speed = StringField('Shutter Speed', validators=[Optional()])
    aperture = StringField('Aperture', validators=[Optional()])
    iso = StringField('ISO', validators=[Optional()])
    frame_number = StringField('Frame Number', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])

    camera_id = SelectField('Camera', coerce=int, validators=[Optional()])
    lens_id = SelectField('Lens', coerce=int, validators=[Optional()])
    film_id = SelectField('Film', coerce=int, validators=[Optional()])
    roll_id = SelectField('Roll', coerce=int, validators=[Optional()])

    submit = SubmitField('Save Photo')