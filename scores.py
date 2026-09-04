import os
import json
from cryptography.fernet import Fernet
import config

def get_or_create_key():
    if not os.path.exists(config.SECRET_KEY_FILE):
        key = Fernet.generate_key()
        with open(config.SECRET_KEY_FILE, "wb") as f:
            f.write(key)
        return key
    with open(config.SECRET_KEY_FILE, "rb") as f:
        return f.read()

def load_high_scores():
    if not os.path.exists(config.SCORE_FILE):
        return []
    try:
        key = get_or_create_key()
        fernet = Fernet(key)
        with open(config.SCORE_FILE, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode("utf-8"))
    except Exception:
        return []

def save_high_score(initials, score):
    scores = load_high_scores()
    scores.append({"initials": initials.upper()[:3], "score": score})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]

    key = get_or_create_key()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(json.dumps(scores).encode("utf-8"))
    with open(config.SCORE_FILE, "wb") as f:
        f.write(encrypted_data)
