import socket
import threading
from logging import getLogger

LOGGER = getLogger()


class Server:
    def __init__(self) -> None:
        pass

    def start(self, port):
        LOGGER.info(f"--- Start(port = {port}) ---")

        # ソケットを生成する。
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # ソケットレベルとデータタイプを設定する。
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # サーバーは複数ipを使っているPCの場合はIPを設定して、そうではない場合はNoneや''で設定する。
        # ポートはPC内で空いているポートを使う。cmdにnetstat -an | find "LISTEN"で確認できる。
        server_socket.bind(("", port))

        # Ctrl + cを受け取ることができるように
        server_socket.settimeout(20)

        # server設定が完了すればlistenを開始する。
        server_socket.listen()

        try:
            # サーバーは複数クライアントから接続するので無限ループを使う。
            while True:
                try:
                    # clientから接続すればacceptが発生する。
                    # clientソケットとaddr(アドレス)をタプルで受け取る。
                    client_socket, addr = server_socket.accept()

                    # スレッドを利用してclient接続を作って、またaccept関数に行ってclientを待機する。
                    th = threading.Thread(target=self.binder, args=(client_socket, addr))
                    th.daemon = True

                    # スレッド開始
                    th.start()
                except socket.timeout:
                    pass

        except Exception as e:
            LOGGER.error(e)
        finally:
            # エラーが発生すればサーバーソケットを閉める。
            server_socket.close()

    def binder(self, client_socket, addr):
        """_summary_
        binder関数はサーバーからacceptしたら生成されるsocketインスタンスを通ってclientから
        データを受信するとecho形で再送信するメソッドだ。
            Args:
                client_socket (_type_): _description_
                addr (_type_): _description_
        """
        # コネクションになれば接続アドレスを出力する。
        LOGGER.info(f"Connected by {addr}")
        try:
            # 接続状況でクライアントからデータ受信を待つ。
            # もし、接続が切れちゃうとexceptが発生する。
            while True:
                # socketのrecv関数は連結されたソケットからデータを受信を待つ関数だ。最初に4byteを待機する。
                data = client_socket.recv(4)
                # 最初4byteは転送するデータのサイズだ。そのサイズはlittleエンディアンでbyteからintタイプに変換する。
                # C#のBitConverterはbigエンディアンで処理する。
                length = int.from_bytes(data, "big")
                # データを受信する。上の受け取ったサイズほど
                data = client_socket.recv(length)
                # 受信されたデータをstr形式でdecodeする。
                msg = data.decode()
                # 受信されたメッセージをコンソールに出力する。
                LOGGER.info(f"Received from {addr} {msg}")

                # 受信されたメッセージの前に「echo:」という文字を付ける。
                msg = "echo : " + msg
                # バイナリ(byte)タイプに変換する。
                data = msg.encode()
                # バイナリのデータサイズを計算する。
                length = len(data)
                # データサイズをlittleエンディアンタイプのbyteに変換して転送する。(※これがバグかbigを入れてもlittleエンディアンで転送する。)
                client_socket.sendall(length.to_bytes(4, byteorder="big"))
                # データをクライアントに転送する。
                client_socket.sendall(data)

        except KeyboardInterrupt:
            LOGGER.warn("KeyboardInterrupt")
        except:
            # 接続が切れちゃうとexceptが発生する。
            LOGGER.info(f"except : {addr}")
        finally:
            # 接続が切れたらsocketリソースを返却する。
            client_socket.close()
