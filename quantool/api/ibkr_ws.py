import websocket
import time
import ssl


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("## CLOSED! ##")


def on_open(ws):
    print("Opened Connection")
    time.sleep(3)
    # market data
    conids = ["265598", "8314"]
    for conid in conids:
        ws.send("smd+" + conid + '+{"fields":["31","84","86"]}')

    # # orders
    # print("Opened Connection")
    # time.sleep(3)
    # ws.send('sor+{}')


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        url="wss://192.168.8.9:5001/v1/api/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
