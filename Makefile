INSTALLDIR=/auto/share/pypeextra

install:
	sudo cp optix.py $(INSTALLDIR)
	sudo cp gammacal.py $(INSTALLDIR)
	sudo cp showcalib.m $(INSTALLDIR)
	sudo cp gammacal.sh $(INSTALLDIR)/gammacal
	sudo chmod +x $(INSTALLDIR)/gammacal

deps:
	sudo apt-get install libusb-dev

clean:	
	rm -f *.o core.* *.pyc \#*~ .*~ \#*\#
