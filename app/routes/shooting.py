# app/routes/shooting.py

from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required, current_user
from app.models import Roll, Film
from app.forms import RollForm
from app import db

shooting = Blueprint('shooting', __name__)

# --------------------------------------------
# 页面渲染：shooting 页面（初始加载）
# --------------------------------------------
@shooting.route('/shooting')
@login_required
def shooting_page():
    # 后续这里可以 preload 但我们预计 AJAX 加载即可
    return render_template(
        'shooting.html',
        roll_form=RollForm()  # 提供 modal 表单
    )

# --------------------------------------------
# 数据接口：返回当前用户所有 Roll（AJAX）
# --------------------------------------------
@shooting.route('/shooting/data/rolls')
@login_required
def get_roll_data():
    rolls = Roll.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            'id': roll.id,
            'roll_name': roll.roll_name,
            'film_id': roll.film_id,
            'film_name': f"{roll.film.brand} {roll.film.name}" if roll.film else None,
            'start_date': roll.start_date.strftime('%Y-%m-%d') if roll.start_date else None,
            'end_date': roll.end_date.strftime('%Y-%m-%d') if roll.end_date else None,
            'status': roll.status,
            'notes': roll.notes or ''
        }
        for roll in rolls
    ])


# -----------------------------
# 上传新 Roll（POST）
# -----------------------------
@shooting.route('/shooting/upload_roll', methods=['POST'])
@login_required
def upload_roll():
    form = RollForm()
    form.film_id.choices = [(f.id, f"{f.brand} {f.name}") for f in Film.query.filter_by(user_id=current_user.id)]
    
    if form.validate_on_submit():
        new_roll = Roll(
            user_id=current_user.id,
            film_id=form.film_id.data,
            roll_name=form.roll_name.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            status=form.status.data,
            notes=form.notes.data
        )
        db.session.add(new_roll)
        db.session.commit()
        return jsonify({'message': 'success'}), 200

    return jsonify({'message': 'form invalid', 'errors': form.errors}), 400


# -----------------------------
# 编辑 Roll（POST）
# -----------------------------
@shooting.route('/shooting/edit_roll/<int:id>', methods=['POST'])
@login_required
def edit_roll(id):
    roll = Roll.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = RollForm()
    form.film_id.choices = [(f.id, f"{f.brand} {f.name}") for f in Film.query.filter_by(user_id=current_user.id)]

    if form.validate_on_submit():
        roll.film_id = form.film_id.data
        roll.roll_name = form.roll_name.data
        roll.start_date = form.start_date.data
        roll.end_date = form.end_date.data
        roll.status = form.status.data
        roll.notes = form.notes.data
        db.session.commit()
        return jsonify({'message': 'updated'}), 200

    return jsonify({'message': 'form invalid', 'errors': form.errors}), 400


# -----------------------------
# 删除 Roll（DELETE）
# -----------------------------
@shooting.route('/shooting/delete_roll/<int:id>', methods=['DELETE'])
@login_required
def delete_roll(id):
    roll = Roll.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(roll)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200
