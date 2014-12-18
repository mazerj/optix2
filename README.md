# Pure python gamma calibration

The programs in this directory are for gamma correcting LCD
and CRT monitors using the DTP94 usb calibration bug from
the MonacoOptix guys.

Calibration is pretty simple once installed:

1. plug DTP94 into USB port on the rig machine to calibrate

2. run the 'gammacal' program (should be in /auto/share/pypeextra
   on your path:
   
    	% gammacal ConfigFile lcd|crt [gamma_value] >outfile
	
   ConfigFile is the name of the pyperc Config.HOST file for
   the system you want to calibrate, lcd|crt is either 'lcd' or
   'crt', depending on what you're calibrating and gamma_value
   is an optional gamma value to set the monitor to DURING the
   calibration for validating and existing calibration

   Calibration data is saved to 'outfile', keep this -- it's
   a record of the complete luminance and color calibration
   for the monitor.
   
4. Plot the resulting calibration:

        % matlab
        ...
        >> showcalib('outfile');


The C dtp94 program is no longer needed.
