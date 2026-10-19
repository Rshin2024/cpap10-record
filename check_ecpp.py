#!/usr/bin/env python3
"""Standalone integer-arithmetic checker for PARI ECPP certificate vectors.

No PARI, FLINT, GMP, or other third-party Python dependency is imported.
The certificate theorem and format are documented at
https://pari.math.u-bordeaux.fr/dochtml/html-stable/Arithmetic_functions.html#primecert

Terminal primes are < 2^64 and are checked deterministically using strong
Miller--Rabin for the first 13 prime bases (2 through 41). This is within the
proven range documented for this base set in FLINT's fmpz_is_prime reference:
https://flintlib.org/doc/fmpz.html#c.fmpz_is_prime (Sorenson--Webster 2016).
"""
import argparse
import json
import math
from pathlib import Path

BASES = (2,3,5,7,11,13,17,19,23,29,31,37,41)


def prime_u64(n):
    if not 2 <= n < 2**64:
        return False
    for p in BASES:
        if n == p:return True
        if n % p == 0:return False
    d=n-1;s=0
    while not d&1:d//=2;s+=1
    for a in BASES:
        z=pow(a,d,n)
        if z in (1,n-1):continue
        for _ in range(s-1):
            z=z*z%n
            if z==n-1:break
        else:return False
    return True


def add(P,Q,a,n):
    if P is None:return Q
    if Q is None:return P
    x,y=P;u,v=Q
    if x==u:
        if (y+v)%n==0:return None
        if y!=v:raise ValueError('Same x with incompatible y coordinates')
        top=(3*x*x+a)%n;bottom=2*y%n
    else:
        top=(v-y)%n;bottom=(u-x)%n
    if math.gcd(bottom,n)!=1:
        raise ValueError('Nonunit elliptic-curve denominator')
    slope=top*pow(bottom,-1,n)%n
    xx=(slope*slope-x-u)%n
    return xx,(slope*(x-xx)-y)%n


def mul(k,P,a,n):
    if k<0:raise ValueError('Negative scalar')
    R=None
    while k:
        if k&1:R=add(R,P,a,n)
        k//=2
        if k:P=add(P,P,a,n)
    return R


def large_enough_q(q,n):
    # q > (n^(1/4)+1)^2, evaluated using integer polynomial inequalities.
    # Equivalently (sqrt(q)-1)^4 > n for q > 1.
    if q<=1:return False
    z=q*q+6*q+1-n
    return z>0 and z*z>16*q*(q+1)**2


def verify_certificate(cert, expected=None):
    if isinstance(cert,int):
        if expected is not None and cert!=expected:raise ValueError('Wrong certified integer')
        if not prime_u64(cert):raise ValueError('Invalid small-prime certificate')
        return dict(prime=str(cert),steps=0,terminal_prime=str(cert),verified=True)
    if not isinstance(cert,list) or not cert:raise ValueError('Empty or non-vector certificate')
    if expected is not None and cert[0][0]!=expected:raise ValueError('Wrong certified integer')
    for j,row in enumerate(cert):
        if not isinstance(row,list) or len(row)!=5:raise ValueError('Malformed certificate row')
        n,t,s,a,P=row
        if not all(type(v) is int for v in (n,t,s,a)) or n<=3 or not n&1 or s<=0:
            raise ValueError('Invalid row integers')
        if t*t>=4*n:raise ValueError('Trace outside Hasse bound')
        m=n+1-t
        if m<=0 or m%s:raise ValueError('Invalid order/cofactor')
        q=m//s
        if not large_enough_q(q,n):raise ValueError('Insufficient prime-order factor')
        if j+1<len(cert):
            if q!=cert[j+1][0]:raise ValueError('Broken certificate chain')
        elif not prime_u64(q):raise ValueError('Terminal factor not a proven 64-bit prime')
        if not isinstance(P,list) or len(P)!=2 or not all(type(v) is int for v in P):
            raise ValueError('Invalid affine point')
        x,y=(v%n for v in P);a%=n;b=(y*y-x*x*x-a*x)%n
        if math.gcd(4*a*a*a+27*b*b,n)!=1:
            raise ValueError('Singular elliptic curve modulo a divisor')
        if mul(m,(x,y),a,n) is not None:raise ValueError('Claimed curve order does not kill point')
        if mul(s,(x,y),a,n) is None:raise ValueError('Cofactor kills point')
    return dict(prime=str(cert[0][0]),steps=len(cert),terminal_prime=str(q),verified=True)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('certificate',type=Path)
    ap.add_argument('--expected',type=int)
    args=ap.parse_args()
    cert=json.loads(args.certificate.read_text())
    print(json.dumps(verify_certificate(cert,args.expected)))


if __name__=='__main__':main()
