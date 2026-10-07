import sympy as sp
from scipy import integrate, optimize
import numpy as np

def calculate_derivative(expr_str: str) -> str:
    """Символьное вычисление производной (SymPy)"""
    x = sp.Symbol('x')
    expr = sp.sympify(expr_str)
    deriv = sp.diff(expr, x)
    return str(sp.simplify(deriv))

def calculate_integral(expr_str: str, a: float, b: float) -> float:
    """Численное вычисление определенного интеграла (SciPy)"""
    x = sp.Symbol('x')
    expr = sp.sympify(expr_str)
    # Преобразуем sympy выражение в numpy-функцию для scipy
    f = sp.lambdify(x, expr, 'numpy')
    result, error = integrate.quad(f, a, b)
    return round(result, 6)

def find_root(expr_str: str, x0: float) -> float:
    """Численный поиск корня уравнения f(x) = 0 (SciPy)"""
    x = sp.Symbol('x')
    expr = sp.sympify(expr_str)
    f = sp.lambdify(x, expr, 'numpy')
    # Используем итерационный метод для поиска корня
    root = optimize.root_scalar(f, x0=x0)
    return round(root.root, 6)