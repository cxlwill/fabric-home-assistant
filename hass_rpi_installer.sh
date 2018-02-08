#!/usr/bin/env bash
# Home Assistant Raspberry Pi Installer Kickstarter
# Copyright (C) 2017 Jonathan Baginski - All Rights Reserved
# Permission to copy and modify is granted under the MIT License
# Last revised 1/30/2017

## Run pre-install apt package dependency checks ##

while getopts ":n" opt; do
  case $opt in
    n)

    me=$(whoami)


    sudo apt-get update

    PKG_PYDEV=$(dpkg-query -W --showformat='${Status}\n' python3-dev|grep "install ok installed")
    echo Checking for python3-dev: $PKG_PYDEV
    if [ "" == "$PKG_PYDEV" ]; then
      echo "缺少 python3-dev。安装 python3-dev。"
      sudo apt-get --force-yes --yes install python-dev
    fi

    PKG_PYPIP=$(dpkg-query -W --showformat='${Status}\n' python3-pip|grep "install ok installed")
    echo Checking for python3-pip: $PKG_PYPIP
    if [ "" == "$PKG_PYPIP" ]; then
      echo "缺少 python3-pip。安装 python3-pip。"
      sudo apt-get --force-yes --yes install python3-pip
    fi

    PKG_GIT=$(dpkg-query -W --showformat='${Status}\n' git|grep "install ok installed")
    echo Checking for git: $PKG_GIT
    if [ "" == "$PKG_GIT" ]; then
      echo "缺少 git。安装 git。"
      sudo apt-get --force-yes --yes install git
    fi

    PKG_LIBSSL_DEV=$(dpkg-query -W --showformat='${Status}\n' libssl-dev|grep "install ok installed")
    echo Checking for libssl-dev: $PKG_LIBSSL_DEV
    if [ "" == "$PKG_LIBSSL_DEV" ]; then
      echo "缺少 libssl-dev。安装 libssl-dev。"
      sudo apt-get --force-yes --yes install libssl-dev
    fi

    PKG_LIBFFI_DEV=$(dpkg-query -W --showformat='${Status}\n' libffi-dev|grep "install ok installed")
    echo Checking for libffi-dev: $PKG_LIBFFI_DEV
    if [ "" == "$PKG_LIBFFI_DEV" ]; then
      echo "缺少 libffi-dev。安装 libffi-dev。"
      sudo apt-get --force-yes --yes install libffi-dev
    fi

    PKG_APT_LISTCHANGES=$(dpkg-query -W --showformat='${Status}\n' apt-listchanges|grep "install ok installed")
    echo Checking for apt-listchanges: $PKG_APT_LISTCHANGES
    if [ "install ok installed" == "$PKG_APT_LISTCHANGES" ]; then
      echo "apt-listchanges 已安装，准备移除。"
      sudo apt-get --force-yes --yes remove apt-listchanges
    fi

	sudo pip3 install --upgrade pip
	sudo pip3 install --upgrade setuptools
	sudo pip3 install pycrypto
	sudo pip3 install cryptography
	sudo pip3 install packaging
	sudo pip3 install appdirs
	sudo pip3 install six
	sudo pip3 install fabric

    git clone https://git.coding.net/cxlwill/ha-aio.git

    ( cd /home/$me/ha-aio && fab deploy_novenv -H localhost 2>&1 | tee installation_report.txt )
    exit
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

me=$(whoami)


sudo apt-get update

PKG_PYDEV=$(dpkg-query -W --showformat='${Status}\n' python3-dev|grep "install ok installed")
echo Checking for python-dev: $PKG_PYDEV
if [ "" == "$PKG_PYDEV" ]; then
  echo "缺少 python3-dev，即将安装 python3-dev."
  sudo apt-get --force-yes --yes install python-dev
fi

PKG_PYPIP=$(dpkg-query -W --showformat='${Status}\n' python3-pip|grep "install ok installed")
echo Checking for python-pip: $PKG_PYPIP
if [ "" == "$PKG_PYPIP" ]; then
  echo "缺少 python3-pip，即将安装 python3-pip."
  sudo apt-get --force-yes --yes install python-pip
fi

PKG_GIT=$(dpkg-query -W --showformat='${Status}\n' git|grep "install ok installed")
echo Checking for git: $PKG_GIT
if [ "" == "$PKG_GIT" ]; then
  echo "缺少 git，即将安装 git。"
  sudo apt-get --force-yes --yes install git
fi

PKG_LIBSSL_DEV=$(dpkg-query -W --showformat='${Status}\n' libssl-dev|grep "install ok installed")
echo Checking for libssl-dev: $PKG_LIBSSL_DEV
if [ "" == "$PKG_LIBSSL_DEV" ]; then
  echo "缺少 libssl-dev，即将安装 libssl-dev。"
  sudo apt-get --force-yes --yes install libssl-dev
fi

PKG_LIBFFI_DEV=$(dpkg-query -W --showformat='${Status}\n' libffi-dev|grep "install ok installed")
echo Checking for libffi-dev: $PKG_LIBFFI_DEV
if [ "" == "$PKG_LIBFFI_DEV" ]; then
  echo "缺少 libffi-dev，即将安装 libffi-dev。"
  sudo apt-get --force-yes --yes install libffi-dev
fi

PKG_APT_LISTCHANGES=$(dpkg-query -W --showformat='${Status}\n' apt-listchanges|grep "install ok installed")
echo Checking for apt-listchanges: $PKG_APT_LISTCHANGES
if [ "install ok installed" == "$PKG_APT_LISTCHANGES" ]; then
  echo "apt-listchanges 已安装，准备移除。"
  sudo apt-get --force-yes --yes remove apt-listchanges
fi

sudo pip3 install --upgrade pip
sudo pip3 install --upgrade setuptools
sudo pip3 install pycrypto
sudo pip3 install cryptography
sudo pip3 install packaging
sudo pip3 install appdirs
sudo pip3 install six
sudo pip3 install fabric

git clone https://git.coding.net/cxlwill/ha-aio.git


( cd /home/$me/ha-aio && fab deploy -H localhost 2>&1 | tee installation_report.txt )
exit
