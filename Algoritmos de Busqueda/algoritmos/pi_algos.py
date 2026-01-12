import sys
import math
import time
from decimal import Decimal, getcontext

sys.set_int_max_str_digits(15000)
sys.setrecursionlimit(20000)

class PiAlgorithms:
    @staticmethod
    def pi_iterative(precision):
        start_time = time.time()
        getcontext().prec = precision + 3
        
        def arctan(x, p):
            x_big = 10**(p + 10)
            x2 = x * x
            termino = x_big // x
            suma = termino
            n = 1
            while True:
                n += 2
                termino //= x2
                if termino == 0: break
                if (n // 2) % 2 == 1: suma -= termino // n
                else: suma += termino // n
            return suma

        res = 4 * (4 * arctan(5, precision) - arctan(239, precision))
        s_res = str(res // 10**10)
        final_str = s_res[0] + "." + s_res[1:]
        
        ms = (time.time() - start_time) * 1000
        return final_str, ms

    @staticmethod
    def pi_recursive_dv(precision):
        start_time = time.time()
        getcontext().prec = precision + 3
        
        def bs_chudnovsky(a, b):
            if b - a == 1:
                if a == 0:
                    P = Q = 1
                else:
                    P = (13591409 + 545140134 * a) * (-(6*a-5)*(2*a-1)*(6*a-1))
                    Q = (a**3) * (640320**3 // 24)
                T = P
                return P, Q, T
            else:
                m = (a + b) // 2
                P1, Q1, T1 = bs_chudnovsky(a, m)
                P2, Q2, T2 = bs_chudnovsky(m, b)
                return P1 * P2, Q1 * Q2, Q2 * T1 + P1 * T2

        n_terminos = math.ceil(precision / 14) 
        P, Q, T = bs_chudnovsky(0, n_terminos)
        C = 426880 * Decimal(10005).sqrt()
        pi = (C * Q) / (13591409 * Q + T)
        
        ms = (time.time() - start_time) * 1000
        return str(pi)[:precision + 2], ms