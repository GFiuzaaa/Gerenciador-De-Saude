from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from app.models.user_model import UserModel
from app.models.health_model import IMCModel, RefeicaoModel

health_bp = Blueprint('health', __name__, url_prefix='/saude')

@health_bp.route('/calcular-imc', methods=['POST'])
def calcular_imc():
    email = session.get('usuario_logado')
    usuario = UserModel.query_filter_by_email(email)

    if not usuario:
        flash('Sessão inválida. Faça login novamente.', 'danger')
        return redirect(url_for('auth.login'))

    try:
        peso = float(request.form.get('peso'))
        altura = float(request.form.get('altura'))

        if peso <= 0 or altura <= 0:
            flash('Informe valores válidos para peso e altura.', 'danger')
            return redirect(url_for('auth.dashboard'))

        # Cálculo do IMC: Peso / (Altura * Altura)
        imc_valor = round(peso / (altura ** 2), 2)
        classificacao = IMCModel.calcular_classificacao(imc_valor)

        # Salva o cálculo no banco
        registo = IMCModel(
            usuario_id=usuario.id,
            peso=peso,
            altura=altura,
            imc=imc_valor,
            classificacao=classificacao
        )
        registo.salvar()

        flash(f'IMC calculado com sucesso: {imc_valor} ({classificacao})', 'success')
    except (ValueError, TypeError):
        flash('Por favor, insira números válidos.', 'danger')

    return redirect(url_for('auth.dashboard'))


@health_bp.route('/criar-refeicao', methods=['POST'])
def criar_refeicao():
    email = session.get('usuario_logado')
    usuario = UserModel.query_filter_by_email(email)

    if not usuario:
        flash('Sessão inválida. Faça login novamente.', 'danger')
        return redirect(url_for('auth.login'))

    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao', '')
    calorias = request.form.get('calorias', 0)

    if not titulo:
        flash('O título da refeição é obrigatório.', 'danger')
        return redirect(url_for('auth.dashboard'))

    try:
        calorias_val = float(calorias) if calorias else 0.0
    except ValueError:
        calorias_val = 0.0

    refeicao = RefeicaoModel(
        usuario_id=usuario.id,
        titulo=titulo,
        descricao=descricao,
        calorias=calorias_val
    )
    refeicao.salvar()

    flash('Refeição/Rotina cadastrada com sucesso!', 'success')
    return redirect(url_for('auth.dashboard'))