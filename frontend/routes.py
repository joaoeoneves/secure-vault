from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from forms import (
    LoginForm, RegistrationForm,
    SelectEntryTypeForm,
    PasswordEntryForm, CreditCardEntryForm,
    SSHKeyEntryForm, NoteEntryForm
)
from api.utilizador_api import UtilizadorApi
from api.vault_api import VaultApi

blueprint = Blueprint('frontend', __name__)

@blueprint.route('/')
def home():
    return redirect(url_for('frontend.login'))

@blueprint.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        api_key = UtilizadorApi.login(form)
        if api_key:
            session['api_key'] = api_key
            session['nomeUtilizador'] = form.nomeUtilizador.data
            flash('Login efetuado com sucesso.')
            return redirect(url_for('frontend.dashboard'))
        flash('Credenciais inválidas.')
    return render_template('login.html', form=form)

@blueprint.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if UtilizadorApi.existe(form.nomeUtilizador.data):
            flash('Nome de utilizador já existe.')
        else:
            user = UtilizadorApi.criar_Utilizador(form)
            if user:
                flash('Registo efetuado. Faça login.')
                return redirect(url_for('frontend.login'))
    return render_template('register.html', form=form)

@blueprint.route('/dashboard')
def dashboard():
    if 'api_key' not in session:
        flash('Faça login primeiro.')
        return redirect(url_for('frontend.login'))
    return render_template('dashboard.html', nome=session.get('nomeUtilizador'))

@blueprint.route('/logout')
def logout():
    session.clear()
    flash('Sessão terminada.')
    return redirect(url_for('frontend.login'))

@blueprint.route('/vault')
def vault():
    if 'api_key' not in session:
        flash('Faça login primeiro.')
        return redirect(url_for('frontend.login'))
    entries = VaultApi.get_entries(session['api_key'])
    return render_template('vault_list.html', entries=entries)

@blueprint.route('/vault/add', methods=['GET','POST'])
def vault_select():
    form = SelectEntryTypeForm()
    if form.validate_on_submit():
        return redirect(url_for('frontend.vault_add', entry_type=form.entry_type.data))
    return render_template('vault_select_type.html', form=form)

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

@blueprint.route('/vault/delete/<int:entry_id>', methods=['POST'])
def vault_delete(entry_id):
    if VaultApi.delete_entry(session['api_key'], entry_id):
        flash('Entrada apagada.')
    else:
        flash('Erro ao apagar.')
    return redirect(url_for('frontend.vault'))
