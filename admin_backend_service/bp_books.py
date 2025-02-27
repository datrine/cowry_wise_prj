import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from admin_backend_service.db import get_db

bp = Blueprint('books', __name__, url_prefix='/books')

