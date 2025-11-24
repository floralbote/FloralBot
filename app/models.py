# app/models.py
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# ============================================================
# TABELA DE USUÁRIOS
# ============================================================


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    password_hash = db.Column(db.String(256), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    birthdate = db.Column(db.Date)      # Data de nascimento
    gender = db.Column(db.String(50))   # Feminino / Masculino / Outro

    is_admin = db.Column(db.Boolean, default=False)  # Controle de acesso

    # Relacionamento com histórico do chat. -> apaga histórico automaticamente quando o usuário for apagado

    chats = db.relationship(
        "ChatHistory",
        backref="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # --------------------------
    # MÉTODOS DE SENHA
    # --------------------------

    def set_password(self, password):
        """Gera hash da senha"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Valida senha"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


# ============================================================
# TABELA DE FLORAIS
# ============================================================

class Floral(db.Model):
    __tablename__ = "florais"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    indications = db.Column(db.Text)

    def __repr__(self):
        return f"<Floral {self.name}>"

# ============================================================
# TABELA DE HISTÓRICO DO CHAT
# ============================================================


class ChatHistory(db.Model):
    __tablename__ = "chat_history"

    id = db.Column(db.Integer, primary_key=True)

    # FK precisa apontar para "user.id"
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)

    user_message = db.Column(db.Text, nullable=False)
    bot_message = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ChatHistory {self.id} user={self.user_id}>"
