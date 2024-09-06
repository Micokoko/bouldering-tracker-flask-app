from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from bouldering_app.db import get_db
from .auth import login_required

bp = Blueprint('log_ascent', __name__, url_prefix='/climber')


@bp.route('/<int:boulder_id>/log_ascent', methods=('GET', 'POST'))
@login_required
def log_ascent_user(boulder_id):
    pass