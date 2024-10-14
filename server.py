import socket
import os
from faker import Faker

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

server_address = '/tmp/socket_file'

faker = Faker()

# 以前の接続が残っていた場合に備えて、サーバアドレスをアンリンク（削除）する。
try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

print('Starting up on {}'.format(server_address))

# サーバにソケットをバインド（接続）する。
sock.bind(server_address)

# ソケットが接続要求を待機するようにする。
sock.listen(1)

# 無限ループでクライアントからの接続を待ち続ける。
while True:
    # クライアントからの接続を受け入れる。
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # 無限ループでクライアントからのデータを待ち続ける。
        while True:
            # データを最大16バイトで受け取り、エンコードして表示。
            data = connection.recv(16)
            data_str = data.decode('utf-8')
            print('Received ' + data_str)
        
            # データがある場合、fakerでテキスト生成して返信。
            if data:
                response = faker.text()
                print('Response ' + response)
                connection.sendall(response.encode())
            
            # データがなければループ終了。
            else:
                print('no data from', client_address)
                break

    # 接続を閉じる。
    finally:
        print("Closing current connection")
        connection.close()