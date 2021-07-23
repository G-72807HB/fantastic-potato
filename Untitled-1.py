# C&C - SERVER

" greeter "
import sys

# import library socket karena akan menggunakan IPC socket
import socket

def comm(task):
    # definisikan IP untuk binding
    IP = "128.0.0.30"

    # definisikan port untuk binding
    PORT = 5555

    # definisikan ukuran buffer untuk menerima pesan
    B_SIZE = 1024

    # buat socket (bertipe UDP atau TCP?)
    d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    d.settimeout(15)

    # lakukan binding ke IP dan port
    d.bind((IP, PORT))

    # lakukan listen
    d.listen(1)

    #  siap menerima koneksi
    cent, _ = d.accept()

    # buka file bernama "file_didownload.txt
    # masih hard code, file harus ada dalam folder yang sama dengan script python
    f = open(task, "rb")

    try:
        # baca file tersebut sebesar buffer 
        line = f.read(B_SIZE)
            
        # selama tidak END OF FILE; pada pyhton EOF adalah b''
        while line != b'':
            # kirim hasil pembacaan file dari server ke client
            cent.send(line)
                
            # baca sisa file hingga EOF
            line = f.read(B_SIZE)
                
    finally:
        # print ("end sending")
            
        # tutup file jika semua file telah  dibaca
        f.close()

    # tutup socket
    d.close()

    # tutup koneksi
    cent.close()

# definisikan alamat IP binding  yang akan digunakan 
TCP_IP = "128.0.0.30"

# definisikan port number binding  yang akan digunakan 
TCP_PORT = 5005

# definisikan ukuran buffer untuk mengirimkan pesan
BUFFER_SIZE = 1024

# buat socket bertipe TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(60)

# lakukan bind
s.bind((TCP_IP, TCP_PORT))

# server akan listen menunggu hingga ada koneksi dari client
s.listen()

# lakukan loop forever
while 1:
    # menerima koneksi
    conn, _ = s.accept()
        
    # menerima data berdasarkan ukuran buffer
    data = conn.recv(BUFFER_SIZE)
    
    # menampilkan pesan yang diterima oleh server menggunakan print
    print("[{0}] joined".format(data.decode()))
    
    # mengirim kembali data yang diterima dari client kepada client
    conn.send(data)

    " send command "
    data = conn.recv(BUFFER_SIZE); hostname = data.decode()
    print("[{0}] ready".format(hostname))

    conn.send(str(len(sys.argv) - 1).encode())
    
    data = conn.recv(BUFFER_SIZE)
    print("[{0}] running".format(hostname))

    for i in range(len(sys.argv) - 1):
        task = sys.argv[i + 1]
        conn.send(task.encode())

        comm(task)

        data = conn.recv(BUFFER_SIZE)
        if data.decode() == "1":
            print("[{0}] {1} failed".format(hostname, task))
        else:
            print("[{0}] {1} succeed".format(hostname, task))

    conn.send(hostname.encode())
    print("[{0}] returning".format(hostname))
    
    " check results "
    data = conn.recv(BUFFER_SIZE)
    print("[{0}] left".format(hostname))

# tutup koneksi
conn.close()