from flask import flash, redirect, render_template, url_for, session, request
from flask_login import login_required, login_user, logout_user
from datetime import timedelta

from . import aute
from .forms import LoginForm, RegistroForm
from .. import db
from ..models import Usuario, Cliente, Funcionario


@aute.route('/registra', methods=['GET', 'POST'])
def registro():
    """"
        Adiciona Usario e Cliente no Banco de Dados
        Atraves do formulario de registro
    """
    form = RegistroForm()

    if request.method == 'POST':

        usuario = Usuario(username=form.username.data, senha=form.senha.data)
        db.session.add(usuario)
        db.session.commit()

        usu_id = Usuario.query.filter_by(username=form.username.data).first()

        cliente = Cliente(nome=form.nome.data,
                          cpf=form.cpf.data,
                          data_nasc=form.data_nasc.data,
                          email=form.email.data,
                          usu_id=[usu_id.id])

        db.session.add(cliente)
        db.session.commit()

        flash('Cadastrado com sucesso! Agora você pode se logar', 'success')

        # redireciona para a página de Login
        return redirect(url_for('aute.login'))

    # Carrega a página de Cadastro
    return render_template('aute/registro.html', form=form, title='Registro')


@aute.route('/login', methods=['GET', 'POST'])
def login():
    """"
        Cuida da chamada da rota /login
        Realiza o login dos usuarios
    """

    form = LoginForm()
    if request.method == 'POST':

        # Procura se o usuario existe no BD e
        # se senha informada é igual ao do BD
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        if usuario is not None and usuario.verifica_senha(form.senha.data):

            if Funcionario.query.filter_by(usu_id=usuario.id).first():

                funcionario = Funcionario.query.filter_by(usu_id=usuario.id).first()
                # Se Funcionario for Admin
                if funcionario.admin == 1:

                    # Concede acesso ao Funcionario
                    login_user(usuario, duration=timedelta(days=1))

                    # Salva nos cookies
                    session['Func'] = True
                    session['Admin'] = True
                    session['Cli'] = False
                    session['id'] = funcionario.id

                    # Retorna para o Dashboard do Funcionario
                    return redirect(url_for('func.dashboard'))

                # Se Funcionario não for Admin
                elif funcionario.admin == 0:

                    # Concede acesso ao Funcionario
                    login_user(usuario, duration=timedelta(days=1))

                    # Salva nos cookies
                    session['Func'] = True
                    session['Admin'] = False
                    session['Cli'] = False
                    session['id'] = funcionario.id

                    # Retorna para o Dashboard do Funcionario
                    return redirect(url_for('func.dashboard'))

            # Se não cliente
            else:

                # Concede acesso ao Cliente
                login_user(usuario,remember=True, duration=timedelta(days=15))

                cli = Cliente.query.filter_by(usu_id=usuario.id).first()

                # Salva nos cookies se for Cliente
                session['Func'] = False
                session['Admin'] = False
                session['Cli'] = True
                session['CPF'] = cli.cpf

                # Retorna para a tela de Eventos
                return redirect(url_for('home.eventos'))

        # Se for Incorreto
        else:
            flash('Username ou Senha inválidos!', 'danger')

    # Carrega página de Login
    return render_template('aute/login.html', form=form, title='Login')


@aute.route('/logout')
@login_required
def logout():
    """"
        Cuida da Chamada da rota /logout
        Logout o usuario
    """
    session.clear()
    logout_user()
    flash('Você não está mais logado', 'success')

    # redireciona para a página de login
    return redirect(url_for('aute.login'))
