#!/usr/bin/env pypenv
# -*- Mode: Python; tab-width: 4; py-indent-offset: 4; -*-

# NOTE: THIS NEEDS THE >= 1.0 pyusb library (not the old c-based version)

VENDOR_ID  = 0x0765
PRODUCT_ID = 0xD094
BUFSIZE    = 8*16
TIMEOUT    = 20000

import sys, string

class OptixMissing(Exception): pass

class Optix():
    def __init__(self):
        import usb.core
        import usb.util
        self.dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        if self.dev is None:
            raise OptixMissing
        
        self.dev.set_configuration()
        cfg = self.dev.get_active_configuration()
        intf = cfg[(0,0)]
        self.ep_r = usb.util.find_descriptor(intf,
                            custom_match = \
                            lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)
        self.ep_w = usb.util.find_descriptor(intf,
                            custom_match = \
                            lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
        self.dev.set_interface_altsetting(intf.bInterfaceNumber, intf.bAlternateSetting)

        # will generate error if not attached..
        self.read('010aCF')

    def read(self, cmd):
        self.ep_r.clear_halt()
        self.ep_w.clear_halt()
        self.dev.write(self.ep_w.bEndpointAddress, cmd+'\r', TIMEOUT)
        return self.dev.read(self.ep_r.bEndpointAddress, BUFSIZE, TIMEOUT)

    def XYZ(self):
        s = self.read('0201RM')
        s = string.join(map(chr, s), '')
        s = string.strip(string.split(s, '\r')[0])
        return map(float,string.split(s)[1::2])
    
    def Yxy(self):
        s = self.read('0301RM')
        s = string.join(map(chr, s), '')
        s = string.strip(string.split(s, '\r')[0])
        return map(float,string.split(s)[1::2])

    def set_mode(self, lcd=1):
        if lcd:
            self.read('0216CF')
        else:
            self.read('0116CF')

    def selfcalibrate(self):
        print "wait...",
        self.read('CO')
        print "done\n",
        
    def clear(self):
        self.read('CE')
        self.read('CE')
        self.read('CE')

if __name__ == '__main__':
    o = Optix()
    o.clear()
    sys.stdout.write('Ready? ')
    sys.stdin.readline()
    o.selfcalibrate()
    o.clear()
    print o.read('010aCF')
    print o.Yxy()
