import re
import unicodedata
from datetime import datetime
from typing import List, Dict, Any, Optional

def format_date(date: datetime, format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """Formatea fecha a string"""
    if isinstance(date, str):
        try:
            date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        except:
            return date
    return date.strftime(format)

def generate_slug(text: str) -> str:
    """Genera slug URL-friendly desde texto"""
    # Normalizar unicode
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Convertir a minúsculas y reemplazar espacios
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    
    return text.strip('-')

def sanitize_filename(filename: str) -> str:
    """Sanitiza nombre de archivo"""
    # Remover caracteres peligrosos
    filename = re.sub(r'[^\w\s.-]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    
    # Limitar longitud
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    if len(name) > 100:
        name = name[:100]
    
    return f"{name}.{ext}" if ext else name

def paginate_results(data: List[Dict], page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """Pagina resultados"""
    total = len(data)
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'data': data[start:end],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': (total + per_page - 1) // per_page,
            'has_next': end < total,
            'has_prev': page > 1
        }
    }

def format_price(price: float, currency: str = 'COP') -> str:
    """Formatea precio con separadores de miles"""
    symbols = {
        'COP': '$',
        'USD': '$',
        'EUR': '€'
    }
    symbol = symbols.get(currency, '$')
    return f"{symbol}{price:,.2f}"

def calculate_percentage(part: float, total: float) -> float:
    """Calcula porcentaje"""
    if total == 0:
        return 0
    return round((part / total) * 100, 2)

def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """Trunca texto a longitud máxima"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)].strip() + suffix

def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Mezcla dos diccionarios recursivamente"""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result

def remove_none_values(data: Dict) -> Dict:
    """Remueve valores None de un diccionario"""
    return {k: v for k, v in data.items() if v is not None}

def group_by_key(data: List[Dict],key: str) -> Dict[str, List[Dict]]:
    """Agrupa lista de diccionarios por clave"""
    result = {}
    for item in data:
        group_key = item.get(key)
        if group_key not in result:
            result[group_key] = []
        result[group_key].append(item)
    return result

def flatten_dict(data: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """Aplana diccionario anidado"""
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def generate_unique_code(prefix: str = '', length: int = 8) -> str:
    """Genera código único"""
    import random
    import string
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}{code}" if prefix else code 
