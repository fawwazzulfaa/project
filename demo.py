# fawwaz zulfaa - 2301955844
import sys 
from getopt import getopt
import socket
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import random, string

# generate key dari string huruf + string angka yang di randomize - 16 karakter
def generate_key():
    key = str()
    
    for _ in range(16):
        key += random.choice(string.ascii_lowercase + string.digits)
    return key


# menggunakan aes 256 cfb
def encrypt(password, message):
    # hashing key pakai sha256 (hashing)
    private_key = hashlib.sha256(password.encode()).digest()
    # dapetin iv (initialization vector) value IV yang random dari block size aes.
    iv = Random.new().read(AES.block_size)
    # buat aes enkripsi baru dengan privite key yang di input
    # dengan mode aes CFB, iv yang baru saja di randomize, ...
    cipher = AES.new(private_key, AES.MODE_CFB, iv, segment_size=128)
    # kemudian inisialissai digunkaan untuk meng encripyt message
    enc = cipher.encrypt(message.encode())
    # lalu IV + hasil dari enkripsi di encode menggunakan base64 
    return base64.b64encode(iv + enc).decode()


def decrypt(password, message):
    # hashing dulu pakai sha256
    private_key = hashlib.sha256(password.encode()).digest()
    # disini message di decode menggunakan base 64
    message = base64.b64decode(message)
    # disini mendapatkan IV dan message enkripsi 
    iv, enc = message[:16], message[16:]
    # kita inisialissai kembali aes enkripsi dengan password mode iv segmen yang sama 
    cipher = AES.new(private_key, AES.MODE_CFB, iv, segment_size=128)
    # mengemnalikan hasil decripsi nya
    return (cipher.decrypt(enc)).decode()

ip =""
port = 0
is_server= False

def handle_client(connection, client_address):
    pass

def run_server():
    print("server is trying to listening")
    #bikin socket
    #parameternya : tipe address(Ipv4) , protokol(Tcp)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    #listen
    server.listen()
    print("server is listening")
    connection, client_address =server.accept()
    print(f"connected with client at{client_address}")
    while True:
    #accept
        message = input("input message['exit' to close connection]: ")
        #kalau exit -> dead
        if message == "exit":
            server.close()
            break
        # intial pass dengan generate key yang sudah di randomize  
        password = generate_key()
        # pada message_enc = berisi key yang sudah di randomize + pesan dan key password yang di encrypt
        message_enc = password + ':' + encrypt(password, message)
        print(message_enc)
        connection.send(message_enc.encode())
        #terima response/result dari targetnya
        password, result = connection.recv(1024).decode().split(':')
        result_dec = decrypt(password, result)
        print(result_dec)



def run_client():
    print("client is trying to listening")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client.connect((ip,port))
    while True:
        # result = client.recv(1024).decode()
        # print(result)
        password, result = client.recv(1024).decode().split(':')    
        result_dec = decrypt(password, result)
        print(result_dec)
        message = input("input message['exit' to close connection]: ")
        if message == "exit":
            client.close()
            break
        # initial pass dengan func generate_key yang sudah di randomize
        password = generate_key()
        # pada message_enc =    
        message_enc = password + ':' + encrypt(password, message)
        print(message_enc)
        client.send(message_enc.encode())

    


def main():
    global ip , port, is_server
    
    print(sys.argv[0:])
    print(sys.argv[1:])
    opts, _ = getopt(sys.argv[1:], "i:p:s",["ip=","port=", "server"] )
    print(opts)
    
    for opt, value in opts:
        print(f"{opt}:{value}")
        if opt == "-i" or opt == "--ip":
            ip=value
        elif opt == "-p" or opt =="--port":
            port = int(value)
        elif opt == "-s" or opt =="--server":
            is_server = True

    if ip == "":
        print("Ip must be filled !")
        exit()
    if port >2500 :
        print("Port must be between 2000 and 2500!")
        exit()
    if port <2000 :
        print("Port must be between 2000 and 2500!")
        exit()
    
    if is_server :
        run_server()
    else:
        run_client()



main()