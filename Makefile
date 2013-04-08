INSTALLDIR=/auto/share/pypeextra

dtp94:
	cc -g -c dtp94.c
	cc -g -o dtp94 dtp94.o -lusb

all: dtp94 install

install: dtp94
	sudo cp dtp94 $(INSTALLDIR)
	sudo chown root $(INSTALLDIR)/dtp94
	sudo chmod +s $(INSTALLDIR)/dtp94
	sudo cp gammacal.py $(INSTALLDIR)
	sudo cp showcalib.m $(INSTALLDIR)
	sudo cp gammacal.sh $(INSTALLDIR)/gammacal
	sudo chmod +x $(INSTALLDIR)/gammacal

deps:
	sudo apt-get install libusb-dev

clean:	
	rm -f *.o core.* *.pyc \#*~ .*~ dtp94 \#*\#
