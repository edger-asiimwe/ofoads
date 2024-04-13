from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User, Restaurant

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RestaurantRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    latitude = StringField('Latitude', validators=[DataRequired()])
    longitude = StringField('Longitude', validators=[DataRequired()])
    submit = SubmitField('Create Restaurant Account')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(message='Email is already in use')
        
    def validate_name(self, field):
        if Restaurant.query.filter_by(name=field.data).first():
            raise ValidationError(message='Restaurant Name is already in use')
        
    