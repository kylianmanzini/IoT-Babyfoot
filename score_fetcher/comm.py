#!/usr/bin/python3
import json
import logging
import re
import threading
import struct
import time
import binascii
from http.server import BaseHTTPRequestHandler, HTTPServer

from bluepy import btle

macs = ["58:BF:25:9C:B8:5A", "7C:9E:BD:3A:C8:7E"]
peripherals = [btle.Peripheral() for _ in range(len(macs))]
teamsName = ['team1_score', 'team2_score']

sem = threading.Semaphore()
resetRequest = [False, False]

scoreboard = {
    "team1_score" : 0,
    "team2_score" : 0
}

class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        global resetRequest
        sem.acquire()
        if re.search('/api/post/reset', self.path):
            length = int(self.headers.get('content-length'))
            #data = self.rfile.read(length).decode('utf8')

            # reset the scoreboard
            for key in scoreboard.keys() :
                scoreboard[key] = 0

            resetRequest[0] = True
            resetRequest[1] = True
            #resetCharacteristic1.write("\x01".encode('utf-8'), withResponse=True)
            #resetCharacteristic2.write("\x01".encode('utf-8'), withResponse=True)
            #print("Reset char val", int.from_bytes(resetCharacteristic.read(), byteorder='little'))

            # reset the scoreboard
            for key in scoreboard.keys() :
                scoreboard[key] = 0

            # re
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # Return json, even though it came in as POST URL params
            data = json.dumps(scoreboard).encode('utf-8')
            self.wfile.write(data)
        else:
            self.send_response(403)
        self.end_headers()
        sem.release()

    def do_GET(self):
        sem.acquire()
        if re.search('/api/get/score', self.path):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                # Return json, even though it came in as POST URL params
                data = json.dumps(scoreboard).encode('utf-8')
                self.wfile.write(data)
        else:
            self.send_response(403)
        self.end_headers()
        sem.release()


def goalFetching(peripheralIndex):
    dev = peripherals[peripheralIndex]
    mac = macs[peripheralIndex]

    dev.connect(mac)

    babyfootUUID = btle.UUID("fff0")
    babyfootService = dev.getServiceByUUID(babyfootUUID)

    goalUUID = btle.UUID("fff1")
    goalCharacteristic = babyfootService.getCharacteristics(goalUUID)[0]

    resetUUID = btle.UUID("fff3")
    resetCharacteristic = babyfootService.getCharacteristics(resetUUID)[0]

    try:
        goalNumberTeam = int.from_bytes(goalCharacteristic.read(), byteorder='little')
        scoreboard[teamsName[peripheralIndex]] = goalNumberTeam
        if(resetRequest[peripheralIndex] == True):
            print("Reset")
            resetCharacteristic.write("\x01".encode('utf-8'), withResponse=True)
            resetRequest[peripheralIndex] = False
        dev.disconnect()
    
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':

    print("Connecting to bluetooth sensor...")

    try:
        server = HTTPServer(('localhost', 8000), HTTPRequestHandler)
        web_server_thread = threading.Thread(target=server.serve_forever)
        web_server_thread.start()
        logging.info('Starting httpd...\n')

        while(1):
            threadBabyfoot1 = threading.Thread(target=goalFetching, args=(0,))
            threadBabyfoot1.setDaemon(True)

            threadBabyfoot2 = threading.Thread(target=goalFetching, args=(1,))
            threadBabyfoot2.setDaemon(True)

            threadBabyfoot1.start()
            threadBabyfoot1.join()

            threadBabyfoot2.start() 
            threadBabyfoot2.join()
            
    except KeyboardInterrupt:
        pass
    server.server_close()
    logging.info('Stopping httpd...\n')