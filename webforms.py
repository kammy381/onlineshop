from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, TextAreaField, PasswordField, BooleanField,ValidationError
from wtforms.validators import DataRequired, NumberRange, URL, Email, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField



class ProductForm(FlaskForm):
    name = StringField("Product name:", validators=[DataRequired()])
    price = DecimalField("Price:", validators=[DataRequired(), NumberRange(min=0.01,max=99999)])
    image_url = StringField("Image url:", validators=[URL(message='wrong url')])
    #description = StringField("Product description:", validators=[DataRequired()], widget=TextArea())
    description = CKEditorField("Product description", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password_hash = PasswordField("Password:", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match!')])
    password_hash2 = PasswordField("Confirm Password:", validators=[DataRequired()])
    address = StringField("Address:", validators=[DataRequired()])
    postal_code = StringField("Postalcode:", validators=[DataRequired()])
    city = StringField('City:', validators=[DataRequired()])
    country = StringField('Country:', validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")