from flask import render_template
from datetime import datetime, time
from ..models import Evento, Empresa, TipoIngresso, Endereco
from . import home


@home.route('/')
def pagprincipal():
    """"
        Mostra a página principal
    """

    evts = Evento.query.filter(Evento.data_inicio == datetime.now().date(),
                               Evento.estado == 0).all()

    return render_template('home/index.html', title='Home', evts=evts, date=datetime)


@home.route('/eventos')
def eventos():
    """
        Mostra a página de Eventos
    """

    evts = Evento.query.filter(Evento.data_inicio >= datetime.now().date(), Evento.estado == 0).order_by(Evento.data_inicio).all()

    return render_template('home/eventos.html', title='Eventos',
                           evts=evts, date=datetime)


@home.route('/evento/<int:id>', methods=['GET', 'POST'])
def detalhe_evento(id):
    """
        Mostra detalhes do Evento
    """

    evt = Evento.query.get_or_404(id)

    emp = Empresa.query.get_or_404(evt.cnpj_emp)

    end = Endereco.query.get_or_404(emp.end_id)

    ting = TipoIngresso.query.filter(TipoIngresso.evt_id == id, TipoIngresso.lote > 0
                                     ).order_by(TipoIngresso.valor).all()

    return render_template('home/detalhe_evento.html', title=evt.nomeevento,
                           evt=evt, emp=emp, ting=ting, end=end, date=datetime, time=time)