from paillier.modified_paillier import *

import random
import math
# import libnum

# print(libnum.primes(100))
# print(libnum.factorize(266389614190954197077551832167907987753))

# print ("Generating keypair...")
# priv, pub, priv_key1, priv_key2 = generate_keypair(32)
# print(priv, "  ", pub)

# a = 423
# b = 2
# print("a= ",a, " b= ", b)
# ea = encrypt(pub, a)
# eb = encrypt(pub, b)
# print("Ciphertext a: ",ea," Ciphertext b: ", eb)
# res = e_mul_const(pub, ea, b)
# print("Decrypted value: " ,decrypt(priv, pub, res))

# matrix = [ [random.randint(0, 1) for i in range (8*256)] for j in range(4*8) ]
# print(matrix)
print(math.log2(1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000))

# matrix2 = [ [j for j in matrix[i]] for i  in range(len(matrix)) ]
# matrix2[0][0] = (1 if matrix[0][0] == 0 else 0)
# if (matrix2 == matrix):
#     print("\nsame")
# else:
#     print("\nnot same")
# eb = re_encrypt(pub, ea)
# print("Ciphertext: ",eb)
# print("Decrypted value: " ,decrypt(priv, pub, eb))

# new_priv = priv.divide_key()
# print(new_priv)

# b = 236
# print(b)
# ebb = encrypt(pub, b)
# print("key_1: ", priv_key1)
# b1 = partial_decrypt(priv_key1, pub, ebb)
# print("b1= ", b1)
# print("key_2: ", priv_key2)
# b2 = decrypt(priv_key2, pub, b1)
# print("b2= ", b2)
