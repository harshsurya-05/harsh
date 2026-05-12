import re


def validate_required_fields(data: dict, fields: list) -> list:
    """Returns list of missing required field names."""
    if not data:
        return fields
    return [f for f in fields if f not in data or data[f] is None or str(data[f]).strip() == '']


def validate_email(email: str) -> bool:
    """Basic email format validation."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))


def success_response(data: dict, message: str = 'Success', status: int = 200):
    return {'status': 'success', 'message': message, 'data': data}, status


def error_response(message: str, status: int = 400):
    return {'status': 'error', 'message': message}, status


def paginate_query(query, page: int = 1, per_page: int = 20):
    """Helper to paginate SQLAlchemy queries."""
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        'items': paginated.items,
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page,
        'per_page': per_page,
        'has_next': paginated.has_next,
        'has_prev': paginated.has_prev
    }


CATEGORIES = ['Vegetables', 'Fruits', 'Grains', 'Pulses', 'Spices', 'Dairy', 'Other']


def format_currency(amount: float, symbol: str = '₹') -> str:
    return f'{symbol}{amount:,.2f}'
