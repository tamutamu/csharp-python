import socket
from logging import getLogger

LOGGER = getLogger(__name__)


class Client:
    def __init__(self, host) -> None:
        self.host = host

    def send(self, msg, port, doRecv=True):
        # ソケットを生成する。
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect関数でサーバーに接続する。
        client_socket.connect((self.host, port))

        # 10回のループでsend、receiveをする。
        for i in range(0, 1):
            # メッセージはhelloで送信
            # メッセージをバイナリ(byte)タイプに変換する。
            data = msg.encode()
            # メッセージのサイズを計算する。
            length = len(data)
            # データサイズをlittleエンディアンタイプに変換してサーバーに送信する。
            client_socket.sendall(length.to_bytes(4, byteorder="big"))
            # データを送信する。
            client_socket.sendall(data)

            if doRecv:
                # サーバーからデータサイズを受信する。
                data = client_socket.recv(4)
                # データ長さはbigエンディアンでintを変換する。(※これがバグかbigを入れてもlittleエンディアンで転送する。)
                length = int.from_bytes(data, "big")
                # データの長さを受信する。
                data = client_socket.recv(length)
                # データを受信する。
                msg = data.decode()
                # データをコンソールで出力する。
                # LOGGER.info("Received from : ", msg)

        # ソケットリソースを返却する。
        client_socket.close()


class LocalClient(Client):
    def __init__(self) -> None:
        super().__init__("127.0.0.1")
