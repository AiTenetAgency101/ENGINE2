from dataclasses import dataclass
from sympy import Rational

PHI = (1 + 5**0.5) / 2
KAPREKAR = 6174
TOL = Rational(1, 20)  # 0.05

@dataclass
class Invariants:
    phi: float = PHI
    kaprekar: int = KAPREKAR
    tol: Rational = TOL

    def within_tol(self, value: float, target: float) -> bool:
        return abs(value - target) <= float(self.tol)

INV = Invariants()
