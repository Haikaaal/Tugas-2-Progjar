import socket

def main():
    server_address = ('172.16.16.101', 45000)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(server_address)
        print("Terhubung ke server.")

        while True:
            command = input("Ketik perintah (TIME atau QUIT): ").strip().upper()

            if command not in ['TIME', 'QUIT']:
                print("Perintah tidak dikenali. Gunakan TIME atau QUIT.")
                continue

            sock.sendall((command + '\r\n').encode('utf-8'))

            response = sock.recv(1024)
            print("Respon dari server:", response.decode('utf-8').strip())

            if command == 'QUIT':
                print("Menutup koneksi.")
                break

    except Exception as e:
        print("Terjadi kesalahan:", e)

    finally:
        sock.close()

if __name__ == '__main__':
    main()
