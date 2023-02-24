#!/usr/bin/env python

import asyncio
import json
import websockets
from src.comms.consumer_message import ManagerConsumerMessage, ManagerConsumerMessageException

class SimpleConsumer:

    def __init__(self, host, port):

        self.server = None
        self.client = None
        self.host = host
        self.port = port
        self.msg_id = 0

    def parse_msg(self,msg):

            if (type(msg)== bytes):
                cmd = "load"
                data = msg.decode('utf-8')
            else:
                event = json.loads(msg)
                cmd = event["cmd"]
                data = None

            self.msg_id = self.msg_id + 1

            id = str(self.msg_id)
            cmd = str(cmd)
            data = str(data)

            return id, cmd, data

    async def handler(self,websocket):

        async for websocket_message in websocket:
            s = json.loads(websocket_message)
            message = ManagerConsumerMessage(**s)
            print(message)
            #msg_id,msg_cmd,msg_data = self.parse_msg(websocket_message)
            #print("id: ",msg_id, type(msg_id))
            #print("cmd: ",msg_cmd, type(msg_cmd))
            #print("data: ",msg_data, type(msg_data))
 #
            #msg_dict = {"id": msg_id, "cmd": msg_cmd, "data": msg_data}
            #print("dict: ",msg_dict, type(msg_dict),"\n")
#
            #message = ManagerConsumerMessage(**msg_dict)
            #print(message)

            # message1 = ManagerConsumerMessage(id=id, cmd=cmd, data=data)
            # print(message1)

    def start(self):
        """
        Starts the consumer and listens for connections
        """
        self.server = websockets.serve(self.handler, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    consumer = SimpleConsumer('0.0.0.0', 8001)
    consumer.start()