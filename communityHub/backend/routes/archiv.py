import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .. import db
from ..models import ArchivDatei, ArchivLink

archiv_bp = Blueprint('archiv', __name__, url_prefix='/archiv')

ERLAUBTE_ENDUNGEN = {'pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg', 'xlsx', 'pptx'}


def erlaubte_datei(dateiname):
    return '.' in dateiname and dateiname.rsplit('.', 1)[1].lower() in ERLAUBTE_ENDUNGEN


@archiv_bp.route('/')
@login_required
def uebersicht():
    dateien = ArchivDatei.query.order_by(ArchivDatei.hochgeladen_am.desc()).all()
    links   = ArchivLink.query.order_by(ArchivLink.gespeichert_am.desc()).all()
    return render_template('archiv/uebersicht.html', dateien=dateien, links=links)


@archiv_bp.route('/datei/hochladen', methods=['GET', 'POST'])
@login_required
def datei_hochladen():
    if request.method == 'POST':
        name         = request.form.get('name', '').strip()
        beschreibung = request.form.get('beschreibung', '').strip()
        datei        = request.files.get('datei')

        if not name or not datei or datei.filename == '':
            flash('Name und Datei sind Pflichtfelder.', 'danger')
        elif not erlaubte_datei(datei.filename):
            flash(f'Dateityp nicht erlaubt. Erlaubt: {", ".join(ERLAUBTE_ENDUNGEN)}', 'danger')
        else:
            sicherer_name = secure_filename(datei.filename)
            eindeutiger_name = f'{uuid.uuid4().hex}_{sicherer_name}'
            pfad = os.path.join(current_app.config['UPLOAD_FOLDER'], eindeutiger_name)
            datei.save(pfad)

            archiv_datei = ArchivDatei(
                name=name,
                originaldatei=sicherer_name,
                dateipfad=eindeutiger_name,
                beschreibung=beschreibung,
                user_id=current_user.id
            )
            db.session.add(archiv_datei)
            db.session.commit()
            flash('Datei erfolgreich hochgeladen!', 'success')
            return redirect(url_for('archiv.uebersicht'))

    return render_template('archiv/datei_hochladen.html')


@archiv_bp.route('/datei/<int:datei_id>/download')
@login_required
def datei_download(datei_id):
    datei = ArchivDatei.query.get_or_404(datei_id)
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        datei.dateipfad,
        as_attachment=True,
        download_name=datei.originaldatei
    )


@archiv_bp.route('/datei/<int:datei_id>/loeschen', methods=['POST'])
@login_required
def datei_loeschen(datei_id):
    datei = ArchivDatei.query.get_or_404(datei_id)

    if datei.user_id != current_user.id:
        flash('Keine Berechtigung.', 'danger')
        return redirect(url_for('archiv.uebersicht'))

    pfad = os.path.join(current_app.config['UPLOAD_FOLDER'], datei.dateipfad)
    if os.path.exists(pfad):
        os.remove(pfad)

    db.session.delete(datei)
    db.session.commit()
    flash('Datei gelöscht.', 'info')
    return redirect(url_for('archiv.uebersicht'))


@archiv_bp.route('/link/neu', methods=['GET', 'POST'])
@login_required
def link_neu():
    if request.method == 'POST':
        titel        = request.form.get('titel', '').strip()
        url          = request.form.get('url', '').strip()
        beschreibung = request.form.get('beschreibung', '').strip()

        if not titel or not url:
            flash('Titel und URL sind Pflichtfelder.', 'danger')
        else:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            link = ArchivLink(
                titel=titel,
                url=url,
                beschreibung=beschreibung,
                user_id=current_user.id
            )
            db.session.add(link)
            db.session.commit()
            flash('Link erfolgreich gespeichert!', 'success')
            return redirect(url_for('archiv.uebersicht'))

    return render_template('archiv/link_neu.html')


@archiv_bp.route('/link/<int:link_id>/loeschen', methods=['POST'])
@login_required
def link_loeschen(link_id):
    link = ArchivLink.query.get_or_404(link_id)

    if link.user_id != current_user.id:
        flash('Keine Berechtigung.', 'danger')
        return redirect(url_for('archiv.uebersicht'))

    db.session.delete(link)
    db.session.commit()
    flash('Link gelöscht.', 'info')
    return redirect(url_for('archiv.uebersicht'))
