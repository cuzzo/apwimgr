#! /usr/bin/env bash

INITDP=/etc/init.d/apwimgrd
SSTART=S99apwimgrd
SKILL=K85apwimgrd

# Create service.
cp apwimgrd $INITDP
ln -s $INITDP /etc/rc0.d/$SKILL
ln -s $INITDP /etc/rc1.d/$SKILL
ln -s $INITDP /etc/rc2.d/$SSTART
ln -s $INITDP /etc/rc3.d/$SSTART
ln -s $INITDP /etc/rc4.d/$SSTART
ln -s $INITDP /etc/rc5.d/$SSTART
ln -s $INITDP /etc/rc6.d/$SKILL

# Create conf.
mkdir /etc/apwimgr
cp apwimgr.conf /etc/apwimgr/

# Create var.
mkdir /usr/share/apwimgr
cp -R static /usr/share/apwimgr/
cp -R tpl /usr/share/apwimgr/

# Create bin.
cp ap_host /usr/local/bin/
cp apwimgr_monitor /usr/sbin/
cp apwimgr_server /usr/local/bin/

# Python install.
pip install apwimgr
