#!/usr/bin/env python

import asyncio
import json
import websockets
from websockets.server import WebSocketServerProtocol
from src.comms.consumer_message import ManagerConsumerMessage, ManagerConsumerMessageException
from src.manager.manager import Manager
from uuid import uuid4

class SimpleConsumer:

    def __init__(self, host, port):
        from src.manager.manager import Manager

        """
        Initializes a new SimpleConsumer
        @param host: host for connections, '0.0.0.0' to bind all interfaces
        @param port: port for connections
        """
        self.server = None
        self.client = None
        self.host = host
        self.port = port
        self.manager = Manager(consumer=self)

    async def reject_connection(self, websocket: WebSocketServerProtocol):
        """
        Rejects a connection
        @param websocket: websocket
        """
        await websocket.close(1008, "This RADI server can't accept more than one connection")

    def parse_msg(self,msg):

        if (type(msg)== bytes):
            data = msg.decode('utf-8')
            print("cmd: ","load")
            print("data: ",data)
        else:
            event = json.loads(msg)
            cmd = event["cmd"]
            data = event["data"]
            print("cmd: ",cmd)
            print("data: ",None)

        self.msg_id = self.msg_id + 1
        id = str(self.msg_id)

        return id, cmd, data

    async def handler(self, websocket: WebSocketServerProtocol):

        # save websocket as self.client if there is not clietn already connected
        if (self.client is not None and websocket != self.client):
            print("Client already connected, rejecting connection")
            await self.reject_connection(websocket)
        else:
            self.client = websocket

        # if client has disconnected reset manager and stablish self.client as None
        if (self.client and self.client.closed):
            print("Client disconnected, machine state reset")
            self.manager.reset()
            self.client = None
            return

        async for websocket_message in websocket:
            try:
                s = json.loads(websocket_message)
                message = ManagerConsumerMessage(**s)
                await self.manager.trigger(message.command, data=message.data or None)
                
                response = {"message": f"Exercise state changed to {self.manager.state}"}
                await websocket.send(str(message.response(response)))

            except:
            




async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever
    
if __name__ == "__main__":
    asyncio.run(main())