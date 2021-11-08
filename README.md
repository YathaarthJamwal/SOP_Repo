The file bit-MIN_modified_paillier.py contains the code for bit-MIN using the modified Paillier encryption scheme.
The file bit-MIN.py contains the implementation using the usual Paillier encryption scheme.

Description of some basic functions:

e_add() is used multiply two ciphertexts, which results in addition of corresponding plaintexts.
e_multiply() is used to raise a ciphertext to a power, which results in multiplication of plaintext with the value of the power.
e_add_constant() is similar to e_add(), but adds a constant directly.
invmod() calculates the inverse under the given modulus.

bit-MIN_modified_paillier.py contains definitions of Client and Server classes, so as to simulate the fact that these two should work independently in the target scenario.

The file dgk_protocol.py contains a definition of a class DGK, which takes a client and server as input, and uses some of their methods to perform the dgk protocol, which is a sub protocol of the bit-MIN protocol.

To get an output, one just needs to change the values of X and Y towards the end of bit_MIN_modified_paillier.py and then run "python3 bit-MIN_modified_paillier.py" on the command line.

