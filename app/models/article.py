from app import db
from datetime import datetime, timezone

class Article(db.Model):
    """Model for articles."""
    __tablename__ = "article"

    id            = db.Column(db.Integer, primary_key=True)
    title         = db.Column(db.String(200), nullable=False)
    author_id     = db.Column(db.Integer, db.ForeignKey("writer.id"), nullable=False)
    content_md    = db.Column(db.Text,       nullable=False)
    created_at    = db.Column(db.DateTime,   default=datetime.utcnow)
    last_edited   = db.Column(db.DateTime,   default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    is_published  = db.Column(db.Boolean,    default=False)

    author = db.relationship("Writer", back_populates="articles")

    def __repr__(self):
        return f"<Article '{self.title}'>"
