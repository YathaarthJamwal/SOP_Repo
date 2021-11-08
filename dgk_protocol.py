from paillier.modified_paillier import *
# import random

# print ("Generating keypair...")
# priv, pub = generate_keypair(64)
# print(priv, "  ", pub)

class DGK:
    def __init__(self, client, server):
        self.client = client
        self.server = server

    def protocol(self):
        # self.server.r = 85
        # server = Server(pub, r)

        print("\n....Inside DGK Protocol....\n")
        # self.client.d = 8 #32 bit integer - considered as vector of bits here
        # client = Client(pub, priv)
        bits_of_d_encrypted = self.client.extract_bits_encrypt()
        # print(bits_of_d_encrypted)

        #first pass as per figure 5
        encrypted_e_bits = self.server.first_pass(bits_of_d_encrypted)

        #second pass as per figure 5
        lbda = self.client.second_pass(encrypted_e_bits)
        # print(decrypt(self.client.privkey, self.client.pubkey , lbda))
        print("\n....DGK Protocol Completed....\n")
        return lbda

    

# class Client:
#     def __init__(self, pubkey, privkey):
#         self.pubkey = pubkey
#         self.privkey = privkey
#         self.d = d

#     def extract_bits_encrypt(self):
#         self.bits_of_d  = []
#         # t = 1
#         for i in range(32):
#             self.bits_of_d.append(int(((1 << i) & self.d) > 0))
#         new_bits_of_d = [ele for ele in reversed(self.bits_of_d)]
#         self.bits_of_d_encrypted = []
#         for i in range(len(new_bits_of_d)):
#             encrypted_bit = encrypt(self.pubkey, new_bits_of_d[i])
#             self.bits_of_d_encrypted.append(encrypted_bit)
#         return self.bits_of_d_encrypted

#     def second_pass(self, encrypted_bits_e):
#         decrypted_e_bits = []
#         for i in range(len(self.bits_of_d)):
#             decrypted_ei = decrypt(self.privkey, self.pubkey, encrypted_bits_e[i])
#             decrypted_e_bits.append(decrypted_ei)
#         print("Decrypted E Bits \n\n", decrypted_e_bits)

#         if 0 in decrypted_e_bits:
#             self.lbda = 1
#         else:
#             self.lbda = 0
        
#         return self.lbda

#     # def output(self):
#     #     print()

# class Server:
#     def __init__(self, pubkey, r):
#         self.pubkey = pubkey
#         self.r = r

#     def extract_bits(self, r):
#         output  = []
#         # t = 1
#         for i in range(32):
#             output.append(int(((1 << i) & r) > 0))
#         self.bits_of_r = [ele for ele in reversed(output)]
#         print("Bits of r \n\n", self.bits_of_r)

#     def first_pass(self, bits_of_d_encrypted):
#         self.extract_bits(self.r)
#         # print(self.bits_of_r)

#         bits_of_r_encrypted = []
#         for i in range(len(self.bits_of_r)):
#             encrypted_bit = encrypt(self.pubkey, self.bits_of_r[i])
#             bits_of_r_encrypted.append(encrypted_bit)

#         # test = []
#         # for i in range(len(self.bits_of_r)):
#         #     x = modinv(bits_of_r_encrypted[i], pub.n_sq)
#         #     test.append(decrypt(priv, pub, e_add(pub, bits_of_r_encrypted[i], x)))
#         # print(" testing\n\n", test)

#         # for i in range(len(self.bits_of_r)):
#         #     print(decrypt(priv, pub, bits_of_r_encrypted[i]), " ")
#         # print("\n\n")

#         self.w_encrypted = []
#         for i in range(len(self.bits_of_r)):
#             encrypted_bit = e_add(self.pubkey, e_add(self.pubkey, bits_of_d_encrypted[i], bits_of_r_encrypted[i]), invmod(e_mul_const(self.pubkey, bits_of_d_encrypted[i], 2*self.bits_of_r[i]), self.pubkey.n_sq))
#             self.w_encrypted.append(encrypted_bit)
#         # print("w\n\n", self.w_encrypted)
#         # for i in range(len(self.bits_of_r)):
#         #     print(decrypt(priv, pub, self.w_encrypted[i]), " ")
#         # print("\n\n")

#         self.c_encrypted = []
#         self.e_encrypted = []
#         for i in range(len(self.bits_of_r)):
#             # one_minus_ri_encrypted = e_add_const(self.pubkey, e_mul_const(self.pubkey, bits_of_r_encrypted[i], -1), 1)
#             one_minus_ri_encrypted = e_add_const(self.pubkey, invmod(bits_of_r_encrypted[i], pub.n_sq), 1)

#             # last_product_term = self.w_encrypted[i+1] if i < len(self.bits_of_r)-1 else encrypt(pub, 0)
#             last_product_term = self.w_encrypted[i-1] if i > 0 else encrypt(pub, 0)
#             for j in range(0, i-1):
#                 last_product_term = e_add(pub, last_product_term, self.w_encrypted[j])
#             encrypted_bit_c = e_add(pub, e_add(pub, bits_of_d_encrypted[i], one_minus_ri_encrypted), last_product_term)

#             # print(encrypted_bit_c)
#             self.c_encrypted.append(encrypted_bit_c)

#             rand_value = random.randint(1, 1024)
            
#             encrypted_bit_e = e_mul_const(pub, encrypted_bit_c, rand_value)
#             self.e_encrypted.append(encrypted_bit_e)

#             # print(encrypted_bit_e)
#         # for i in range(len(self.bits_of_r)):
#         #     print(decrypt(priv, pub, self.c_encrypted[i]), " ")
#         # print("\n\n")

#         print("c_encrypted\n\n", self.e_encrypted)
#         # print(self.e_encrypted)

#         return self.e_encrypted



# r = 85
# server = Server(pub, r)


# d = 84 #32 bit integer - considered as vector of bits here
# client = Client(pub, priv)
# bits_of_d_encrypted = client.extract_bits_encrypt()
# # print(bits_of_d_encrypted)

# #first pass as per figure 5
# encrypted_e_bits = server.first_pass(bits_of_d_encrypted)

# #second pass as per figure 5
# lbda = client.second_pass(encrypted_e_bits)
# print(lbda)










