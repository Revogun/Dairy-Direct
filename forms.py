from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
import re

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    user_type = SelectField(
        'User Type',
        choices=[('', 'Select user type'), ('farmer', 'Farmer'), ('entrepreneur', 'Entrepreneur')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Register')

    def validate_phone(self, phone):
        # Validate phone number format
        if not re.match(r'^\+?[0-9\s\-]+$', phone.data):
            raise ValidationError('Please enter a valid phone number')
