from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DateField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from ..models import Usuario, Cliente


class RegistroForm(FlaskForm):
    """"
        Formulario para Clientes criarem uma nova conta
    """

    nome = StringField('Nome', validators=[DataRequired(), Length(min=1, max=30)])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=1, max=30)])
    data_nasc = DateField('Data de Nascimento', validators=[DataRequired()], format='%d/%m/%Y')
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=30)])
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=30)])
    senha = PasswordField('Senha', validators=[DataRequired(), EqualTo('confirma_senha')])
    confirma_senha = PasswordField('Confirma Senha')
    registrar = SubmitField('Registra')

    def validar_email(self, field):
        if Cliente.query.filter_by(email=field.data).first():
            raise ValidationError('Email já está em uso.')

    def validar_username(self, field):
        if Usuario.query.filter_by(username=field.data).first():
            raise ValidationError('Username já está em uso')


class LoginForm(FlaskForm):
    """"
        Formulario para Login
    """
    username = StringField('Username', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    logar = SubmitField('Login')
