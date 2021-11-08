#!/usr/bin/env python

from paillier.paillier import *

# import libnum

# print(libnum.primes(100))
# print(libnum.factorize(266389614190954197077551832167907987753))

print ("Generating keypair...")
priv, pub = generate_keypair(16)
print(priv, "  ", pub)

# x = 3
# print ("x =", x)
# print ("Encrypting x...")
# cx = encrypt(pub, x)
# print ("cx =", cx)
# print("x=" ,decrypt(priv, pub, cx))

# y = 5
# print ("y =", y)
# print ("Encrypting y...")
# cy = encrypt(pub, y)
# print ("cy =", cy)
# print("y=" ,decrypt(priv, pub, cy))

# print ("Computing cx + cy...")
# cz = e_add(pub, cx, cy)
# print ("cz =", cz)

# print ("Decrypting cz...")
# z = decrypt(priv, pub, cz)
# print ("z =", z)

# print ("Computing decrypt((cz + 2) * 3) ...")
# print ("result =", decrypt(priv, pub,
#                           e_mul_const(pub, e_add_const(pub, cz, 2), 3)))

x = 4
cx = encrypt(pub, x)
print(cx)
print(decrypt(priv, pub, cx))

print(-1*x)
# val = encrypt(pub, -1*x)
# val = e_mul_const(pub, cx, -1)
val = invmod(cx, pub.n_sq)
final = e_add(pub, cx, val)
print(final)

print(decrypt(priv, pub, final))

# randVal = random.randint(0, 2**(101+32))
# print(randVal)

# def modular_sqrt(a, p):

#     def legendre_symbol(a, p):
#         """ Compute the Legendre symbol a|p using
#             Euler's criterion. p is a prime, a is
#             relatively prime to p (if p divides
#             a, then a|p = 0)
#             Returns 1 if a has a square root modulo
#             p, -1 otherwise.
#         """
#         ls = pow(a, (p - 1) // 2, p)
#         return -1 if ls == p - 1 else ls

#     """ Find a quadratic residue (mod p) of 'a'. p
#         must be an odd prime.
#         Solve the congruence of the form:
#             x^2 = a (mod p)
#         And returns x. Note that p - x is also a root.
#         0 is returned is no square root exists for
#         these a and p.
#         The Tonelli-Shanks algorithm is used (except
#         for some simple cases in which the solution
#         is known from an identity). This algorithm
#         runs in polynomial time (unless the
#         generalized Riemann hypothesis is false).
#     """
#     # Simple cases
#     #
#     if legendre_symbol(a, p) != 1:
#         return 0
#     elif a == 0:
#         return 0
#     elif p == 2:
#         return p
#     elif p % 4 == 3:
#         return pow(a, (p + 1) // 4, p)

#     # Partition p-1 to s * 2^e for an odd s (i.e.
#     # reduce all the powers of 2 from p-1)
#     #
#     s = p - 1
#     e = 0
#     while s % 2 == 0:
#         s //= 2
#         e += 1

#     # Find some 'n' with a legendre symbol n|p = -1.
#     # Shouldn't take long.
#     #
#     n = 2
#     while legendre_symbol(n, p) != -1:
#         n += 1

#     # Here be dragons!
#     # Read the paper "Square roots from 1; 24, 51,
#     # 10 to Dan Shanks" by Ezra Brown for more
#     # information
#     #

#     # x is a guess of the square root that gets better
#     # with each iteration.
#     # b is the "fudge factor" - by how much we're off
#     # with the guess. The invariant x^2 = ab (mod p)
#     # is maintained throughout the loop.
#     # g is used for successive powers of n to update
#     # both a and b
#     # r is the exponent - decreases with each update
#     #
#     x = pow(a, (s + 1) // 2, p)
#     b = pow(a, s, p)
#     g = pow(n, s, p)
#     r = e

#     while True:
#         t = b
#         m = 0
#         for m in range(r):
#             if t == 1:
#                 break
#             t = pow(t, 2, p)

#         if m == 0:
#             return x

#         gs = pow(g, 2 ** (r - m - 1), p)
#         g = (gs * gs) % p
#         x = (x * gs) % p
#         b = (b * g) % p
#         r = m

# print(modular_sqrt(30418014865314379746372009363345157183977066918744862092261689018772940667718, 40406066415879874301109841807530739468039791893736288074119681915760733042889)) # should return 6


# Python3 program to implement Shanks Tonelli
# algorithm for finding Modular Square Roots
 
# utility function to find pow(base,
# exponent) % modulus
def pow1(base, exponent, modulus):
 
    result = 1;
    base = base % modulus;
    while (exponent > 0):
        if (exponent % 2 == 1):
            result = (result * base) % modulus;
        exponent = int(exponent) >> 1;
        base = (base * base) % modulus;
 
    return result;
 
# utility function to find gcd
def gcd(a, b):
    if (b == 0):
        return a;
    else:
        return gcd(b, a % b);
 
# Returns k such that b^k = 1 (mod p)
def order(p, b):
 
    if (gcd(p, b) != 1):
        print("p and b are not co-prime.\n");
        return -1;
 
    # Initializing k with first
    # odd prime number
    k = 3;
    while (True):
        if (pow1(b, k, p) == 1):
            return k;
        k += 1;
 
# function return p - 1 (= x argument) as
# x * 2^e, where x will be odd sending e
# as reference because updation is needed
# in actual e
def convertx2e(x):
    z = 0;
    while (x % 2 == 0):
        x = x / 2;
        z += 1;
         
    return [x, z];
 
# Main function for finding the
# modular square root
def STonelli(n, p):

    # a and p should be coprime for
    # finding the modular square root
    if (gcd(n, p) != 1):
        print("a and p are not coprime\n");
        return -1;
 
    # If below expression return (p - 1) then
    # modular square root is not possible
    if (pow1(n, (p - 1) / 2, p) == (p - 1)):
        print("no sqrt possible\n");
        return -1;
 
    # expressing p - 1, in terms of s * 2^e,
    # where s is odd number
    ar = convertx2e(p - 1);
    s = ar[0];
    e = ar[1];
 
    # finding smallest q such that
    # q ^ ((p - 1) / 2) (mod p) = p - 1
    q = 2;
    while (True):
         
        # q - 1 is in place of (-1 % p)
        if (pow1(q, (p - 1) / 2, p) == (p - 1)):
            break;
        q += 1;
 
    # Initializing variable x, b and g
    x = pow1(n, (s + 1) / 2, p);
    b = pow1(n, s, p);
    g = pow1(q, s, p);
 
    r = e;
 
    # keep looping until b become
    # 1 or m becomes 0
    while (True):
        m = 0;
        while (m < r):
            if (order(p, b) == -1):
                return -1;
 
            # finding m such that b^ (2^m) = 1
            if (order(p, b) == pow(2, m)):
                break;
            m += 1;
 
        if (m == 0):
            return x;
 
        # updating value of x, g and b
        # according to algorithm
        x = (x * pow1(g, pow(2, r - m - 1), p)) % p;
        g = pow1(g, pow(2, r - m), p);
        b = (b * g) % p;
 
        if (b == 1):
            return x;
        r = m;
 
# Driver Code
n = 2;
 
# p should be prime
p = 113;
 
# x = STonelli(17392178544435983572607078783800631996162039072059498421889801425767802465275, 22341564833628683843025838940725525006380262614964654019432351484628231388209);
 
# if (x == -1):
#     print("Modular square root is not exist\n");
# else:
#     print("Modular square root of", n,
#           "and", p, "is", x);
         
# This code is contributed by mits