#!/bin/sh

SETUPTOOLS=`grep "setuptools\s*\=\s*" versions.cfg | sed 's/\s*=\s*/==/g'`
ZCBUILDOUT=`grep "zc\.buildout\s*=\s*" versions.cfg | sed 's/\s*=\s*/==/g'`
VPARAMS="--clear"

if [ -z "$SETUPTOOLS" ]; then
  SETUPTOOLS="setuptools"
fi

if [ -z "$ZCBUILDOUT" ]; then
  ZCBUILDOUT="zc.buildout"
fi

if [ "$1" = "deployment.cfg" ]; then
  VPARAMS=$VPARAMS" --system-site-packages"
fi

if [ "$2" = "deployment.cfg" ]; then
  VPARAMS=$VPARAMS" --system-site-packages"
fi

if [ -s "bin/activate" ]; then
  echo "Updating setuptools: ./bin/easy_install" $SETUPTOOLS
  ./bin/easy_install $SETUPTOOLS

  echo "\n============================================================="
  echo "Buildout is already installed."
  echo "Please remove bin/activate if you want to re-run this script."
  echo "=============================================================\n"

  exit 0
fi

echo "Installing virtualenv"
wget "https://raw.github.com/pypa/virtualenv/master/virtualenv.py" -O "/tmp/virtualenv.py"

echo "Running: python2.6 /tmp/virtualenv.py $VPARAMS ."
python2.6 "/tmp/virtualenv.py" $VPARAMS .
rm /tmp/virtualenv.py*

echo "Updating setuptools: ./bin/easy_install" $SETUPTOOLS
./bin/easy_install $SETUPTOOLS

echo "Installing zc.buildout: $ ./bin/easy_install" $ZCBUILDOUT
./bin/easy_install $ZCBUILDOUT

echo "Disabling the SSL CERTIFICATION for git"
git config --global http.sslVerify false

echo ""
echo "===================================================="
echo "All set. Now you can run ./bin/buildout -c devel.cfg"
echo "===================================================="
echo ""
