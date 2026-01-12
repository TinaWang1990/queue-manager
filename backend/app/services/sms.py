import random

def send_code(phone: str) -> str:
    code = str(random.randint(100000, 999999))
    print(f"[SMS MOCK] {phone} -> {code}")
    return code
