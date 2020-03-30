from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class AddJobsForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    team_leader = StringField('Team Leader id', validators=[DataRequired()])
    work_size = IntegerField('Work size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    is_finished = BooleanField("Is job finished?")
    submit = SubmitField('Submit')
