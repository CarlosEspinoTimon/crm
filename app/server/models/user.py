from datetime import datetime

from server import db, ma


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(120), index=True, nullable=False)
    surname = db.Column(db.String(120), index=True, nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    modified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    password_hash = db.Column(db.String(128))
    is_deleted = db.Column(
        db.Boolean,
        index=True,
        nullable=False,
        default=False)


class UserSchema(ma.ModelSchema):

    class Meta:
        model = User
        include_fk = True
        exclude = ['password_hash']
