from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from sqlalchemy.dialects.mysql import TIME, TINYINT
import uuid


class Usuario(db.Model, UserMixin):
    """"Cria uma Tabela Usuario"""

    __tablename__ = 'usuario'

    id = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    senha_hash = db.Column(db.String(100), nullable=False)
    # admins = db.relationship('Admins', backref='usuarios', lazy=True)
    funcionario = db.relationship('Funcionario', backref='usuario', lazy=True)
    cliente = db.relationship('Cliente', backref='usuario', lazy=True)

    @property
    def senha(self):

        raise AttributeError('Senha não pode ser lida.')

    @senha.setter
    def senha(self, senha):

        self.senha_hash = generate_password_hash(senha)

    def verifica_senha(self, senha):

        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return '<Usuario: {}>'.format(self.username)


@login_manager.user_loader
def load_user(usu_id):
    return Usuario.query.get(int(usu_id))


class Funcionario(db.Model):
    """Cria uma Tabela Funcionário"""

    __tablename__ = 'funcionario'
    
    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    nome = db.Column(db.String(30), nullable=False)
    estado = db.Column(TINYINT(1), nullable=False, default=0)
    admin = db.Column(TINYINT(1), nullable=False, default=0)
    usu_id = db.Column(db.Integer(), db.ForeignKey('usuario.id'), nullable=False)
    empresa = db.relationship('Empresa', backref='funcionario', lazy=True)
    evento = db.relationship('Evento', backref='funcionario', lazy=True)
    estilo = db.relationship('EstiloMusical', backref='funcionario', lazy=True)
    tipo_ingresso = db.relationship('TipoIngresso', backref='funcionario', lazy=True)

    def __repr__(self):
        return '<Funcionário: {}>'.format(self.id)


class Cliente(db.Model):
    """"Cria a tabela Cliente"""

    __tablename__ = 'cliente'

    cpf = db.Column(db.String(14), nullable=False, unique=True, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    data_nasc = db.Column(db.Date(), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    estado = db.Column(TINYINT(1), nullable=False, default=0)
    usu_id = db.Column(db.Integer(), db.ForeignKey('usuario.id'), nullable=False)
    compra = db.relationship('Compra', backref='cliente', lazy=True)

    def __repr__(self):
        return '<Cliente: {}>'.format(self.cpf)


class Empresa(db.Model):
    """"Cria a tabela Empresa"""

    __tablename__ = 'empresa'

    cnpj = db.Column(db.String(18), nullable=False, unique=True, primary_key=True)
    nomefantasia = db.Column(db.String(30), nullable=False)
    telefone = db.Column(db.String(14), nullable=False)
    descricao = db.Column(db.Text(100), nullable=False)
    estado = db.Column(TINYINT(1), nullable=False, default=0)
    end_id = db.Column(db.Integer(), db.ForeignKey('endereco.id'), nullable=False)
    func_id = db.Column(db.Integer(), db.ForeignKey('funcionario.id'), nullable=False)
    evento = db.relationship('Evento', backref='empresa', lazy=True)

    def __repr__(self):
        return '<Empresa: {}>'.format(self.cnpj)


class Endereco(db.Model):
    """"Cria a tabela Endereco"""

    __tablename__ = 'endereco'

    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    rua = db.Column(db.String(25), nullable=False)
    bairro = db.Column(db.String(25), nullable=False)
    numero = db.Column(db.String(6), nullable=False)
    empresa = db.relationship('Empresa', backref='endereco', lazy=True)

    def __repr__(self):
        return '<Endereco: {}>'.format(self.id)


class EstiloMusical(db.Model):
    """"Cria a tabela Estilo Musical"""

    __tablename__ = 'estilomusical'

    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    nome = db.Column(db.String(15), nullable=False)
    func_id = db.Column(db.Integer(), db.ForeignKey('funcionario.id'), nullable=False)
    evento = db.relationship('Evento', backref='estilomusical', lazy=True)

    def __repr__(self):
        return '<Estilo Musical: {}>'.format(self.nome)


class Evento(db.Model):
    """"Cria a tabela Evento"""

    __tablename__ = 'evento'

    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    nomeevento = db.Column(db.String(30), nullable=False)
    data_inicio = db.Column(db.Date(), nullable=False)
    hora_inicio = db.Column(TIME(), nullable=False)
    hora_final = db.Column(TIME(), nullable=False)
    descricao = db.Column(db.Text(100), nullable=False)
    image = db.Column(db.String(50), nullable=False)
    estado = db.Column(TINYINT(1), nullable=False, default=0)
    est_id = db.Column(db.Integer(), db.ForeignKey('estilomusical.id'), nullable=False)
    cnpj_emp = db.Column(db.String(18), db.ForeignKey('empresa.cnpj'), nullable=False)
    func_id = db.Column(db.Integer(), db.ForeignKey('funcionario.id'), nullable=False)
    compra = db.relationship('Compra', backref='evento', lazy=True)
    tipo_ingresso = db.relationship('TipoIngresso', backref='evento', lazy=True)

    def __repr__(self):
        return '<Evento: {}>'.format(self.id)


class Compra(db.Model):
    """"Cria a tabela Compra"""

    __tablename__ = 'compra'

    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    valor_total = db.Column(db.Numeric(5, 2), nullable=False)
    data_compra = db.Column(db.DateTime(), nullable=False)
    evt_id = db.Column(db.Integer(), db.ForeignKey('evento.id'), nullable=False)
    cpf_cli = db.Column(db.String(14), db.ForeignKey('cliente.cpf'), nullable=False)
    itens_compra = db.relationship('ItensCompra', backref='compra', lazy=True)

    def __repr__(self):
        return '<Compra: {}>'.format(self.id)


class TipoIngresso(db.Model):
    """"Cria a tabela Tipo Ingresso"""

    __tablename__ = 'tipo_ingresso'

    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    valor = db.Column(db.Numeric(5, 2), nullable=False)
    lote = db.Column(db.Integer(), nullable=False)
    estado = db.Column(TINYINT(1), nullable=False, default=0)
    evt_id = db.Column(db.Integer(), db.ForeignKey('evento.id'), nullable=False)
    func_id = db.Column(db.Integer(), db.ForeignKey('funcionario.id'), nullable=False)
    itens_compra = db.relationship('ItensCompra', backref='tipo_ingresso', lazy=True)

    def __repr__(self):
        return '<Tipo Ingresso: {}>'.format(self.id)


class ItensCompra(db.Model):
    """""Cria a tabela Itens Compra"""

    __tablename__ = 'itens_compra'

    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    qtd = db.Column(db.Integer(), nullable=False)
    compra_id = db.Column(db.Integer(), db.ForeignKey('compra.id'), nullable=False)
    tipo_id = db.Column(db.Integer(), db.ForeignKey('tipo_ingresso.id'), nullable=False)

    def __repr__(self):
        return '<Itens Compra: {}>'.format(self.id)

