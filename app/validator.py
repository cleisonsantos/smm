from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from app.models import Solution

def solution_exists(form, field):
    if not Solution.query.filter_by(id=id).first():
        raise ValidationError('Solution does not exist')

class ComponentForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    solution_id = IntegerField('solution_id', validators=[DataRequired(), solution_exists])
