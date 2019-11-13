from flask import flash, redirect, render_template, url_for, session, abort, request, json
from flask_login import login_required
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from . import func
from app import create_app
from .forms import EstForm, FuncionarioForm, TipoIngForm, EmpresaForm, EventoForm, RelatorioForm
from .. import db
from ..models import Usuario, Funcionario, Empresa, EstiloMusical, TipoIngresso, Endereco, Evento, Compra

UPLOAD_FOLDER = 'C:/Users/T-Gamer/OneDrive/Faculdade/8P/TCCpy/DigIngressoPy/app/static/img'

def check_func():
    """"
        Previnir que outros tenham acesso
    """
    if not session['Func']:
        abort(403)


def check_admin():

    if not session['Admin']:
        abort(403)


@func.route('/dashboard')
@login_required
def dashboard():
    """"
        Chamada para a Dashboard Funcionario
    """
    # Se for funcionario
    check_func()

    return render_template('func/dashboard.html', title='Dashboard')


@func.route('/estilomusical/cadastrar', methods=['GET', 'POST'])
@login_required
def cad_estilo():
    """"
        Cadastra o Estilo Musical
    """
    # Checa se é o Funcionario que está realizando a operação
    check_func()

    add_estilo = True

    form = EstForm()

    if request.method == 'POST':
        estilo = EstiloMusical(nome=form.nome.data, func_id=session['id'])

        try:
            # Cadastra os estilo no BD
            db.session.add(estilo)
            db.session.commit()
            flash('Estilo Musical cadastrado com sucesso, Deseja realizar outro cadastro?', 'func.cad_estilo')

        except:
            # Error
            flash('Erro ao cadastrar o Estilo Musical', 'warning')

        return redirect(url_for('func.dashboard'))

    # Carrega a página
    return render_template('func/estilomusical/estilomusical.html', action='Cad',
                           add_estilo=add_estilo, form=form, title='Cadastrar Estilo Musical')


@func.route('/estilomusical/pesquisar', methods=['GET', 'POST'])
@login_required
def listar_estilo():
    """"
        Lista todos os Estilos Musicais
    """

    check_func()

    estilos = EstiloMusical.query.order_by(EstiloMusical.nome).all()

    return render_template('func/estilomusical/pesqestilomusical.html',
                           estilos=estilos, title='Estilos Musicais')


@func.route('/estilomusical/alterar/<int:id>', methods=['GET', 'POST'])
@login_required
def alterar_estilo(id):
    """"
        Alterar Estilo Musical
    """

    check_func()

    add_estilo = False

    estilo = EstiloMusical.query.get_or_404(id)
    form = EstForm(obj=estilo)
    if request.method == 'POST':
        estilo.nome = form.nome.data
        estilo.func_id = session['id']

        db.session.commit()

        flash('Estilo Musical alterado com sucesso', 'alterar')

        # Redireciona para a tela de pesquisar
        return redirect(url_for('func.listar_estilo'))

    form.nome.data = estilo.nome

    return render_template('func/estilomusical/estilomusical.html', action='Alt',
                           add_estilo=add_estilo, form=form, estilo=estilo,
                           title='Alterar Estilo Musical')


@func.route('/estilomusical/deletar/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_estilo(id):
    """"
        Deletar Estilo Musical do BD
    """

    check_func()

    estilo = EstiloMusical.query.get_or_404(id)
    db.session.delete(estilo)
    db.session.commit()
    flash('Você deletou com sucesso o Estilo Musical')

    # Redireciona para o Pesquisar
    return redirect(url_for('func.listar_estilo'))


@func.route('/funcionario/cadastrar', methods=['GET', 'POST'])
@login_required
def cad_func():
    """"
        Cadastrar um novo Funcionario
    """

    # Checar se é o Funcionario que está realizando a operação
    check_func()

    check_admin()

    add_func = True

    form = FuncionarioForm()

    if request.method == 'POST':

        usuario = Usuario(username=form.username.data,senha=form.senha.data)

        try:
            db.session.add(usuario)
            db.session.commit()
            usu_id = Usuario.query.filter_by(username=form.username.data).first()

            if request.form.get('admin'):
                funcionario = Funcionario(nome=form.nome.data, usu_id=[usu_id.id], admin=1)
                db.session.add(funcionario)
                db.session.commit()
            else:
                funcionario = Funcionario(nome=form.nome.data, usu_id=[usu_id.id])
                db.session.add(funcionario)
                db.session.commit()

            flash('Funcionario cadastrado com sucesso, Deseja realizar outro cadastro?', 'func.cad_func')

        except:
            # Error
            flash('Erro ao cadastrar o funcionario', 'warning')

        return redirect(url_for('func.dashboard'))

    return render_template('func/funcionario/funcionario.html', action='Cad',
                           add_func=add_func, form=form, title='Cadastrar Funcionário')


@func.route('/funcionario/pesquisar', methods=['GET', 'POST'])
@login_required
def pesquisar_func():
    """"
        Pesquisar Funcionario
    """

    check_func()

    check_admin()

    funcionarios = False

    if request.method == 'POST':
        pesq = request.form['pesq_func']

        funcionarios = Funcionario.query.filter(Funcionario.nome.like(pesq+'%'),
                                                Funcionario.estado == 0).all()

        return render_template('func/funcionario/pesqfuncionario.html',
                               funcionarios=funcionarios, title='Funcionarios')

    return render_template('func/funcionario/pesqfuncionario.html',
                           title='Funcionarios', funcionarios=funcionarios)


@func.route('/funcionario/alterar/<int:id>', methods=['GET', 'POST'])
@login_required
def alterar_func(id):
    """"
        Alterar a senha do Funcionario
    """

    check_func()

    check_admin()

    add_func = False

    usuario = Usuario.query.get_or_404(id)

    form = FuncionarioForm(obj=usuario)

    if request.method == 'POST':
        usuario.senha = form.senha.data

        db.session.commit()

        flash('Você alterou a senha do Funcionario com sucesso!', 'alterar')

        return redirect(url_for('func.pesquisar_func'))

    return render_template('func/funcionario/funcionario.html', action="Alt",
                           add_func=add_func, form=form, usuario=usuario,
                           title="Alterar Funcionario")


@func.route('/funcionario/deletar/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_func(id):
    """"
        Desativar Funcionario
    """

    check_func()

    check_admin()

    funcionario = Funcionario.query.get_or_404(id)
    funcionario.estado = 1

    db.session.commit()

    flash('Funcionario excluido com sucesso!', 'success')

    # Redireciona para o Pesquisar
    return redirect(url_for('func.pesquisar_func'))


@func.route('/tipoingresso/cadastrar', methods=['GET', 'POST'])
@login_required
def cad_ting():
    """"
        Cadastrar um novo Tipo de Ingresso
    """

    check_func()

    add_ting = True

    evento = Evento.query.filter(Evento.estado == 0).order_by(Evento.nomeevento).all()
    lista_evento = [(evt.id, evt.nomeevento) for evt in evento]

    form = TipoIngForm()

    form.evento.choices = lista_evento

    if request.method == 'POST':

        tipoingresso = TipoIngresso(nome=form.nome.data,
                                    valor=str(form.valor.data).replace(',', '.'),
                                    lote=form.lote.data,
                                    evt_id=form.evento.data,
                                    func_id=session['id'])

        try:
            db.session.add(tipoingresso)
            db.session.commit()

            flash('Tipo Ingresso cadastrado com sucesso, Deseja realizar outro cadastro?', 'func.cad_ting')

        except:
            # Error
            flash('Erro ao cadastrar o Tipo de Ingresso', 'warning')

        return redirect(url_for('func.dashboard'))

    # Carrega a página
    return render_template('func/tipoingresso/tipoingresso.html', action='Cad',
                           add_ting=add_ting, form=form, title='Cadastrar Tipo de Ingresso')


@func.route('/tipoingresso/pesquisar', methods=['GET', 'POST'])
@login_required
def pesquisar_ting():
    """"
        Pesquisar Tipo de Ingresso
    """

    check_func()

    tings = False

    if request.method == 'POST':
        pesq = request.form['pesq_ting']

        tings = TipoIngresso.query.filter(TipoIngresso.nome.like(pesq+'%'),
                                          TipoIngresso.estado == 0).all()

        return render_template('func/tipoingresso/pesqtipoingresso.html',
                               tings=tings, title='Tipo de Ingressos')

    return render_template('func/tipoingresso/pesqtipoingresso.html',
                           tings=tings, title='Tipo de Ingressos')


@func.route('/tipoingresso/alterar/<int:id>', methods=['GET', 'POST'])
@login_required
def alterar_ting(id):
    """"
        Alterar Tipo de Ingresso
    """

    check_func()

    add_ting = False

    evento = Evento.query.filter(Evento.estado == 0).all()
    lista_evento = [(evt.id, evt.nomeevento) for evt in evento]

    ting = TipoIngresso.query.get_or_404(id)

    form = TipoIngForm(obj=ting)

    if request.method == 'POST':

        ting.nome = form.nome.data
        ting.valor = str(form.valor.data).replace(',', '.')
        ting.lote = form.lote.data
        ting.func_id = session['id']

        db.session.commit()

        flash('Você alterou o Tipo de Ingresso com sucesso!', 'alterar')

        return redirect(url_for('func.pesquisar_ting'))

    form.evento.choices = lista_evento
    form.evento.data = ting.evt_id

    return render_template('func/tipoingresso/tipoingresso.html', action='Alt',
                           add_ting=add_ting, form=form, title='Alterar Tipo de Ingresso')


@func.route('/tipoingresso/deletar/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_ting(id):
    """"
        Deletar/Desativar Tipo de Ingresso
    """

    check_func()

    ting = TipoIngresso.query.get_or_404(id)

    ting.estado = 1

    db.session.commit()

    flash('Tipo de Ingresso excluido com sucesso!', 'success')

    # Redireciona para o Pesquisar
    return redirect(url_for('func.pesquisar_ting'))


@func.route('/empresa/cadastrar', methods=['GET', 'POST'])
@login_required
def cad_emp():
    """"
        Cadastrar Empresa
    """

    check_func()

    add_emp = True

    form = EmpresaForm()

    if request.method == 'POST':

        endereco = Endereco(rua=form.rua.data,
                            bairro=form.bairro.data,
                            numero=form.numero.data)

        try:
            db.session.add(endereco)
            db.session.commit()

            end = Endereco.query.filter_by(rua=form.rua.data,
                                           bairro=form.bairro.data,
                                           numero=form.numero.data).first()

            empresa = Empresa(cnpj=form.cnpj.data,
                              nomefantasia=form.nome.data,
                              telefone=form.telefone.data,
                              descricao=form.descricao.data,
                              end_id=[end.id],
                              func_id=session['id'])

            db.session.add(empresa)
            db.session.commit()

            flash('Empresa cadastrada com sucesso, Deseja realizar outro cadastro?', 'func.cad_emp')

        except:
            # Error
            flash('Erro ao cadastrar a empresa', 'warning')

        return redirect(url_for('func.dashboard'))

    return render_template('func/empresa/empresa.html', action='Cad',
                           add_emp=add_emp, form=form, title='Cadastrar Empresa')


@func.route('/empresa/pesquisar', methods=['GET', 'POST'])
@login_required
def pesquisar_emp():
    """"
        Pesquisar Empresa
    """

    check_func()

    emps = False

    if request.method == 'POST':

        pesq = request.form['pesq_emp']

        emps = Empresa.query.filter(Empresa.nomefantasia.like(pesq+'%'),
                                    Empresa.estado == 0).all()

        return render_template('func/empresa/pesqempresa.html',
                               emps=emps, title='Empresa')

    return render_template('func/empresa/pesqempresa.html',
                           emps=emps, title='Empresa')


@func.route('/empresa/alterar/<path:cnpj>', methods=['GET', 'POST'])
@login_required
def alterar_emp(cnpj):
    """"
        Alterar Empresa
    """

    check_func()

    add_emp = False

    emp = Empresa.query.get_or_404(cnpj)

    end = Endereco.query.filter(Endereco.id == emp.end_id).first()

    form = EmpresaForm()

    if request.method == 'POST':

        emp.nomefantasia = form.nome.data
        emp.telefone = form.telefone.data
        emp.descricao = form.descricao.data
        emp.func_id = session['id']

        end.rua = form.rua.data
        end.bairro = form.bairro.data
        end.numero = form.numero.data

        db.session.commit()

        flash('Você alterou a Empresa com sucesso', 'alterar')

        return redirect(url_for('func.pesquisar_emp'))

    form.cnpj.data = cnpj
    form.nome.data = emp.nomefantasia
    form.telefone.data = emp.telefone
    form.descricao.data = emp.descricao
    form.rua.data = end.rua
    form.bairro.data = end.bairro
    form.numero.data = end.numero

    return render_template('func/empresa/empresa.html', action='Alt',
                           add_emp=add_emp, form=form, title='Alterar Empresa')


@func.route('/empresa/deletar/<path:cnpj>', methods=['GET', 'POST'])
@login_required
def delete_emp(cnpj):
    """"
        Deletar/Desativar Empresa
    """

    check_func()

    emp = Empresa.query.get_or_404(cnpj)

    emp.estado = 1

    db.session.commit()

    flash('Empresa excluida com sucesso!', 'success')

    # Redireciona para o Pesquisar
    return redirect(url_for('func.pesquisar_emp'))


@func.route('/evento/cadastrar', methods=['GET', 'POST'])
@login_required
def cad_evt():
    """"
        Cadastrar Evento
    """

    check_func()

    add_evt = True

    estilos = EstiloMusical.query.order_by(EstiloMusical.nome).all()
    lista_estilo = [(est.id, est.nome) for est in estilos]

    empresas = Empresa.query.filter(Empresa.estado == 0).order_by(Empresa.nomefantasia).all()
    lista_empresa = [(emp.cnpj, emp.nomefantasia) for emp in empresas]

    form = EventoForm()

    form.estilo.choices = lista_estilo

    form.empresa.choices = lista_empresa

    if request.method == 'POST':

        if request.files:

            img = request.files["image"]
            name_img = img.filename

            evento = Evento(nomeevento=form.nome.data,
                            data_inicio=form.data_inicio.data,
                            hora_inicio=form.hora_inicio.data,
                            hora_final=form.hora_final.data,
                            descricao=form.descricao.data,
                            est_id=form.estilo.data,
                            cnpj_emp=form.empresa.data,
                            image=name_img,
                            func_id=session['id'])
            try:
                db.session.add(evento)
                db.session.commit()

                print(name_img)
                img.save(os.path.join(os.path.abspath('D:/OneDrive/Faculdade/8P/TCCpy/DigIngressoPy/app/static/img'),
                                      name_img))

                flash('Evento salvo com sucesso, Deseja realizar outro cadastro?', 'func.cad_evt')

            except:
                # Error
                flash('Erro ao cadastrar o evento', 'warning')

            return redirect(url_for('func.dashboard'))

    return render_template('func/evento/evento.html', action='Cad',
                           add_evt=add_evt, form=form, title='Cadastrar Evento')


@func.route('/evento/pesquisar', methods=['GET', 'POST'])
@login_required
def pesquisar_evt():
    """"
        Pesquisar Evento
    """

    check_func()

    evts = False

    if request.method == 'POST':

        pesq = request.form['pesq_evt']

        evts = Evento.query.filter(Evento.nomeevento.like(pesq+'%'),
                                   Evento.estado == 0).all()

        return render_template('func/evento/pesqevento.html',
                               evts=evts, title='Eventos', date= datetime)

    return render_template('func/evento/pesqevento.html',
                           evts=evts, title='Eventos')


@func.route('/evento/alterar/<int:id>', methods=['GET', 'POST'])
@login_required
def alterar_evt(id):
    """"
        Alterar Evento
    """

    check_func()

    add_evt = False

    estilos = EstiloMusical.query.all()
    lista_estilo = [(est.id, est.nome) for est in estilos]

    empresas = Empresa.query.all()
    lista_empresa = [(emp.cnpj, emp.nomefantasia) for emp in empresas]

    evt = Evento.query.get_or_404(id)

    form = EventoForm()

    if request.method == 'POST':

        evt.nomeevento = form.nome.data
        evt.data_inicio = form.data_inicio.data
        evt.hora_inicio = form.hora_inicio.data
        evt.hora_final = form.hora_final.data
        evt.descricao = form.descricao.data
        evt.est_id = form.estilo.data
        evt.cnpj_emp = form.empresa.data
        evt.func_id = session['id']

        db.session.commit()

        flash('Você alterou o Evento com sucesso', 'alterar')

        return redirect(url_for('func.pesquisar_evt'))

    form.nome.data = evt.nomeevento
    form.data_inicio.data = datetime.strftime(evt.data_inicio, '%d/%m/%Y')
    form.hora_inicio.data = evt.hora_inicio
    form.hora_final.data = evt.hora_final
    form.descricao.data = evt.descricao

    form.estilo.choices = lista_estilo
    form.estilo.data = evt.est_id

    form.empresa.choices = lista_empresa
    form.empresa.data = evt.cnpj_emp

    return render_template('func/evento/evento.html', action='Alt',
                           add_evt=add_evt, form=form, title='Alterar Evento')


@func.route('/evento/deletar/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_evt(id):
    """
        Deletar/Desativar Evento
    """

    check_func()

    evt = Evento.query.get_or_404(id)

    evt.estado = 1

    db.session.commit()

    flash('Evento excluida com sucesso!', 'success')

    # Redireciona para o Pesquisar
    return redirect(url_for('func.pesquisar_evt'))


@func.route('/relatorio/estilomusical')
@login_required
def rela_est():
    """
     Mostra relatório de estilo musicais
    """
    check_func()

    check_admin()

    res = db.engine.execute('select em.nome, count(em.id) as qtd from compra c '
                            'join evento e on c.evt_id = e.id '
                            'join estilomusical em on e.est_id = em.id '
                            'group by em.nome '
                            'order by qtd '
                            'limit 10 ')

    ests = []
    qtds = []
    for row in res:
        ests.append(row[0])
        qtds.append(row[1])

    return render_template('func/relatorio/relatorio_estilo.html', title='Relatório Estilo Musical',
                           ests=json.dumps(ests), qtds=qtds)


@func.route('/relatorio/venda', methods=['GET', 'POST'])
@login_required
def rela_venda():
    """
     Mostra relatório de venda
    """
    check_func()

    check_admin()

    pesq = False

    empresas = Empresa.query.filter(Empresa.estado == 0).order_by(Empresa.nomefantasia).all()
    lista_empresa = [(emp.cnpj, emp.nomefantasia) for emp in empresas]

    form = RelatorioForm()

    form.empresa.choices = lista_empresa

    if request.method == 'POST':
        pesq = True

        cnpj = form.empresa.data

        empresa = Empresa.query.filter(Empresa.cnpj == cnpj).first()

        nome_emp = empresa.nomefantasia

        sql = 'select sum(c.valor_total) as Total, e.nomeevento from compra c ' \
              'join evento e on c.evt_id = e.id ' \
              'join empresa em on e.cnpj_emp = em.cnpj ' \
              'where em.cnpj = "%s" ' \
              'group by e.nomeevento ' \
              'order by Total ' \
              'limit 10' % cnpj

        emp = db.engine.execute(sql)

        evt = []
        total = []
        for row in emp:
            evt.append(row[1])
            total.append(float(row[0]))

        return render_template('func/relatorio/relatorio_venda.html', title='Relatório de Venda',
                               form=form, pesq=pesq, evt=json.dumps(evt), total=json.dumps(total), nome=nome_emp)

    return render_template('func/relatorio/relatorio_venda.html', title='Relatório de Venda',
                           form=form, pesq=pesq)