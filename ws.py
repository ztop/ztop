from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory

# On connect, add clients to the clients set; remove them on disconnect
clients = set() 
class ProcessServerProtocol(WebSocketServerProtocol):
   def onConnect(self, request):
      print("Client connecting: {}".format(request.peer))
 
   def onOpen(self):
      print("WebSocket connection open.")
      clients.add(self)
 
   def onClose(self, wasClean, code, reason):
      print("WebSocket connection closed: {}".format(reason))
      clients.remove(self)

# Gets process information and broadcasts to connected clients
import psutil
import json
def poll():
    procs = []
    for p in psutil.process_iter():
        try:
            procs.append(p.as_dict())
        except Exception, e:
            pass

    msg = json.dumps(procs)
    for c in clients:
        c.sendMessage(msg)

if __name__ == '__main__':
    import sys
 
    from twisted.python import log
    from twisted.web.server import Site
    from twisted.web.static import File
    from twisted.internet import reactor
    from twisted.internet.task import LoopingCall
 
    log.startLogging(sys.stdout)
 
    factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
    factory.protocol = ProcessServerProtocol
 
    # Polll and broadcast every second
    lc = LoopingCall(poll)
    lc.start(1)

    # WebSockets on port 9000, static files on 8000
    reactor.listenTCP(9000, factory)
    reactor.listenTCP(8000, Site(File('./client')))
    reactor.run()
