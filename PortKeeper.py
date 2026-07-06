import socket
import sys
import threading
import time

def get_valid_port():
    while True:
        try:
            user_input = input("Введите номер порта (1-65535): ").strip()
            port = int(user_input)
            if 1 <= port <= 65535:
                return port
            print("[-] Ошибка: Порт должен быть от 1 до 65535.")
        except ValueError:
            print("[-] Ошибка: Введите целое число.")
        except KeyboardInterrupt:
            print("\n[-] Выход.")
            sys.exit(0)

def get_protocol():
    while True:
        try:
            print("\nВыберите протокол:")
            print("1. TCP")
            print("2. UDP")
            print("3. Оба (TCP + UDP)")
            choice = input("Ваш выбор (1/2/3): ").strip()
            if choice == '1': return 'tcp'
            if choice == '2': return 'udp'
            if choice == '3': return 'both'
            print("[-] Ошибка: Выберите 1, 2 или 3.")
        except KeyboardInterrupt:
            print("\n[-] Выход.")
            sys.exit(0)

def listen_tcp(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(5)
        print(f"[+] TCP-порт {port} успешно открыт и ожидает соединений.")
        
        while True:
            client_socket, addr = server_socket.accept()
            print(f"[!] [TCP] Входящее подключение от {addr[0]}:{addr[1]}")
            client_socket.close()
    except Exception as e:
        print(f"[-] [TCP] Ошибка на порту {port}: {e}")
    finally:
        server_socket.close()

def listen_udp(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        server_socket.bind(('0.0.0.0', port))
        print(f"[+] UDP-порт {port} успешно открыт и готов принимать пакеты.")
        
        while True:
            data, addr = server_socket.recvfrom(1024)
            print(f"[!] [UDP] Получен пакет от {addr[0]}:{addr[1]} ({len(data)} байт)")
    except Exception as e:
        print(f"[-] [UDP] Ошибка на порту {port}: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    target_port = get_valid_port()
    proto = get_protocol()
    
    threads = []
    
    if proto in ('tcp', 'both'):
        t_tcp = threading.Thread(target=listen_tcp, args=(target_port,), daemon=True)
        threads.append(t_tcp)
        t_tcp.start()
        
    if proto in ('udp', 'both'):
        t_udp = threading.Thread(target=listen_udp, args=(target_port,), daemon=True)
        threads.append(t_udp)
        t_udp.start()
        
    print("\n[*] Чтобы закрыть программу и освободить порты, нажмите Ctrl+C")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[-] Завершение работы. Все порты освобождены.")
