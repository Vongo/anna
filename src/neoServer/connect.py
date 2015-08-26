from py2neo.server import GraphServer
import sys
sys.path.insert(0, '../talk')
sys.path.insert(0, '../../talk')
import db

def connect():
    """
    Connects to the Neo4j server once and for all
    """
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
    """
    Disconnects from the server
    """
    server = GraphServer("../../../neo4j")
    print "Disconnecting from movie lines database..."
    server.stop()
    print "Disconnected."
