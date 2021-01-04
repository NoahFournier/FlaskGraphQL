from .extensions import db

class CRUDMixin(object):
    
    @classmethod
    def create(cls, **kwargs):
        """Create new record and save it in db"""
        instance = cls(**kwargs)
        return instance.save()
    
    def update(self, commit=True, **kwargs):
        """Update fields of a record"""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self
    
    def save(self, commit=True):
        """Save the record"""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
    
    def delete(self, commit=True):
        """Delete the record"""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD methods"""

    __abstract__ = True


class PkModel(Model):
    """Base Model that includes CRUD methods, and PK column named `id`"""

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID"""
        if isinstance(record_id, (int, float, str)):
            return cls.query.get(int(record_id))
        return None


def reference_col(
    tablename, nullable=False, pk_name="id",
    foreign_key_kwargs=None, column_kwargs=None
):
    """Column that adds primary key foreign reference

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return db.Column(
        db.ForeignKey(f"{tablename}.{pk_name}",**foreign_key_kwargs),
        nullable=nullable,
        **column_kwargs,
    )
