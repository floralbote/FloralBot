# app/routes.py

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from app.decorators import admin_required
from app import db
from app.models import User, Floral, ChatHistory
from app.chatbot import generate_response
from datetime import datetime

main_bp = Blueprint("main", __name__)

# ================================
# PÁGINAS PÚBLICAS
# ================================


@main_bp.route("/")
def home():
    return render_template("home.html")


@main_bp.route("/testetemplate")
def testetemplate():
    return render_template("chatbot.html")


@main_bp.route("/florais")
def florais_public():
    return render_template("florais_public.html")

# ================================
# DASHBOARD ADMIN
# ================================


@main_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_chats = ChatHistory.query.count()
    total_florais = Floral.query.count()

    users = User.query.order_by(User.created_at.desc()).all()
    chats = ChatHistory.query.order_by(
        ChatHistory.created_at.desc()).limit(20).all()
    florais = Floral.query.all()

    return render_template(
        "dashboard.html",
        total_users=total_users,
        total_chats=total_chats,
        total_florais=total_florais,
        users=users,
        chats=chats,
        florais=florais
    )

# ================================
# USUÁRIOS ADMIN
# ================================


@main_bp.route("/users-admin")
@login_required
@admin_required
def users_admin():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("users_admin.html", users=users)


@main_bp.route("/users-admin/add", methods=["GET"])
@login_required
@admin_required
def add_user_form():
    return render_template("add_user.html")


@main_bp.route("/users-admin/add", methods=["POST"])
@login_required
@admin_required
def add_user():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    gender = request.form.get("gender", "")
    birthdate_str = request.form.get("birthdate", "")

    birthdate = None
    if birthdate_str:
        try:
            birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
        except:
            birthdate = None

    is_admin = request.form.get("is_admin") == "on"
    hashed_pw = generate_password_hash(password)

    new_user = User(
        name=name,
        email=email,
        password_hash=hashed_pw,
        gender=gender,
        birthdate=birthdate,
        is_admin=is_admin
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("main.users_admin"))


@main_bp.route("/users-admin/edit/<int:user_id>", methods=["GET"])
@login_required
@admin_required
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@main_bp.route("/users-admin/edit/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    user.name = request.form.get("name", user.name)
    user.email = request.form.get("email", user.email)
    user.gender = request.form.get("gender", user.gender)

    birthdate_str = request.form.get("birthdate", "")
    if birthdate_str:
        try:
            user.birthdate = datetime.strptime(
                birthdate_str, "%Y-%m-%d").date()
        except:
            user.birthdate = None

    user.is_admin = request.form.get("is_admin") == "on"

    new_pw = request.form.get("password", "").strip()
    if new_pw:
        user.password_hash = generate_password_hash(new_pw)

    db.session.commit()
    return redirect(url_for("main.users_admin"))


@main_bp.route("/users-admin/delete/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        return jsonify({"error": "Você não pode excluir a si mesmo!"}), 400

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("main.users_admin"))

# ================================
# CRUD FLORAIS ADMIN
# ================================


@main_bp.route("/florais-admin")
@login_required
@admin_required
def florais_admin():
    florais = Floral.query.order_by(Floral.name.asc()).all()
    return render_template("florais.html", florais=florais)


@main_bp.route("/florais-admin/add", methods=["GET"])
@login_required
@admin_required
def florais_add_form():
    return render_template("add_floral.html")


@main_bp.route("/florais-admin/add", methods=["POST"])
@login_required
@admin_required
def florais_add():
    name = request.form.get("name")
    description = request.form.get("description", "")
    indications = request.form.get("indications", "")

    if not name:
        return jsonify({"error": "Nome obrigatório"}), 400

    floral = Floral(name=name, description=description,
                    indications=indications)
    db.session.add(floral)
    db.session.commit()

    return redirect(url_for("main.florais_admin"))


@main_bp.route("/florais-admin/edit/<int:floral_id>", methods=["GET"])
@login_required
@admin_required
def edit_floral_form(floral_id):
    floral = Floral.query.get_or_404(floral_id)
    return render_template("edit_floral.html", floral=floral)


@main_bp.route("/florais-admin/edit/<int:floral_id>", methods=["POST"])
@login_required
@admin_required
def florais_edit(floral_id):
    floral = Floral.query.get_or_404(floral_id)

    floral.name = request.form.get("name", floral.name)
    floral.description = request.form.get("description", floral.description)
    floral.indications = request.form.get("indications", floral.indications)

    db.session.commit()
    return redirect(url_for("main.florais_admin"))


@main_bp.route("/florais-admin/delete/<int:floral_id>", methods=["POST"])
@login_required
@admin_required
def florais_delete(floral_id):
    floral = Floral.query.get_or_404(floral_id)
    db.session.delete(floral)
    db.session.commit()
    return redirect(url_for("main.florais_admin"))


# ================================
# API FLORAIS
# ================================

@main_bp.route("/api/florais", methods=["GET"])
def get_florais():
    florais = Floral.query.all()
    return jsonify([
        {
            "id": f.id,
            "name": f.name,
            "description": f.description,
            "indications": f.indications
        }
        for f in florais
    ])

# ================================
# CHATBOT — Página do chat
# ================================


@main_bp.route("/chat", methods=["GET"])
def chat_page():
    return render_template("chatbot.html")


# ================================
# CHATBOT — IA + CONTROLE DE TURNOS
# ================================

@main_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Mensagem vazia."}), 400

    # Usuário logado ou visitante
    user_id = current_user.id if current_user.is_authenticated else None

    # Carregar histórico
    history = ChatHistory.query.filter_by(user_id=user_id).order_by(
        ChatHistory.created_at.asc()).all()

    contexto_conversa = ""
    num_user_messages = 0  # contador para as 3 perguntas

    # Detectar quando reiniciar ciclo
    ciclo_finalizado = False

    for h in history:
        if h.user_message:
            msg = h.user_message.lower()

            # Detecta encerramento do ciclo anterior
            if any(x in msg for x in ["não", "nao", "obrigado", "obrigada", "tchau"]):
                ciclo_finalizado = True
                num_user_messages = 0
            else:
                num_user_messages += 1

            contexto_conversa += f"Usuário: {h.user_message}\n"

        if h.bot_message:
            contexto_conversa += f"FloralBot: {h.bot_message}\n"

    # Limitar o contador a no máximo 4
    # 1, 2, 3 → perguntas
    # 4 → fase de recomendar florais
    if num_user_messages > 4:
        num_user_messages = 4

    # Trazer florais do banco
    florais = Floral.query.all()
    contexto_florais = "\n".join(
        f"{f.name}: {f.indications or ''}" for f in florais
    )

    # Construir contexto total
    contexto_total = f"{contexto_conversa}\n\nFLORAIS DISPONÍVEIS:\n{contexto_florais}"

    # Gerar resposta
    try:
        bot_response = generate_response(
            user_message,
            context=contexto_total,
            num_user_messages=num_user_messages
        )
    except Exception:
        bot_response = "Desculpe, ocorreu um erro ao gerar a resposta."

    # Salvar conversa
    chat = ChatHistory(
        user_id=user_id,
        user_message=user_message,
        bot_message=bot_response
    )
    db.session.add(chat)
    db.session.commit()

    # Resposta JSON
    return jsonify({"response": bot_response})
