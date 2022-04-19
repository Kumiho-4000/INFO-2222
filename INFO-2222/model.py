'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
from cmath import log
from http import server
from tkinter.tix import Tree
import view
import random
import csv
import rsa
from Crypto.Hash import MD5
import string

# Initialise our views, all arguments are defaults for the template
page_view = view.View()

# generate salt
def generate_random_string(size):
        res = []
        ascii_set = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
        ascii_set_length = len(ascii_set)
        for i in range(size):
            res.append(ascii_set[random.randint(0, ascii_set_length - 1)])
        
        return "".join(res)


#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")

#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # By default assume good creds
    login = True

    # Load private key
    with open('private.pem','rb+') as privatefile:
        p = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(p)
    # Decrypto username & password
    plain_username = rsa.decrypt(username, privkey)
    # Decrypto password
    plain_password = rsa.decrypt(password, privkey)

    csv_reader = csv.reader(open("database/users.csv"))

    # Case 1: user not exist
    err_str = "No user"

    for line in csv_reader:
        # Found user
        if line[0] == plain_username:
            salt = line[1]
            hashed = line[2]
            hashedinput = MD5.new((plain_password + salt).encode()).hexdigest()
            if hashed == hashedinput:
                login = True
            else:
                login = False
                # Case2: wrong password
                err_str = "Wrong password"

        
    if login: 
        return page_view("valid", name=username)
    else:
        return page_view("invalid", reason=err_str)

#-----------------------------------------------------------------------------
# Signup
#-----------------------------------------------------------------------------

def signup_form():
    return page_view("signup")


def signup_check(username, password):

    csv_reader = csv.reader(open("database/users.csv"))

    # Case 1: If this username had been used by another user
    for line in csv_reader:
        if line[0] == username:
            err_str = "username had been ouccpied"
            return page_view("invalid", reason=err_str)


    # Case 2: If this username is available
    # Load private key
    with open('private.pem','rb+') as privatefile:
        p = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(p)

    # decrypt password by private key
    plaintext = rsa.decrypt(password, privkey)
    
    # generate salt
    salt = generate_random_string(128)

    # Gain hashed value
    hashed = MD5.new((plaintext + salt).encode()).hexdigest()

    with open("database/users.csv", 'a') as f:
        # There is no firend in the list when you signup
        f.write(username + ',' + salt + ',' + hashed + ', ')
        reason = "Signup successfully"
        return page_view("signup_successfully", reason=err_str)

#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())



# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass

#-----------------------------------------------------------------------------
# Send keys
#-----------------------------------------------------------------------------

# Return server's private key
def send_public_key():
    with open('keys/public.pem','rb+') as f:
        publickey = f.read()

    return publickey

# Return cert
def send_server_cert():
    with open('cert/server.crt', 'rb+') as f:
        cert = f.read()
    return cert

# Return server key
def send_server_key():
    with open('cert/server.key', 'rb+') as f:
        serverkey = f.read()
    return serverkey

# Return sign
def send_sign():
    with open('cert/server.crt', 'r') as f:
        cert = f.read()

    # Load private key
    with open('keys/private.pem','rb+') as f:
        p = f.read()
    privkey = rsa.PrivateKey.load_pkcs1(p)

    signature = rsa.sign(bytes(cert, "utf-8"), privkey, "SHA-256")
    return signature


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)