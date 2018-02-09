from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError, SelectField
from wtforms.validators import DataRequired, Length
from app.backend.models import Post


class AddPostForm(FlaskForm):
    
    post_title = StringField('Title', validators=[DataRequired(), Length(min=1)])
    post_body = StringField('Post Body', validators=[DataRequired(), Length(min=1)])
    post_topic = StringField('Topic', validators=[DataRequired(), Length(min=1)])
    post_tag = StringField('Tag', validators=[DataRequired(), Length(min=1)])
    post_status = SelectField('Post status',
                              validators=[DataRequired()],
                              choices=[('Draft', 'Draft'), ('Post', 'Post')]
                              )
