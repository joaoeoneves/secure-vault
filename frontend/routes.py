from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from forms import (
    LoginForm, RegistrationForm,
    SelectEntryTypeForm,
    PasswordEntryForm, CreditCardEntryForm,
    SSHKeyEntryForm, NoteEntryForm
)
from api.utilizador_api import UtilizadorApi
from api.vault_api import VaultApi

# Blueprint para agrupar todas as rotas do frontend.
blueprint = Blueprint('frontend', __name__)

# Página inicial redireciona para login.
@blueprint.route('/')
def home():
    return redirect(url_for('frontend.login'))

# Página de login. Autentica o utilizador via API.
@blueprint.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        api_key = UtilizadorApi.login(form)
        if api_key:
            session['api_key'] = api_key
            session['nomeUtilizador'] = form.nomeUtilizador.data
            flash('Login efetuado com sucesso.', 'success')
            return redirect(url_for('frontend.dashboard'))
        flash('Credenciais inválidas.', 'danger')
    return render_template('login.html', form=form)

# Página de registo de novo utilizador.
@blueprint.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if UtilizadorApi.existe(form.nomeUtilizador.data):
            flash('Nome de utilizador já existe.', 'warning')
        else:
            user = UtilizadorApi.criar_Utilizador(form)
            if user:
                flash('Registo efetuado. Faça login.', 'success')
                return redirect(url_for('frontend.login'))
            flash('Erro no registo.', 'danger')
    return render_template('register.html', form=form)

# Dashboard do utilizador autenticado.
@blueprint.route('/dashboard')
def dashboard():
    if 'api_key' not in session:
        flash('Faça login primeiro.', 'warning')
        return redirect(url_for('frontend.login'))
    return render_template('dashboard.html', nome=session.get('nomeUtilizador'))

# Logout limpa a sessão.
@blueprint.route('/logout')
def logout():
    session.clear()
    flash('Sessão terminada.', 'info')
    return redirect(url_for('frontend.login'))

# Lista de entradas do cofre (vault).
@blueprint.route('/vault')
def vault():
    if 'api_key' not in session:
        flash('Faça login primeiro.')
        return redirect(url_for('frontend.login'))
    entries = VaultApi.get_entries(session['api_key'])
    return render_template('vault_list.html', entries=entries)

# Seleção do tipo de entrada a adicionar ao cofre.
@blueprint.route('/vault/add', methods=['GET','POST'])
def vault_select():
    form = SelectEntryTypeForm()
    if form.validate_on_submit():
        return redirect(url_for('frontend.vault_add', entry_type=form.entry_type.data))
    return render_template('vault_select_type.html', form=form)

# Formulário para adicionar uma nova entrada ao cofre.
@blueprint.route('/vault/add/<entry_type>', methods=['GET','POST'])
def vault_add(entry_type):
    form_map = {
        'password': PasswordEntryForm,
        'credit_card': CreditCardEntryForm,
        'ssh_key': SSHKeyEntryForm,
        'note': NoteEntryForm
    }
    form_cls = form_map.get(entry_type)
    if not form_cls:
        flash('Tipo inválido.')
        return redirect(url_for('frontend.vault'))
    form = form_cls()
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k not in ('csrf_token','submit')}
        data['type'] = entry_type
        if VaultApi.create_entry(session['api_key'], data):
            flash('Entrada adicionada.')
            return redirect(url_for('frontend.vault'))
        flash('Erro ao adicionar.')
    return render_template('vault_add.html', form=form, entry_type=entry_type, edit=False)

# Formulário para editar uma entrada existente.
@blueprint.route('/vault/edit/<int:entry_id>', methods=['GET','POST'])
def vault_edit(entry_id):
    entries = VaultApi.get_entries(session['api_key'])
    entry = next((e for e in entries if e['id']==entry_id), None)
    if not entry:
        flash('Entrada não encontrada.')
        return redirect(url_for('frontend.vault'))
    form_map = {
        'password': PasswordEntryForm,
        'credit_card': CreditCardEntryForm,
        'ssh_key': SSHKeyEntryForm,
        'note': NoteEntryForm
    }
    form = form_map[entry['type']](data=entry)
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k not in ('csrf_token','submit')}
        data['type'] = entry['type']
        if VaultApi.update_entry(session['api_key'], entry_id, data):
            flash('Entrada atualizada.')
            return redirect(url_for('frontend.vault'))
        flash('Erro ao atualizar.')
    return render_template('vault_add.html', form=form, entry_type=entry['type'], edit=True)

# Apagar uma entrada do cofre.
@blueprint.route('/vault/delete/<int:entry_id>', methods=['POST'])
def vault_delete(entry_id):
    if VaultApi.delete_entry(session['api_key'], entry_id):
        flash('Entrada apagada.')
    else:
        flash('Erro ao apagar.')
    return redirect(url_for('frontend.vault'))

# Proxy para avaliar a saúde de uma entrada (chama API do vault).
@blueprint.route('/proxy/vault/entries/<int:entry_id>/health')
def proxy_vault_health(entry_id):
    api_key = session.get("api_key")
    if not api_key:
        return {"status": "error", "reason": "Não autenticado"}, 401

    from api.vault_api import VaultApi
    return VaultApi.get_health(api_key, entry_id), 200
