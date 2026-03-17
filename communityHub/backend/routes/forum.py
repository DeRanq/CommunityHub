from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .. import db
from ..models import Beitrag, Kommentar

forum_bp = Blueprint('forum', __name__, url_prefix='/forum')

KATEGORIEN = ['Allgemein', 'Ankündigungen', 'Fragen', 'Projekte', 'Offtopic']


@forum_bp.route('/')
@login_required
def uebersicht():
    kategorie = request.args.get('kategorie', '')
    if kategorie and kategorie in KATEGORIEN:
        beitraege = Beitrag.query.filter_by(kategorie=kategorie)\
                          .order_by(Beitrag.erstellt_am.desc()).all()
    else:
        beitraege = Beitrag.query.order_by(Beitrag.erstellt_am.desc()).all()

    return render_template('forum/uebersicht.html',
                           beitraege=beitraege,
                           kategorien=KATEGORIEN,
                           aktive_kategorie=kategorie)


@forum_bp.route('/neu', methods=['GET', 'POST'])
@login_required
def neu():
    if request.method == 'POST':
        titel     = request.form.get('titel', '').strip()
        inhalt    = request.form.get('inhalt', '').strip()
        kategorie = request.form.get('kategorie', 'Allgemein')

        if not titel or not inhalt:
            flash('Titel und Inhalt sind Pflichtfelder.', 'danger')
        else:
            beitrag = Beitrag(
                titel=titel,
                inhalt=inhalt,
                kategorie=kategorie,
                user_id=current_user.id
            )
            db.session.add(beitrag)
            db.session.commit()
            flash('Beitrag erfolgreich erstellt!', 'success')
            return redirect(url_for('forum.detail', beitrag_id=beitrag.id))

    return render_template('forum/neu.html', kategorien=KATEGORIEN)


@forum_bp.route('/<int:beitrag_id>')
@login_required
def detail(beitrag_id):
    beitrag = Beitrag.query.get_or_404(beitrag_id)
    return render_template('forum/detail.html', beitrag=beitrag)


@forum_bp.route('/<int:beitrag_id>/bearbeiten', methods=['GET', 'POST'])
@login_required
def bearbeiten(beitrag_id):
    beitrag = Beitrag.query.get_or_404(beitrag_id)

    if beitrag.user_id != current_user.id:
        flash('Du kannst nur deine eigenen Beiträge bearbeiten.', 'danger')
        return redirect(url_for('forum.detail', beitrag_id=beitrag_id))

    if request.method == 'POST':
        beitrag.titel     = request.form.get('titel', '').strip()
        beitrag.inhalt    = request.form.get('inhalt', '').strip()
        beitrag.kategorie = request.form.get('kategorie', 'Allgemein')

        if not beitrag.titel or not beitrag.inhalt:
            flash('Titel und Inhalt sind Pflichtfelder.', 'danger')
        else:
            db.session.commit()
            flash('Beitrag aktualisiert!', 'success')
            return redirect(url_for('forum.detail', beitrag_id=beitrag_id))

    return render_template('forum/bearbeiten.html', beitrag=beitrag, kategorien=KATEGORIEN)


@forum_bp.route('/<int:beitrag_id>/loeschen', methods=['POST'])
@login_required
def loeschen(beitrag_id):
    beitrag = Beitrag.query.get_or_404(beitrag_id)

    if beitrag.user_id != current_user.id:
        flash('Keine Berechtigung.', 'danger')
        return redirect(url_for('forum.uebersicht'))

    db.session.delete(beitrag)
    db.session.commit()
    flash('Beitrag gelöscht.', 'info')
    return redirect(url_for('forum.uebersicht'))


@forum_bp.route('/<int:beitrag_id>/kommentar', methods=['POST'])
@login_required
def kommentar(beitrag_id):
    beitrag = Beitrag.query.get_or_404(beitrag_id)
    inhalt  = request.form.get('inhalt', '').strip()

    if not inhalt:
        flash('Kommentar darf nicht leer sein.', 'danger')
    else:
        k = Kommentar(inhalt=inhalt, user_id=current_user.id, beitrag_id=beitrag.id)
        db.session.add(k)
        db.session.commit()
        flash('Kommentar hinzugefügt!', 'success')

    return redirect(url_for('forum.detail', beitrag_id=beitrag_id))


@forum_bp.route('/kommentar/<int:kommentar_id>/loeschen', methods=['POST'])
@login_required
def kommentar_loeschen(kommentar_id):
    k = Kommentar.query.get_or_404(kommentar_id)

    if k.user_id != current_user.id:
        flash('Keine Berechtigung.', 'danger')
    else:
        beitrag_id = k.beitrag_id
        db.session.delete(k)
        db.session.commit()
        flash('Kommentar gelöscht.', 'info')
        return redirect(url_for('forum.detail', beitrag_id=beitrag_id))

    return redirect(url_for('forum.uebersicht'))
