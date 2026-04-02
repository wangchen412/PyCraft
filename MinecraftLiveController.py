import asyncio
import websockets
import json
import uuid

class MinecraftLiveController:
    def __init__(self, host="0.0.0.0", port=6464):
        self.host = host
        self.port = port
        self.websocket = None
        self.queue = asyncio.Queue()

    def _make_cmd(self, cmd):
        return json.dumps({
            "header": {"version": 1, "requestId": str(uuid.uuid4()), "messagePurpose": "commandRequest", "messageType": "commandRequest"},
            "body": {"version": 1, "commandLine": cmd, "origin": {"type": "player"}}
        })

    async def handler(self, websocket):
        print(f"Game connected! Address: {websocket.remote_address}")
        self.websocket = websocket
        try:
            while True:
                cmd = await self.queue.get()
                await self.websocket.send(self._make_cmd(cmd))
                self.queue.task_done()
        except Exception as e:
            print(f"Disconnected: {e}")
        finally:
            self.websocket = None

    async def start_server(self):
        async with websockets.serve(self.handler, self.host, self.port, ping_interval=None):
            print(f"Server ready, port: {self.port}")
            while True:
                await asyncio.sleep(3600) 

    def set_block(self, x, y, z, block_name, tile_data=0):
        self.run_cmd(f"setblock {x} {y} {z} {block_name} {tile_data}")

    def fill(self, x1, y1, z1, x2, y2, z2, block_name):
        self.run_cmd(f"fill {x1} {y1} {z1} {x2} {y2} {z2} {block_name}")

    def spawn(self, entity_type, x, y, z):
        self.run_cmd(f"summon {entity_type} {x} {y} {z}")

    def run_cmd(self, command):
        asyncio.get_event_loop().create_task(self.queue.put(command))

    def set_blocks(self, points, block_name, tile_data=0, delay=0.05):
        self.set_blocks_with_select_func(points, lambda: block_name, tile_data, delay)

    def set_blocks_with_select_func(self, points, block_func, tile_data=0, delay=0.05):
        ps = set()
        for p in points:
            ps.add((int(p[0]), int(p[1]), int(p[2])))
        points = list(ps)
        points.sort(key=lambda x: x[1])

        async def _internal_worker():
            print(f"Start building: {len(points)} blocks...")
            for i, (x, y, z) in enumerate(points):
                block_name = block_func(x, y, z)
                self.set_block("~" + str(int(x)), "~" + str(int(y)), "~" + str(int(z)), block_name, tile_data)
                await asyncio.sleep(delay)
                if (i + 1) % 100 == 0:
                    print(f" >> progress: {i + 1}/{len(points)}")
            print(f"Completed!")
        asyncio.create_task(_internal_worker())

def StartServer():
    mlc = MinecraftLiveController()
    server_task = asyncio.create_task(mlc.start_server())
    return mlc