import bcrypt
from database import get_user_by_username, add_user, init_db


def hash_password(plain_text_password: str) -> str:
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(plain_text_password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False


def create_user(name, username, email, password):
    hashed = hash_password(password)
    return add_user(name, username, email, hashed, is_admin=0)


def ensure_admin(username='PradipT0928', password='PradipT@0928'):
    # Initialize DB and ensure admin present
    init_db()
    u = get_user_by_username(username)
    if u:
        return u
    hashed = hash_password(password)
    add_user('Admin', username, 'admin@prepstr.local', hashed, is_admin=1)
    return get_user_by_username(username)
