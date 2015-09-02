from wtforms import Form, TextField, PasswordField, BooleanField, validators

class RegistrationForm(Form):

    firstName = TextField('First Name', [validators.Required(),
        validators.Length(min=2, max=30)])
    lastName = TextField('Last Name', [validators.Required(),
        validators.Length(min=2, max=30)])

    username = TextField('Username', [validators.Required(),
        validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Required(),
        validators.Length(min=6, max=60),
        validators.Email(message="Invalid email address.")])
    password = PasswordField('Password', [validators.Required(),
        validators.EqualTo('confirmPassword', message = 'Passwords must match.'),
        validators.Length(min=6, max=40)])
    confirmPassword = PasswordField('Repeat Password')

    acceptTOS = BooleanField('I accept the Terms of Service.', [validators.Required()])
