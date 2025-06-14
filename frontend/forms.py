from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    nomeUtilizador = StringField('Nome de Utilizador', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    nomeUtilizador = StringField('Nome de Utilizador', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registar')

class SelectEntryTypeForm(FlaskForm):
    entry_type = SelectField(
        'Tipo',
        choices=[
            ('password','Password'),
            ('credit_card','Cartão Bancário'),
            ('ssh_key','Chave SSH'),
            ('note','Nota'),
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Seguinte')

class PasswordEntryForm(FlaskForm):
    title    = StringField('Título', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit   = SubmitField('Salvar')

class CreditCardEntryForm(FlaskForm):
    title       = StringField('Título', validators=[DataRequired()])
    card_number = StringField('Número do Cartão', validators=[DataRequired()])
    expiry_date = StringField('Validade (MM/AA)', validators=[DataRequired()])
    cvv         = StringField('CVV', validators=[DataRequired()])
    submit      = SubmitField('Salvar')

class SSHKeyEntryForm(FlaskForm):
    title   = StringField('Título', validators=[DataRequired()])
    ssh_key = TextAreaField('Chave SSH', validators=[DataRequired()])
    submit  = SubmitField('Salvar')

class NoteEntryForm(FlaskForm):
    title     = StringField('Título', validators=[DataRequired()])
    note_text = TextAreaField('Nota', validators=[DataRequired()])
    submit    = SubmitField('Salvar')
