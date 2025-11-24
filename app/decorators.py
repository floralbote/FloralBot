# app/decorators.py
from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Você precisa estar logado.", "error")
            return redirect(url_for("auth.login"))

        if not current_user.is_admin:
            flash(
                "Acesso negado. Apenas administradores podem acessar esta página.", "error")
            return redirect(url_for("main.home"))

        return f(*args, **kwargs)
    return decorated_function
