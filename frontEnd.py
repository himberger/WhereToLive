#!/usr/bin/python
# Web Handler from https://www.acmesystems.it/python_http
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import re
import numpy as np
import scipy
PORT_NUMBER = 8080
from skimage import io

# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):

    def query_parser(self):
        parsed = dict()

        searches = re.split("&", self.path[7:])

        for q in range(len(searches)):  # iterate through number of search terms
            if "=" in searches[q]:
                sqs = re.split("=", searches[q])
                if len(sqs) != 2:
                    return dict()
                else: # Normal processing
                    if sqs[0] in ["ID1", "ID2", "ID3"]:
                        sqs[1] = unicode(sqs[1], 'utf-8')
                        if not sqs[1].isnumeric():
                            return dict()
                        else:  # It is numeric
                            parsed[sqs[0]] = int(sqs[1])
                    else:  # Not a known search type
                        return dict()
            else:
                return dict()

        return parsed


    # Handler for the GET requests
    def do_GET(self):
        # Send the html message


        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.path)  # Main homepage
        elif self.path[:7] == "/query?":
            # query time
            p = self.query_parser()
            if len(p) != 0:
                # pass
                output = np.ones(np.shape(storeImage['ID1']),dtype=bool)
                for key in p.keys():
                    output = np.logical_and(output, storeImage[key]> p[key])
                scipy.misc.imsave('temp.png',output)
                f=open('temp.gif')
                self.send_response(200)
                self.send_header('Content-type','image/gif')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()

            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("ERROR: Query parsing was unsuccessful.")
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("WARNING: " + self.path + "was the unknown directory")
        return

try:
    storeImage={'ID1':np.array(io.imread("maps/wc2.0_bio_10m_01.tif")), 
                'ID2':np.array(io.imread("maps/wc2.0_bio_10m_07.tif")), 
                'ID3':np.array(io.imread("maps/wc2.0_bio_10m_12.tif"))}
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ', PORT_NUMBER

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()