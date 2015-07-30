from py2neo.server import GraphServer
import sys
sys.path.insert(0, '../talk')
sys.path.insert(0, '../../talk')
import db

def connect():
    server = GraphServer("../../../neo4j")
    print "Checking existing connections to movie line database..."
    server.stop()
    print "Done."
    print "Connecting to movie lines database..."
    server.start()
    print "Connected."
    print "Deleting previous histo"
    db.clean_histo()
    print "Done."

def disconnect():
    server = GraphServer("../../../neo4j")
    print "Disconnecting from movie lines database..."
    server.stop()
    print "Disconnected."
