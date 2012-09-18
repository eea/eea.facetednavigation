#!/bin/sh
if [ ! -f bootstrap.sh ]
then
    wget -O bootstrap.sh https://svn.eionet.europa.eu/repositories/Zope/trunk/www.eea.europa.eu/trunk/install.sh
fi
chmod u+x bootstrap.sh
./bootstrap.sh
