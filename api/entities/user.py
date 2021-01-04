import datetime as dt
from flask_login import UserMixin
from api.database import PkModel, db, reference_col
from api.extensions import bcrypt

class Role(PkModel):

    __tablename__ = "roles"
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = db.relationship("User", backref="roles")

    def __init__(self, name, **kwargs):
        """Create instance"""
        super().__init__(name=name, **kwargs)
    
    def __repr__(self):
        """Represent instance as unique string."""
        return f"<Role({self.name})>"

class User(UserMixin, PkModel):
    """A user of the app."""

    __tablename__ = "users"
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.LargeBinary(128), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    is_admin = db.Column(db.Boolean(), default=False)

    def __init__(self, username, password=None, **kwargs):
        """Create instance"""
        super().__init__(username=username, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None
        
    def set_password(self, password):
        """Set password"""
        self.password = bcrypt.generate_password_hash(password)
    
    def check_password(self, value):
        """Check password"""
        return bcrypt.check_password_hash(self.password, value)
    
    def to_dict(self):
        """Return dictionary view"""
        return {
            "id": self.id,
            "username": self.username,
            "is_admin": self.is_admin
        }
    
    def __repr__(self):
        """Represent instance as unique string"""
        return f"<User({self.username!r})>"