#!/usr/bin/python
import SimpleHTTPServer
import SocketServer
import re
import numpy as np
import scipy
from skimage import io
import os.path
import matplotlib
import json
                
PORT = 8001


# This class will handles any incoming request from
# the browser
class myHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def query_parser(self):
        parsed = list()

        searches = re.split("&", self.path[7:])

        for q in range(len(searches)):  # iterate through number of search terms
            if "=" in searches[q]:
                sqs = re.split("_", searches[q])
                if len(sqs) != 2:
                    return list()
                else: # Normal processing
                    if sqs[1] in ["0", "1", "2"] and sqs[0] in [str(idx) for idx in range(len(storeImage))]:
                        sqs[1] = unicode(sqs[1], 'utf-8')
                        if not sqs[1].isnumeric():
                            return list()
                        else:  # It is numeric
                            parsed.append = [int(sqs[1]),int(sqs[1]),float(sqs[2])]
                    else:  # Not a known search type
                        return list()
            else:
                return list()

        return parsed


   
    def do_GET(self):
        if self.path[:7] == "/query?":
            # query time
            p = self.query_parser()
            if len(p) != 0:
                self.path=self.path[:6] + '_'  + self.path[8:]+'.png'                
                if not os.path.isfile(self.path):
                    output = (storeImage[0]>-1000).astype(int)
                    operations = [np.equal, np.greater, np.less]
                    for op in p:
                        output = np.add(output, operations[op[1]](storeImage[op[0]], op[2]))
                    output = output * 127 / (len(p)+1)
                    output = output+np.sign(output)*128
                    output = output+np.sign(output)*np.sign(output-255)*64
                    output_final = np.zeros([1080,2160,3],dtype='uint8')
                    colormap = 255*np.array(matplotlib._cm_listed.cmaps['viridis'].colors)
                    colormap[0,:] = [78,91,190]
                    for idx in range(3):
                        output_final[:,:,idx]=colormap[output,idx]
                    scipy.misc.imsave(self.path[1:],output_final)
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()
f = open('maps.json', 'r')
maps = json.loads(f.read())
f.close()
storeImage = [];
for map in maps:
    storeImage.append(np.array(io.imread("maps/"+map[1])))

httpd = SocketServer.TCPServer(("", PORT), myHandler)

print "serving at port", PORT
httpd.serve_forever()
