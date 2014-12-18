#!/usr/bin/env pypenv
# -*- Mode: Python; tab-width: 4; py-indent-offset: 4; -*-

import os, string
from sys import *
from pype import *
from config import *
from pype_aux import *
from sprite import *

import optix

if len(sys.argv) < 3:
    sys.stderr.write('usage: %s configfile lcd|crt [gamma]\n' % sys.argv[0])
    sys.stderr.write('  - configfile is something like ~/.pyperc/Config.foo\n')
    sys.stderr.write('  - lcd or crt specifies what to calibrate\n')
    sys.stderr.write('  - [optional] gamma is for validating an old\n')
    sys.stderr.write('    by rerunning the calibration at specified gamma\n')
    sys.exit(1)

configfile = Config(sys.argv[1])
bugmode = sys.argv[2]
if len(sys.argv) == 4:
    gammatest = float(sys.argv[3])
else:
    gammatest = None

w = configfile.iget('DPYW')
h = configfile.iget('DPYH')
bits = 32
dpy = configfile.get('SDLDPY')
#flags = DOUBLEBUF | FULLSCREEN
flags = DOUBLEBUF

if (flags & FULLSCREEN) and os.geteuid != 0:
    sys.stderr.write('WARNING: no full screen mode w/o root access!\n')

try:
    dtp = optix.Optix()
except optix.OptixMissing:
    sys.stderr.write('Attach calibration bug and try again\n')
    sys.exit(1)

if bugmode == 'lcd':
    dtp.set_mode(lcd=1)
else:
    dtp.set_mode(lcd=0)
    
if dpy is None:
    dpy = os.environ['DISPLAY']

sys.stderr.write('specs: %dx%d %dbits dpy=%s\n' % (w, h, bits, dpy,))

dtp.clear()

sys.stderr.write("Calibrate offsets 1st? [yN] ")
sys.stderr.flush()
x=sys.stdin.readline()
if x[0] == 'y' or x[0] == 'Y':
    sys.stderr.write('Place calibration bug on an opaque surface:\n')
    sys.stderr.write('and then hit return >>')
    sys.stderr.flush()
    sys.stdin.readline()
    sys.stderr.write('please wait -- this will take ~10 secs...\n');
    dtp.selfcalibrate()
    sys.stderr.write('Done!\n');

sys.stderr.write('Attach calibration bug to monitor (under framebuffer)\n')
sys.stderr.write('and hit return >>')
sys.stderr.flush()
sys.stdin.readline()

fb = FrameBuffer(dpy, w, h, bits, flags, sync=0)

if gammatest:
    fb.set_gamma(gammatest, gammatest, gammatest)

sys.stderr.write('.....calibration is running....\n')

print "%% bugmode=%s" % bugmode
print "%% gammatest=%s" % gammatest
print "%% columns: |r|g|b|Y|x|y|"

R = range(0,255,10)
if R[-1] != 255:
    R.append(255)

for l in R:
    for (rw,gw,bw) in ((1,0,0), (0,1,0), (0,0,1), (1,1,1)):
        r, g, b = rw*l, gw*l, bw*l
        fb.clear(color=(r, g, b))
        fb.flip()
        (Y, x, y) = dtp.Yxy()
        print r, g, b, Y, x, y
        sys.stderr.write("%s -> %s\n" % ((r,g,b), (Y,x,y)))
        sys.stdout.flush()
