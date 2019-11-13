from flask_wtf import FlaskForm
from wtforms import StringField, TimeField, TextAreaField, PasswordField,\
    DecimalField, IntegerField, DateField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

from ..models import Usuario


class EstForm(FlaskForm):
    """"
        Formulário do Estilo Musical
    """

    nome = StringField('Nome Estilo Musical', validators=[DataRequired(), Length(min=1, max=15)])
    submit = SubmitField('Salvar')


class FuncionarioForm(FlaskForm):
    """"
        Formulário do Funcionario
    """

    nome = StringField('Nome do Funcionário', validators=[DataRequired(), Length(min=1, max=30)])
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=30)])
    senha = PasswordField('Senha', validators=[DataRequired(), EqualTo('confirma_senha')])
    confirma_senha = PasswordField('Comfirma Senha')
    submit = SubmitField('Salvar')

    def validar_username(self, field):
        if Usuario.query.filter_by(username=field.data).first():
            raise ValidationError('Username já está em uso')


class TipoIngForm(FlaskForm):
    """"
        Formulário do Tipo de Ingresso
    """
    nome = StringField('Nome do Tipo de Ingresso', validators=[DataRequired(), Length(min=1, max=30)])
    valor = DecimalField('Valor do Ingresso', places=2, validators=[DataRequired(), Length(min=1, max=5)])
    lote = IntegerField('Quantidade de Ingressos', validators=[DataRequired()])
    evento = SelectField('Evento', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Salvar')


class EmpresaForm(FlaskForm):
    """
        Formulário da Empresa
    """

    cnpj = StringField('CNPJ', validators=[DataRequired(), Length(min=18, max=18)])
    nome = StringField('Nome Fantasia', validators=[DataRequired(), Length(min=1, max=30)])
    telefone = StringField('Telefone', validators=[DataRequired(), Length(min=13, max=14)])
    descricao = TextAreaField('Descrição', validators=[DataRequired(), Length(min=1, max=100)])
    rua = StringField('Rua', validators=[DataRequired(), Length(min=1, max=25)])
    bairro = StringField('Bairro', validators=[DataRequired(), Length(min=1, max=25)])
    numero = StringField('Número', validators=[DataRequired(), Length(min=1, max=6)])
    submit = SubmitField('Salvar')


class EventoForm(FlaskForm):
    """"
        Formulário do Evento
    """

    nome = StringField('Nome do Evento', validators=[DataRequired(), Length(min=1, max=30)])
    data_inicio = DateField('Data de Início', validators=[DataRequired()], format='%d/%m/%Y')
    hora_inicio = TimeField('Hora de Início', validators=[DataRequired()], format='%H:%M')
    hora_final = TimeField('Hora Final', validators=[DataRequired()], format='%H:%M')
    descricao = TextAreaField('Descrição', validators=[DataRequired(), Length(min=1, max=100)])
    estilo = SelectField('Estilo Musical', validators=[DataRequired()], coerce=int)
    empresa = SelectField('Empresa', validators=[DataRequired()])
    submit = SubmitField('Salvar')


class RelatorioForm(FlaskForm):
    """
        Formulário do Relatório de Venda
    """
    empresa = SelectField('Empresa', validators=[DataRequired()])
    gerar = SubmitField('Gerar Relatório')
