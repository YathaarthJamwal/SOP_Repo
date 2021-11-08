import math
# import primes
import random

def ipow(a, b, n):
    """calculates (a**b) % n via binary exponentiation, yielding intermediate
       results as Rabin-Miller requires"""
    A = a = (a % n)
    yield A
    t = 1
    while t <= b:
        t <<= 1

    # t = 2**k, and t > b
    t >>= 2
    
    while t:
        A = (A * A) % n
        if t & b:
            A = (A * a) % n
        yield A
        t >>= 1

def rabin_miller_witness(test, possible):
    """Using Rabin-Miller witness test, will return True if possible is
       definitely not prime (composite), False if it may be prime."""
    return 1 not in ipow(test, possible-1, possible)

smallprimes = (2,3,5,7,11,13,17,19,23,29,31,37,41,43,
               47,53,59,61,67,71,73,79,83,89,97)

def default_k(bits):
    return max(40, 2 * bits)

def is_probably_prime(possible, k=None):
    if possible == 1:
        return True
    if k is None:
        k = default_k(possible.bit_length())
    for i in smallprimes:
        if possible == i:
            return True
        if possible % i == 0:
            return False
    for i in range(int(k)):
        test = random.randrange(2, possible - 1) | 1
        if rabin_miller_witness(test, possible):
            return False
    return True

def generate_prime(bits, k=None):
    """Will generate an integer of b bits that is probably prime 
       (after k trials). Reasonably fast on current hardware for 
       values of up to around 512 bits."""
    assert bits >= 8

    if k is None:
        k = default_k(bits)

    while True:
        possible = random.randrange(2 ** (bits-1) + 1, 2 ** bits) | 1
        if is_probably_prime(possible, k):
            return possible



def invmod(a, p, maxiter=10000000):
    """The multiplicative inverse of a in the integers modulo p:
         a * b == 1 mod p
       Returns b.
       (http://code.activestate.com/recipes/576737-inverse-modulo-p/)"""
    if a == 0:
        raise ValueError('0 has no inverse mod %d' % p)
    r = a
    d = 1
    for i in range(min(p, maxiter)):
        d = ((p // r + 1) * d) % p
        r = (d * a) % p
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d

def invmod_pair(a, p):
    return invmod(a[0], p), invmod(a[1], p)

def modpow(base, exponent, modulus):
    """Modular exponent:
         c = b ^ e mod m
       Returns c.
       (http://www.programmish.com/?p=34)"""
    result = 1
    while exponent > 0:
        if exponent & 1 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

class PrivateKey(object):

    def __init__(self, p, q, n, x, g):
        # self.l = (p-1) * (q-1)
        # self.m = invmod(self.l, n)
        self.x = x
        self.g = g

    def __repr__(self):
        return '<PrivateKey: %s %s>' % (self.x, self.g)

    # def divide_key(self):
    #     # r = random.randint(1, self.x)
    #     self.key_1 = (r, self.g)
    #     self.key_2 = (self.x - r, self.g)
    #     return PrivateKey(p, q, n, x, g)

class PublicKey(object):

    @classmethod
    def from_n(cls, n):
        return cls(n)

    def __init__(self, n, x, g):
        self.n = n
        self.n_sq = n * n
        self.g = g
        # self.g = n + 1
        # a = 0
        # while True:
        #     a = random.randrange(0, self.n_sq)
        #     if (math.gcd(a, self.n_sq) == 1):
        #         break
        # self.g = (self.n_sq - pow(a, 2*self.n, self.n_sq)) % self.n_sq
        # print("\ng=", self.g)

        self.h = pow(self.g, x, self.n_sq)

    def __repr__(self):
        return '<PublicKey: %s %s %s>' % (self.n, self.g, self.h)

def generate_keypair(bits):
    p = generate_prime(bits / 2)
    while not is_probably_prime(2*p + 1, bits / 2):
        p = generate_prime(bits / 2)

    q = 2*p + 1
    # q = generate_prime(bits / 2)
    # p = 2*q + 1
    print("\np =", p, " ", "q =", q)
    n = p * q
    print("n =", n)
    n_sq = n*n
    x = random.randint(1, int(n_sq/2))
    print("\nx =", x)
    a = 0
    
    print("\nn_sq =", n_sq)
    while True:
        a = random.randrange(1, n_sq)
        if (math.gcd(a, n_sq) == 1):
            break
    print("\na =", a)
    # print("\npow(a, 2*n, n_sq)= ", pow(a, 2*n, n_sq))
    print("\ng = -a^2n = ", (-1*pow(a, 2*n, n_sq)) % n_sq)
    g = (-1*pow(a, 2*n, n_sq)) % n_sq

    # partial keys also generated in safe environment
    r = random.randint(1, x)
    return PrivateKey(p, q, n, x, g), PublicKey(n, x, g), PrivateKey(p, q, n, r, g), PrivateKey(p, q, n, x-r, g)

def encrypt(pub, plain):
    # while True:
    #     r = generate_prime(round(math.log(pub.n, 2)))
    #     if r > 0 and r < pub.n:
    #         break
    r = random.randint(1, int(pub.n/4))
    # print("\nr=", r)
    t1 = pow(pub.g, r, pub.n_sq)
    t2 = (pow(pub.h, r, pub.n_sq) * (1 + plain*pub.n)) % pub.n_sq
    return t1,t2
    # if plain < 0:
    #     x = pow(r, pub.n, pub.n_sq)
    #     cipher = (pow(pub.g, plain % pub.n, pub.n_sq) * x) % pub.n_sq
    #     return cipher
    # x = pow(r, pub.n, pub.n_sq)
    # cipher = (pow(pub.g, plain, pub.n_sq) * x) % pub.n_sq
    # return cipher

def re_encrypt(pub, cipher):
    r1 = random.randint(1, int(pub.n/4))
    print("\nr1= ", r1)
    t1_ = (pow(pub.g, r1, pub.n_sq) * (cipher[0])) % pub.n_sq
    t2_ = (pow(pub.h, r1, pub.n_sq) * (cipher[1])) % pub.n_sq
    return t1_, t2_

def egcd(a, b):
    if a == 0:
        return (b,0,1)
    else:
        g, y, x = egcd(b%a, a)
        return (g,x - (b // a)*y, y)
# def xgcd(a,b):
#     prevx = 1
#     x = 0
#     prevy = 0
#     y = 1
#     while b:
#         q = a/b;
#         x = prevx - q*x
#         prevx = x
#         y = prevy - q*y
#         prevy = y
#         a = b
#         b = a % b
#     return (a, prevx, prevy)

def modinv(a, m):
    g,x,y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def e_add(pub, a, b):
    """Add one encrypted integer to another"""
    return a[0] * b[0] % pub.n_sq, a[1] * b[1] % pub.n_sq

def e_add_const(pub, a, n):
    """Add constant n to an encrypted integer"""
    return a[0] * modpow(pub.g, n, pub.n_sq) % pub.n_sq, a[1] * modpow(pub.g, n, pub.n_sq) % pub.n_sq

def e_mul_const(pub, a, n):
    """Multiplies an encrypted integer by a constant"""
    power_negative = 0
    if n == -1:
        ans1 = modinv(a[0], pub.n_sq) % pub.n_sq
        ans2 = modinv(a[1], pub.n_sq) % pub.n_sq
        print(ans1, " ", ans2, " in here")
        return ans1, ans2

    return modpow(a[0], n, pub.n_sq), modpow(a[1], n, pub.n_sq)

def decrypt(priv, pub, cipher):
    # x = pow(cipher, priv.l, pub.n_sq) - 1
    # plain = ((x // pub.n) * priv.m) % pub.n
    # return plain
    def delta(val):
        res = ((val - 1) % pub.n_sq) / pub.n
        return int(res)

    t1 = cipher[0]
    t2 = cipher[1]
    deno = pow(t1, priv.x, pub.n_sq)
    # print(deno)
    u = (invmod(deno, pub.n_sq) * t2) % pub.n_sq
    # print("u= ",u)
    return delta(u)

def partial_decrypt(priv, pub, cipher):
    t1 = cipher[0]
    denominator = pow(cipher[0], priv.x, pub.n_sq)
    print("in here: ", denominator)
    t2 = (cipher[1] / denominator) % pub.n_sq
    return t1, t2

def modular_sqrt(a, p):

    def legendre_symbol(a, p):
        """ Compute the Legendre symbol a|p using
            Euler's criterion. p is a prime, a is
            relatively prime to p (if p divides
            a, then a|p = 0)
            Returns 1 if a has a square root modulo
            p, -1 otherwise.
        """
        ls = pow(a, (p - 1) // 2, p)
        return -1 if ls == p - 1 else ls

    """ Find a quadratic residue (mod p) of 'a'. p
        must be an odd prime.
        Solve the congruence of the form:
            x^2 = a (mod p)
        And returns x. Note that p - x is also a root.
        0 is returned is no square root exists for
        these a and p.
        The Tonelli-Shanks algorithm is used (except
        for some simple cases in which the solution
        is known from an identity). This algorithm
        runs in polynomial time (unless the
        generalized Riemann hypothesis is false).
    """
    # Simple cases
    #
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Partition p-1 to s * 2^e for an odd s (i.e.
    # reduce all the powers of 2 from p-1)
    #
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    # Find some 'n' with a legendre symbol n|p = -1.
    # Shouldn't take long.
    #
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    # Here be dragons!
    # Read the paper "Square roots from 1; 24, 51,
    # 10 to Dan Shanks" by Ezra Brown for more
    # information
    #

    # x is a guess of the square root that gets better
    # with each iteration.
    # b is the "fudge factor" - by how much we're off
    # with the guess. The invariant x^2 = ab (mod p)
    # is maintained throughout the loop.
    # g is used for successive powers of n to update
    # both a and b
    # r is the exponent - decreases with each update
    #
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m

