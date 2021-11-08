# from math import log2
from dgk_protocol import *
from paillier.modified_paillier import *
import libnum

print ("Generating keypair...")
priv, pub, priv_key1, priv_key2 = generate_keypair(64)
# priv_key1, priv_key2 can be used in case we wish to divide x into 2 parts for proxy re-encryption
print("The private and public keys are as per the following template:")
print("<PrivateKey: x g> \n <PublicKey: n g h=g^x>")
print("\n",priv, "\n", pub, "\n")

# print("\nn: " ,pub.n)

# Length of input is fixed
length = 32

# encrypted_length = encrypt(pub, 2**length-1)
# inverse_encrypted_length = invmod_pair(encrypted_length, pub.n_sq)
# print("here" ,inverse_encrypted_length)

class Client:
    def __init__(self, pubkey, privkey):
        self.pubkey = pubkey
        self.privkey = privkey
        # self.d = d

    def initialize(self, d_encrypted):
        self.d = decrypt(self.privkey, self.pubkey, d_encrypted)
        self.d_cap = self.d % (2**length)
        self.d_cap_encrypted = encrypt(self.pubkey, self.d_cap)
        return self.d_cap_encrypted

    def extract_bits_encrypt(self):
        self.bits_of_d  = []
        # t = 1
        for i in range(length):
            self.bits_of_d.append(int(((1 << i) & self.d_cap) > 0))
        new_bits_of_d = [ele for ele in reversed(self.bits_of_d)]
        self.bits_of_d_encrypted = []
        for i in range(len(new_bits_of_d)):
            encrypted_bit = encrypt(self.pubkey, new_bits_of_d[i])
            self.bits_of_d_encrypted.append(encrypted_bit)
        return self.bits_of_d_encrypted

    def second_pass(self, encrypted_bits_e):
        decrypted_e_bits = []
        for i in range(len(self.bits_of_d)):
            decrypted_ei = decrypt(self.privkey, self.pubkey, encrypted_bits_e[i])
            decrypted_e_bits.append(decrypted_ei)
        print("Decrypted E Bits \n\n", decrypted_e_bits)

        if 0 in decrypted_e_bits:
            self.lbda = 1
        else:
            self.lbda = 0

        encrypted_lbda = encrypt(self.pubkey, self.lbda)
        
        return encrypted_lbda

    # def output(self):
    #     print()

class Server:
    def __init__(self, pubkey, X_encrypted, Y_encrypted):
        self.pubkey = pubkey
        # self.r = r
        self.X_encrypted = X_encrypted
        self.Y_encrypted = Y_encrypted

    def calculateValues(self):
        randVal = random.randint(0, 2**(length))
        print("\nRandom value r is:", randVal)
        self.r = randVal
        self.r_encrypted = encrypt(self.pubkey, self.r)
        print("\nEncrypted r =", self.r_encrypted)

        self.z_encrypted = e_add(self.pubkey, encrypt(self.pubkey, 2**length), e_add(self.pubkey, self.X_encrypted, invmod_pair(self.Y_encrypted, self.pubkey.n_sq)))
        # print("\nz - z^\n", decrypt(priv, pub, self.z_encrypted) - (decrypt(priv, pub, self.z_encrypted) % 2**length), "\n")
        print("\nEncrypted z =", self.z_encrypted)
        self.d_encrypted = e_add(self.pubkey, self.z_encrypted, self.r_encrypted)
        print("\nEncrypted d =", self.d_encrypted)

        self.r_cap = self.r % (2**length)

        return self.d_encrypted



    def extract_bits(self, r_cap):
        output  = []
        # t = 1
        for i in range(length):
            output.append(int(((1 << i) & r_cap) > 0))
        self.bits_of_r = [ele for ele in reversed(output)]
        print("Extracted bits of r \n", self.bits_of_r)

    def first_pass(self, bits_of_d_encrypted):
        self.extract_bits(self.r_cap)
        # print(self.bits_of_r)

        bits_of_r_encrypted = []
        for i in range(len(self.bits_of_r)):
            encrypted_bit = encrypt(self.pubkey, self.bits_of_r[i])
            bits_of_r_encrypted.append(encrypted_bit)

        # test = []
        # for i in range(len(self.bits_of_r)):
        #     x = modinv(bits_of_r_encrypted[i], pub.n_sq)
        #     test.append(decrypt(priv, pub, e_add(pub, bits_of_r_encrypted[i], x)))
        # print(" testing\n\n", test)

        # for i in range(len(self.bits_of_r)):
        #     print(decrypt(priv, pub, bits_of_r_encrypted[i]), " ")
        # print("\n\n")

        self.w_encrypted = []
        for i in range(len(self.bits_of_r)):
            encrypted_bit = e_add(self.pubkey, e_add(self.pubkey, bits_of_d_encrypted[i], bits_of_r_encrypted[i]), invmod_pair(e_mul_const(self.pubkey, bits_of_d_encrypted[i], 2*self.bits_of_r[i]), self.pubkey.n_sq))
            self.w_encrypted.append(encrypted_bit)
        # print("w\n\n", self.w_encrypted)
        # for i in range(len(self.bits_of_r)):
        #     print(decrypt(priv, pub, self.w_encrypted[i]), " ")
        # print("\n\n")

        print("\nEncrypted w: ")
        print(self.w_encrypted)

        self.c_encrypted = []
        self.e_encrypted = []
        for i in range(len(self.bits_of_r)):
            # one_minus_ri_encrypted = e_add_const(self.pubkey, e_mul_const(self.pubkey, bits_of_r_encrypted[i], -1), 1)
            one_minus_ri_encrypted = e_add(self.pubkey, invmod_pair(bits_of_r_encrypted[i], pub.n_sq), encrypt(self.pubkey, 1))   #e_add_const

            # last_product_term = self.w_encrypted[i+1] if i < len(self.bits_of_r)-1 else encrypt(pub, 0)
            last_product_term = self.w_encrypted[i-1] if i > 0 else encrypt(pub, 0)
            for j in range(0, i-1):
                last_product_term = e_add(pub, last_product_term, self.w_encrypted[j])
            encrypted_bit_c = e_add(pub, e_add(pub, bits_of_d_encrypted[i], one_minus_ri_encrypted), last_product_term)

            # print(encrypted_bit_c)
            self.c_encrypted.append(encrypted_bit_c)

            rand_value = random.randint(1, 1024)
            # re-randomization
            encrypted_bit_e = e_mul_const(pub, encrypted_bit_c, rand_value)
            self.e_encrypted.append(encrypted_bit_e)

            # print(encrypted_bit_e)
        # for i in range(len(self.bits_of_r)):
        #     print(decrypt(priv, pub, self.c_encrypted[i]), " ")
        # print("\n\n")

        print("\nEncrypted c:\n", self.c_encrypted)
        print("\nEncrypted e:\n", self.e_encrypted)
        # print(self.e_encrypted)

        return self.e_encrypted

    def final_calculation(self, encrypted_lbda, d_cap_encrypted):
        self.r_cap_encrypted = encrypt(self.pubkey, self.r_cap)
        print("\nEncrypted r_cap =", self.r_cap_encrypted)
        d_cap_encrypted_inverse = invmod_pair(d_cap_encrypted, self.pubkey.n_sq)
        print("\nInverse of encrypted d_cap =", d_cap_encrypted_inverse)

        # encrypted_lbda_powered = e_mul_const(self.pubkey, invmod(encrypted_lbda, self.pubkey.n_sq), 2**32)
        encrypted_lbda_powered = invmod_pair(e_mul_const(self.pubkey, encrypted_lbda, 2**length), self.pubkey.n_sq)

        product_term = e_add(self.pubkey, e_add(self.pubkey, self.z_encrypted, d_cap_encrypted_inverse), e_add(self.pubkey, self.r_cap_encrypted, encrypted_lbda_powered))
        
        self.b_encrypted = product_term
        # print("\nb: ", decrypt(priv, pub, self.b_encrypted))
        print("\nn_sq: ", self.pubkey.n_sq)
        print("\nb_encrypted: ", self.b_encrypted)



        # for i in range(32):
        #     # print(i)
        #     # self.b_encrypted = modular_sqrt(self.b_encrypted, self.pubkey.n_sq)
        #     self.b_encrypted = math.sqrt(self.b_encrypted)

        # self.b_encrypted = e_add(self.pubkey, self.b_encrypted, inverse_encrypted_length)

        # print("\nb_encrypted after: ", self.b_encrypted)

        return self.b_encrypted


# class bitMIN:
#     def __init__(self, client, server):
#         self.client = client
#         self.server = server

#     def 

# d = 8
client = Client(pub, priv)

# r = 9
# server = Server(pub, r)

X = 12
Y= 11
X_encrypted = encrypt(pub, X)
Y_encrypted = encrypt(pub, Y)
server = Server(pub, X_encrypted, Y_encrypted)

d_encrypted = server.calculateValues()
# print(d_encrypted)

d_cap_encrypted = client.initialize(d_encrypted)

dgk = DGK(client, server)
encrypted_lbda = dgk.protocol()
print("\nEncrypted_lambda =", encrypted_lbda)
# print(decrypt(priv, pub, encrypted_lbda))

b_encrypted = server.final_calculation(encrypted_lbda, d_cap_encrypted)
print("\nFinal output (without raising to power 2^-L): ")
# print("b_encrypted: " ,b_encrypted)
print("Decrypted value of b_encrypted i.e. b =",decrypt(priv, pub, b_encrypted))
# print(decrypt(priv, pub, e_add(pub, encrypted_length, inverse_encrypted_length)))

