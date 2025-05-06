# test/utils.py
# 테스트용 유틸리티 함수
import random
import string

def generate_random_string(length: int = 16) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

