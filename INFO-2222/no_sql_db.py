import rsa
from Crypto.Hash import MD5
import random
import string

class Table():
    def __init__(self, table_name, table_fields):
        self.entries = []
        self.fields = table_fields
        self.name = table_name
   
        # Create csv file and write fields
        with open("database/" + self.name + ".csv", "w") as f:
            fields = ""
            for i in (table_fields):
                fields = fields + i + ','
            fields = fields[:len(fields) - 1]
            fields = fields + '\n'

            f.write(fields)
        return

    # Add new entry into table
    # Users(True): Personal information for a new user
    # Msgs(False): New message
    def add_users_entry(self, username, salt, hashvalue, firendlist):

        with open("database/" + self.name + ".csv", "a") as fa:
            fa.write(username + ',' + salt + ',' + hashvalue)
        
        fa = open("database/" + self.name + ".csv", "a")
        for i in firendlist:
            fa.write(',' + i)
        
        fa.write('\n')
        fa.close()
        
    # Search specific line
    def search_in_table(self, username):
        with open("database/" + self.name + ".csv", "r") as f:
            lines = f.readlines()

            for line in lines:
                info = line.split(',', 3)
                # info: username, salt, hashvalue, friendlist
                if info[0] == username:
                    return info
        return





class Bin():
    def __init__(self, username, caller):
        self.digest = username + caller
        with open("database/" + self.digest + ".bin", "w") as f:
            f.write('')
    
    def add_line(self, ecrypto):
        with open("database/" + self.digest + ".bin", "ab") as f:
            f.write(ecrypto)





class DB():
    def __init__(self):
        # Tables dictionary
        self.tables = {}

        self.fields_users = ["username", "salt", "hashvalue", "friendlist"]
        self.fields_msgs = []

        # Setup users table
        self.add_table('users')
        return

    # Store user login message and friend list
    def add_table(self, table_name):
        table = Table(table_name, self.fields_users)
        self.tables[table_name] = table
        return

    # Store message
    def add_bin(self, username, caller):
        bin = Bin(username, caller)
        self.tables[username + caller] = bin 
        
        return





# if __name__ == '__main__':
#     db = DB()
#     ascii_set = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
#     ascii_set_length = len(ascii_set)

#     def generate_random_string(size):
#             res = []
#             for i in range(size):
#                 res.append(ascii_set[random.randint(0, ascii_set_length - 1)])
            
#             return "".join(res)

#     msg = "123"
#     salt = generate_random_string(128)
#     hashed = MD5.new((msg + salt).encode()).hexdigest()
#     ls = ["Bob", "Carry"]
#     db.tables["users"].add_users_entry("Alice", salt, hashed, ls)

#     msg = '234'
#     salt = generate_random_string(128)
#     hashed = MD5.new((msg + salt).encode()).hexdigest()
#     ls = [" "]
#     db.tables["users"].add_users_entry("Bob", salt, hashed, ls)

#     db.add_bin("Alice", "Bob")
    
#     plaintext = "1 2, 3"
#     # Load public key
#     with open('keys/public.pem','rb+') as publickfile:
#         p = publickfile.read()
#     pubkey = rsa.PublicKey.load_pkcs1(p)
#     print('**********公钥已导入,开始RSA加密**********')

#     # Encrypt text
#     crypto = rsa.encrypt(bytes(plaintext, "utf_8"), pubkey)

#     db.tables["AliceBob"].add_line(crypto)