from app import db
from datetime import datetime

class Writer(db.Model):
    __tablename__ = "writer"

    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    user      = db.relationship("User", back_populates="writer")
    articles  = db.relationship("Article", back_populates="author")

    def __repr__(self):
        return f"<Writer {self.user.username}>"
