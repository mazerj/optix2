#!/usr/bin/env pypenv
# -*- Mode: Python; tab-width: 4; py-indent-offset: 4; -*-

import os, string
from sys import *
from pype import *
from config import *
from pype_aux import *
from sprite import *

try:
    import optix
except ImportError:
    sys.stderr.write('install optix python module\n')
    sys.exit(1)

if len(sys.argv) < 3:
    sys.stderr.write("""\
usage: gammacal config lcd|crt full|win outfile [gamma]
  config   - pype configfile (~/.pyperc/Config.HOST); - for default)
  lcd|crt  - one or the other (calibration bug cares)
  full|win - full screen or windowed mode
  outfile  - output file
  [gamma]  - optional gamma value for validation\n""");
    sys.exit(1)


if sys.argv[1] == '-':
    import socket
    h = socket.gethostname().split('.')[0]
    configfile = Config(os.environ['HOME'] + '/.pyperc/Config.' + h)
else:
    configfile = Config(sys.argv[1])

if sys.argv[2] == 'lcd':
    lcd = 1
else:
    lcd = 0

if sys.argv[3] == 'full':
    full = 1
else:
    full = 0
    
outfile = open(sys.argv[4], 'w')

if len(sys.argv) > 5:
    gammatest = float(sys.argv[5])
else:
    gammatest = None

w = configfile.iget('DPYW')
h = configfile.iget('DPYH')
dpy = configfile.get('SDLDPY')
if dpy is None:
    dpy = os.environ['DISPLAY']
    
try:
    dtp = optix.Optix()
    dtp.set_mode(lcd=lcd)
    dtp.clear()
except optix.OptixMissing:
    sys.stderr.write('Attach calibration bug and restart.\n')
    sys.exit(1)

sys.stdout.write("Calibrate offsets? [yN] "); sys.stdout.flush()
x = sys.stdin.readline()
if x[0] == 'y' or x[0] == 'Y':
    dtp.selfcalibrate(prompt=True)

if not full:
    fb = FrameBuffer(dpy, w, h, False, sync=0)
    sys.stdout.write('Place bug under window and\n')
    sys.stdout.write('hit RETURN to start >>'); sys.stdout.flush()
    sys.stdin.readline()
else:
    sys.stdout.write('hit RETURN to start >>'); sys.stdout.flush()
    sys.stdin.readline()
    fb = FrameBuffer(dpy, w, h, True, sync=0)


if gammatest:
    fb.set_gamma(gammatest, gammatest, gammatest)

outfile.write("%% lcd=%s\n" % lcd)
outfile.write("%% full=%s\n" % full)
outfile.write("%% gammatest=%s\n" % gammatest)
outfile.write("%% columns: |r|g|b|Y|x|y|\n")

for l in range(255, 0, -10):
    for (rw,gw,bw) in ((1,0,0), (0,1,0), (0,0,1), (1,1,1)):
        r, g, b = rw*l, gw*l, bw*l
        fb.clear(color=(r, g, b))
        fb.flip()
        (Y, x, y) = dtp.Yxy()
         
        outfile.write('%d %d %d %f %f %f\n' % (r, g, b, Y, x, y))
        outfile.flush()
        
        sys.stdout.write("%s -> %s\n" % ((r,g,b), (Y,x,y)))
        sys.stdout.flush()

outfile.close()
