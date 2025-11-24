# app/auth/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from datetime import datetime

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if not email or not password:
            flash("Email e senha são obrigatórios.", "error")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Credenciais inválidas.", "error")
            return redirect(url_for("auth.login"))

        login_user(user)
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("main.home"))

    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        password2 = request.form.get("password2") or ""

        birthdate_raw = request.form.get("birthdate")
        gender = request.form.get("gender")
        gender_other = request.form.get("gender_other") or None

        # "Outro" vira o texto digitado
        if gender == "Outro" and gender_other:
            gender = gender_other

        # Converter data
        birthdate = None
        if birthdate_raw:
            try:
                birthdate = datetime.strptime(birthdate_raw, "%Y-%m-%d").date()
            except ValueError:
                flash("Data de nascimento inválida.", "error")
                return redirect(url_for("auth.register"))

        # Validações
        if not name or not email or not password:
            flash("Nome, email e senha são obrigatórios.", "error")
            return redirect(url_for("auth.register"))

        if password != password2:
            flash("As senhas não coincidem.", "error")
            return redirect(url_for("auth.register"))

        if not birthdate:
            flash("Data de nascimento é obrigatória.", "error")
            return redirect(url_for("auth.register"))

        if not gender:
            flash("Selecione um gênero.", "error")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Já existe conta com esse email.", "error")
            return redirect(url_for("auth.register"))

        # Criar usuário
        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            birthdate=birthdate,
            gender=gender
        )

        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Conta criada com sucesso!", "success")
        return redirect(url_for("main.home"))

    return render_template("register.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("main.home"))
