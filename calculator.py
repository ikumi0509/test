def add(a, b):
    """足し算"""
    return a + b


def subtract(a, b):
    """引き算"""
    return a - b


def multiply(a, b):
    """掛け算"""
    return a * b


def divide(a, b):
    """割り算（ゼロ除算はValueErrorを発生）"""
    if b == 0:
        raise ValueError("ゼロで割ることはできません")
    return a / b
