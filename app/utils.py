from datetime import datetime, timezone
from typing import Dict, Any, List

def format_date(date_obj: datetime) -> str:
    """Format a datetime object to a readable string."""
    if date_obj:
        return date_obj.strftime("%Y-%m-%d %H:%M:%S")
    return ""

def format_date_to_obj(date_str: str) -> datetime:
    """Convert a date string to a datetime object."""
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return None

def get_current_utc_time() -> datetime:
    """Get the current UTC time."""
    return datetime.now(timezone.utc)

def paginate_results(items: List[Any], page: int, per_page: int) -> Dict:
    """Paginate a list of items."""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        "items": items[start:end],
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total + per_page - 1) // per_page
    }