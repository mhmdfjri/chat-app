# server/websocket_server.py
import asyncio, json
import websockets

clients = {}

async def notify_users():
    users = [{"username": name, "avatar": avatar} for _, (name, avatar) in clients.items()]
    message = json.dumps({"type": "users", "users": users})
    await asyncio.gather(*(ws.send(message) for ws in clients))

async def handler(ws):
    try:
        hello = await ws.recv()  # format: {"username": "...", "avatar": "img.png"}
        data = json.loads(hello)
        clients[ws] = (data["username"], data["avatar"])
        await notify_users()

        async for msg in ws:
            broadcast_msg = json.dumps({"type": "message", "from": data["username"], "avatar": data["avatar"], "text": msg})
            await asyncio.gather(*(w.send(broadcast_msg) for w in clients))
    except:
        pass
    finally:
        if ws in clients:
            del clients[ws]
            await notify_users()

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket ready on ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())
