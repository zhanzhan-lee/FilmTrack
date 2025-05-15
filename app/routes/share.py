from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Share, User
from flask import abort

share = Blueprint("share", __name__)

@share.route("/share", methods=["GET", "POST"])
@login_required
def share_page():
    if request.method == "POST":
        raw_username = request.form.get("share_users", "")
        username = raw_username.lstrip("@").strip()
        if username == current_user.username:
            flash("You cannot share with yourself.", "danger")
            return redirect(url_for("share.share_page"))

        recipient = User.query.filter_by(username=username).first()
        if not recipient:
            flash("Recipient not found.", "danger")
            return redirect(url_for("share.share_page"))

        try:
            start = datetime.fromisoformat(request.form["start_date"])
            end = datetime.fromisoformat(request.form["end_date"])
        except ValueError:
            flash("Invalid date.", "danger")
            return redirect(url_for("share.share_page"))

        note = request.form.get("message", "")
        flags = dict(
            share_exposure=bool(request.form.get("share_exposure")),
            share_aperture=bool(request.form.get("share_aperture")),
            share_favorite_film=bool(request.form.get("share_favorite_film")),
            share_gear=bool(request.form.get("share_gear")),
            share_shoot_time=bool(request.form.get("share_shoot_time"))
        )

        rec = Share.query.filter_by(
            from_user_id=current_user.id,
            to_user_id=recipient.id
        ).first()

        if rec:
            rec.start_date, rec.end_date, rec.note = start, end, note
            for k, v in flags.items():
                setattr(rec, k, v)
            flash("Share updated.", "success")
        else:
            rec = Share(
                from_user_id=current_user.id,
                to_user_id=recipient.id,
                start_date=start,
                end_date=end,
                note=note,
                **flags
            )
            db.session.add(rec)
            flash("Share created.", "success")

        db.session.commit()
        return redirect(url_for("share.share_page"))

    shares = Share.query.filter_by(
        from_user_id=current_user.id
    ).order_by(Share.created_at.desc()).all()
    return render_template("share.html", title="Share", shares=shares)

@share.route("/share/<int:share_id>/revoke", methods=["POST"])
@login_required
def revoke_share(share_id):
    rec = db.session.get(Share, share_id)
    if not rec:
        abort(404)
    if rec.from_user_id != current_user.id:
        flash("Not authorised.", "danger")
        return redirect(url_for("share.share_page"))
    db.session.delete(rec)
    db.session.commit()
    flash("Share revoked.", "success")
    return redirect(url_for("share.share_page"))





