import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from admin_backend_service.db import get_db

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/register', methods=("POST",))
def register():
        body_as_json = request.get_json(force=True)
        ['username']
        email=body_as_json['email']
        firstname = body_as_json['firstname']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not firstname:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, firstname)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)


