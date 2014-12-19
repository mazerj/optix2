# Pure python gamma calibration

Pype-based gamma correction using the DTP94 usb calibration
ug from the Monaco Optix.

Calibration is simple once installed:

1. plug DTP94 into a USB port on the rig machine to calibrate

2. run the 'gammacal' program (need pypenv on your path)
   
    	% gammacal ConfigFile lcd|crt [gamma_value] >outfile
	
   ConfigFile is the name of the pyperc Config.HOST file for
   the system you want to calibrate, lcd|crt is either 'lcd' or
   'crt', depending on what you're calibrating and gamma_value
   is an optional gamma value to set the monitor to DURING the
   calibration for validating and existing calibration

   Calibration data is saved to 'outfile', keep this -- it's
   a record of the complete luminance and color calibration
   for the monitor.
   
4. Plot the results in matlab:

        >> showcalib('outfile');

## Dependencies

- [Python](http://www.python.org)
- [pype](http://github.com/mazerj/pype3)
  * pype has it's own dependencies (numpy/scipy & pygame)
- [pyusb](http://walac.github.io/pyusb/) library
