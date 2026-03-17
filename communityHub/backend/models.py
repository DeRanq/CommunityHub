from . import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id           = db.Column(db.Integer, primary_key=True)
    username     = db.Column(db.String(80),  unique=True, nullable=False)
    email        = db.Column(db.String(120), unique=True, nullable=False)
    password     = db.Column(db.String(200), nullable=False)
    erstellt_am  = db.Column(db.DateTime, default=datetime.utcnow)

    beitraege    = db.relationship('Beitrag',    backref='autor', lazy=True, cascade='all, delete-orphan')
    kommentare   = db.relationship('Kommentar',  backref='autor', lazy=True, cascade='all, delete-orphan')
    dateien      = db.relationship('ArchivDatei',backref='autor', lazy=True, cascade='all, delete-orphan')
    links        = db.relationship('ArchivLink', backref='autor', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'


class Beitrag(db.Model):
    __tablename__ = 'beitrag'

    id           = db.Column(db.Integer, primary_key=True)
    titel        = db.Column(db.String(200), nullable=False)
    inhalt       = db.Column(db.Text,        nullable=False)
    kategorie    = db.Column(db.String(50),  nullable=False, default='Allgemein')
    erstellt_am  = db.Column(db.DateTime, default=datetime.utcnow)
    user_id      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    kommentare   = db.relationship('Kommentar', backref='beitrag', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Beitrag {self.titel}>'


class Kommentar(db.Model):
    __tablename__ = 'kommentar'

    id           = db.Column(db.Integer, primary_key=True)
    inhalt       = db.Column(db.Text, nullable=False)
    erstellt_am  = db.Column(db.DateTime, default=datetime.utcnow)
    user_id      = db.Column(db.Integer, db.ForeignKey('user.id'),    nullable=False)
    beitrag_id   = db.Column(db.Integer, db.ForeignKey('beitrag.id'), nullable=False)

    def __repr__(self):
        return f'<Kommentar {self.id}>'


class ArchivDatei(db.Model):
    __tablename__ = 'archiv_datei'

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(200), nullable=False)
    originaldatei   = db.Column(db.String(200), nullable=False)
    dateipfad       = db.Column(db.String(300), nullable=False)
    beschreibung    = db.Column(db.Text)
    hochgeladen_am  = db.Column(db.DateTime, default=datetime.utcnow)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<ArchivDatei {self.name}>'


class ArchivLink(db.Model):
    __tablename__ = 'archiv_link'

    id           = db.Column(db.Integer, primary_key=True)
    titel        = db.Column(db.String(200), nullable=False)
    url          = db.Column(db.String(500), nullable=False)
    beschreibung = db.Column(db.Text)
    gespeichert_am = db.Column(db.DateTime, default=datetime.utcnow)
    user_id      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<ArchivLink {self.titel}>'
