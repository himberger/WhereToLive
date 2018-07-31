#!/usr/bin/python
import SimpleHTTPServer
import SocketServer
import re
import numpy as np
import scipy
from skimage import io
import os.path
import matplotlib
                
PORT = 8001


# This class will handles any incoming request from
# the browser
class myHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

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


   
    def do_GET(self):
        if self.path[:7] == "/query?":
            # query time
            p = self.query_parser()
            if len(p) != 0:
                self.path=self.path[:6] + '_'  + self.path[8:]+'.png'                
                if not os.path.isfile(self.path):
                    output = (storeImage['ID1']>-1000).astype(int)
                    for key in p.keys():
                        output = np.add(output, storeImage[key]> p[key])
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

storeImage={'ID1':np.array(io.imread("maps/wc2.0_bio_10m_01.tif")), 
            'ID2':np.array(io.imread("maps/wc2.0_bio_10m_07.tif")), 
            'ID3':np.array(io.imread("maps/wc2.0_bio_10m_12.tif"))}

httpd = SocketServer.TCPServer(("", PORT), myHandler)

print "serving at port", PORT
httpd.serve_forever()
