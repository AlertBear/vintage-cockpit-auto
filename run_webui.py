#!/usr/bin/python2.7
from run import run_test
from SimpleXMLRPCServer import SimpleXMLRPCServer


if __name__ == "__main__":
    server = SimpleXMLRPCServer(("0.0.0.0", 9090))
    print "Listening on port 9090..."
    server.register_function(run_test, "run01")
    server.serve_forever()
