from app.models.writer import Writer
from app.models.article import Article
from app import db
from typing import Optional, List
from datetime import datetime, timezone

def create_article(title: str, content_md: str, author_id: int, is_published: Optional[bool] = False) -> Article:
    """Create a new article."""
    new_article = Article(
        title=title,
        author_id=author_id,
        content_md=content_md,
        created_at=datetime.now(timezone.utc),
        last_edited=datetime.now(timezone.utc),
        is_published=is_published
    )
    db.session.add(new_article)
    db.session.commit()
    return new_article

def update_article(article_id: int, 
                   title: Optional[str] = None,
                   author_id: Optional[int] = None,
                   content_md: Optional[str] = None, 
                   is_published: Optional[bool] = None) -> Article:
    """Update an article's information.
    All parameters are optional.
    """
    article = Article.query.get(article_id)
    if not article:
        return None
    if title:
        article.title = title
    if content_md:
        article.content_md = content_md
    if author_id:
        article.author_id = author_id
    if is_published is not None:
        article.is_published = is_published
    article.last_edited = datetime.now(timezone.utc)
    db.session.commit()
    return article

def delete_article(article_id: int) -> bool:
    """Delete an article."""
    article = Article.query.get(article_id)
    if not article:
        return False
    db.session.delete(article)
    db.session.commit()
    return True