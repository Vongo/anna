from py2neo.server import GraphServer

def connect():
    server = GraphServer("../../../neo4j")
    print "Checking existing connections to movie line database..."
    server.stop()
    print "Done."
    print "Connecting to movie lines database..."
    server.start()
    print "Connected."

def disconnect():
    server = GraphServer("../../../neo4j")
    print "Disconnecting from movie lines database..."
    server.stop()
    print "Disconnected."
