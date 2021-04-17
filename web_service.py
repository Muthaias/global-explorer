import asyncio
import websockets
import json
import os
import sys
import glob
import traceback
from uuid import uuid4

from game.node_manager import NodeManager
from game.game import Game
from game.trotter import TrotterState
from game_runner import create_game_runner


class Store:
    def __init__(self, root):
        self.__root = root
        try:
            os.makedirs(root)
        except FileExistsError:
            pass

    def store(self, id, data):
        with open(self.__path(id), "w") as f:
            return json.dump(data, f, indent=2)

    def load(self, id):
        with open(self.__path(id), "r") as f:
            return json.load(f)

    def __path(self, id):
        return os.path.join(self.__root, id + ".json")


class Server:
    def __init__(self, handlers=None):
        self.__handlers = {} if handlers is None else handlers

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

    def serve(self, host="0.0.0.0", port=5000):
        return websockets.serve(self.handle, host, port)


def create_server(store, files):
    node_manager = NodeManager.from_paths(files)

    runners = {}
    server = Server()

    @server_handler(server)
    def init(data, id):
        if id not in runners:
            previous_game = None
            try:
                data = store.load(id)
                id_stack = data["stack"]
                state_data = data["state"]
                state = TrotterState.from_data(state_data, node_manager)
                previous_game = Game.from_id_stack(
                    id_stack=id_stack,
                    node_manager=node_manager,
                    state=state
                )
            except Exception:
                traceback.print_exc()
                pass
            runners[id] = create_game_runner(
                node_manager=node_manager,
                previous_game=previous_game,
            )
        return {
            "session_id": id
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
        action = data.get("action", None)
        game = runners[id].context.game
        result = runners[id].action(action)
        if game:
            id_stack = game.to_id_stack(node_manager)
            state_data = game.state.to_data(node_manager)
            store.store(id, {
                "stack": id_stack,
                "state": state_data,
            })
        return result

    return server


def server_handler(server):
    def _server_handler(func):
        async def _handler(data, websocket, path):
            try:
                session_id = data.get("_session_id", str(uuid4()))
                response = func(data, session_id)
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
    store = Store("./__store__")
    files = [
        "data/defaults.yaml",
        "data/polacks.yaml",
        "data/barkeep.yaml",
        "data/uppsala.yaml",
        "data/stockholm.yaml"
    ]
    if len(sys.argv) > 1:
        files = []
        for matches in sys.argv[1:]:
            files = [
                *files,
                *glob.glob(matches),
            ]

    print(files)
    server = create_server(store, files)

    asyncio.get_event_loop().run_until_complete(server.serve())
    asyncio.get_event_loop().run_forever()
    print("All done")
