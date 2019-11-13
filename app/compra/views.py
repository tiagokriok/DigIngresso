from flask import render_template, request, session,abort, redirect, url_for
from flask_login import login_required
from ..models import ItensCompra, Compra, TipoIngresso, Cliente, Evento
from datetime import datetime, time
from .. import db
from . import compra

from datetime import datetime


def check_cli():

    if not session['Cli']:
        abort(403)


@compra.route('/finalizarcompra', methods=['GET', 'POST'])
@login_required
def finalizar_compra():
    """Finalizar a Compra"""

    check_cli()

    return render_template('compra/finalizarcompra.html', title='Finalizar Compra')


@compra.route('/realizarcompra', methods=['GET','POST'])
@login_required
def realizar_compra():
    """Realizar Compra e Salvar no BD"""

    check_cli()

    if request.is_json and request.method == 'POST':
        carrinho = request.get_json()

        compra = Compra(valor_total=float(carrinho['Total']), data_compra=datetime.now()
                        , evt_id=int(carrinho['Evento']), cpf_cli=session['CPF'])

        db.session.add(compra)
        db.session.commit()

        for item in carrinho:
            if item != 'Total' and item != 'Evento':
                tid = int(item)
                itens = ItensCompra(qtd=carrinho[item]['qtd'], compra_id=compra.id,
                                    tipo_id=tid)

                tipo = TipoIngresso.query.get(tid)
                tipo.lote = int(tipo.lote) - int(carrinho[item]['qtd'])

                db.session.add(itens)
                db.session.commit()

        return 200

    return redirect(url_for('compra.compra_sucesso'))


@compra.route('/ingresso/<path:cpf>')
@login_required
def compra_sucesso(cpf):
    """Mostra ingresso"""

    check_cli()

    # cpf = session['CPF']

    cliente = Cliente.query.filter(Cliente.cpf == cpf).first()

    com = Compra.query.filter(Compra.cpf_cli == cpf).order_by(Compra.id.desc()).first()

    evt = Evento.query.get_or_404(com.evt_id)

    ing = ItensCompra.query.join(TipoIngresso, ItensCompra.tipo_id==TipoIngresso.id).add_columns(ItensCompra.qtd, TipoIngresso.nome).filter(ItensCompra.compra_id == com.id).all()

    return render_template('compra/sucesso.html', title='Compra Realizada com Sucesso',
                           cli=cliente, com=com, evt=evt, ing=ing, date=datetime, time=time)
