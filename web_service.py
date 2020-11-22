import asyncio
import websockets
import json
from uuid import uuid4

from game.node_manager import NodeManager
from game.trotter import Player, Account, Transaction
from game_runner import create_game_runner


class Server:
    def __init__(self, handlers=None):
        self.__handlers = {} if handlers is None else handlers
        self.__socket_ids = {}

    def socket_id(self, websocket):
        socket_id = self.__socket_ids.get(websocket, str(uuid4()))
        self.__socket_ids[websocket] = socket_id
        return socket_id

    def add_handler(self, id, func):
        self.__handlers[id] = func

    async def handle(self, websocket, path):
        async for message in websocket:
            data = json.loads(message)
            try:
                handler = self.__handlers[data["type"]]
                await handler(data, websocket, path)
            except Exception as e:
                print(e)

    def serve(self, host="localhost", port=8765):
        return websockets.serve(self.handle, host, port)


def create_server():
    node_manager = NodeManager.from_paths([
        "data/defaults.yaml",
        "data/polacks.yaml",
        "data/barkeep.yaml",
        "data/uppsala.yaml",
        "data/stockholm.yaml"
    ])

    runners = {}
    server = Server()

    @server_handler(server)
    def init(data, id):
        name = data.get("name", "Dirk Smallwood")
        initial_funds = Transaction(1000)
        player = Player(
            name=name,
            account=Account([initial_funds]),
            skills=[]
        )
        runners[id] = create_game_runner(
            node_manager=node_manager,
            player=player,
        )
        return {
            "name": player.name,
            "account_balance": player.account.balance
        }

    @server_handler(server)
    def version(data, id):
        return runners[id].version()

    @server_handler(server)
    def content(data, id):
        return runners[id].content()

    @server_handler(server)
    def player(data, id):
        return runners[id].player()

    @server_handler(server)
    def game(data, id):
        return runners[id].game()

    @server_handler(server)
    def action(data, id):
        return runners[id].action(data.get("action"))

    return server


def server_handler(server):
    def _server_handler(func):
        async def _handler(data, websocket, path):
            socket_id = server.socket_id(websocket)
            try:
                response = func(data, socket_id)
                blob = json.dumps({
                    "_id": data.get("_id", None),
                    "response": response
                })
            except Exception as e:
                blob = json.dumps({
                    "_id": data.get("_id", None),
                    "error": str(e)
                })
            await websocket.send(blob)

        server.add_handler(func.__name__, _handler)
        return func
    return _server_handler


if __name__ == "__main__":
    server = create_server()

    asyncio.get_event_loop().run_until_complete(server.serve())
    asyncio.get_event_loop().run_forever()
    print("All done")
