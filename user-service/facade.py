from models import db, Utilizador

# Classe Facade que centraliza a lógica de negócio dos utilizadores.
# Permite que as rotas interajam com os utilizadores de forma simples,
# escondendo a complexidade do acesso à base de dados e regras de negócio.
class UtilizadorFacade:
    @staticmethod
    def criar_utilizador(nome, senha):
        # Verifica se já existe utilizador com este nome
        if Utilizador.query.filter_by(nomeUtilizador=nome).first():
            return None, "Utilizador já existe."
        user = Utilizador(nomeUtilizador=nome)
        user.set_password(senha)
        user.update_api_key()
        db.session.add(user)
        db.session.commit()
        return user, None

    @staticmethod
    def autenticar_utilizador(nome, senha):
        user = Utilizador.query.filter_by(nomeUtilizador=nome).first()
        # Verifica credenciais
        if not user or not user.check_password(senha):
            return None
        user.update_api_key()
        db.session.commit()
        return user

    @staticmethod
    def existe_utilizador(nome):
        return Utilizador.query.filter_by(nomeUtilizador=nome).first() is not None