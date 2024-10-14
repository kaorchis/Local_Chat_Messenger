import socket
import sys


# ドメイン：AF_UNIX、タイプ：SOCK_STREAMでTCP/IPソケット作成
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# サーバが待ち受けている特定の場所にソケットを設定
server_address = '/tmp/socket_file'
print('connecting to {}'.format(server_address))

# サーバ接続
try:
    sock.connect(server_address)
except socket.error as err:
    print(err)
    sys.exit(1)

# メッセージ授受
try:
    print('Type in what you would like to send to server.')
    print('Server reply to the client with a random message.')
    # コマンドラインからの入力を送信する。
    inputstr = input()
    message = inputstr.encode('utf-8')
    sock.sendall(message)

    # 応答待ち時間
    sock.settimeout(2)

    # サーバから応答があれば表示。なければ終了。
    try:
        while True:
            # サーバからのデータを最大32バイトで受け取る。
            data = str(sock.recv(32))

            if data:
                print('Server response: ' + data)
            else:
                break
    except(TimeoutError):
        print('Socket timeout, ending listening for server messages')

# 通信終了
finally:
    print('closing socket')
    sock.close()
