#!/bin/bash
# Copyright (C) 2011 Citrix Systems, Inc.  All rights reserved
#     
# This software is licensed under the GNU General Public License v3 or later.
# 
# It is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Version @VERSION@

#set -x
 
usage() {
  printf "Usage: %s [mountpoint in secondary storage] [uuid of the source vdi] [uuid of the source sr]\n" $(basename $0) 
}

cleanup()
{
  if [ ! -z $localmp ]; then 
    umount $localmp
    if [ $? -eq 0 ];  then
      rmdir $localmp
    fi
  fi
}

if [ -z $1 ]; then
  usage
  echo "1#no mountpoint"
  exit 0
else
  mountpoint=$1
fi

if [ -z $2 ]; then
  usage
  echo "2#no uuid of the source sr"
  exit 0
else
  vdiuuid=$2
fi


if [ -z $3 ]; then
  usage
  echo "3#no uuid of the source sr"
  exit 0
else
  sruuid=$3
fi

type=$(xe sr-param-get uuid=$sruuid param-name=type)
if [ $? -ne 0 ]; then
  echo "4#sr $sruuid doesn't exist"
  exit 0
fi

localmp=/var/run/cloud_mount/$(uuidgen -r)

mkdir -p $localmp
if [ $? -ne 0 ]; then
  echo "5#can't make dir $localmp"
  exit 0
fi

mount -o tcp,soft,timeo=133,retrans=1 $mountpoint $localmp
if [ $? -ne 0 ]; then
  echo "6#can't mount $mountpoint to $localmp"
  exit 0
fi

vhdfile=$localmp/${vdiuuid}.vhd

if [ $type == "nfs" -o $type == "ext" ]; then
  dd if=/var/run/sr-mount/$sruuid/${vdiuuid}.vhd of=$vhdfile bs=2M
  if [ $? -ne 0 ]; then
    rm -f $vhdfile
    echo "8#failed to copy /var/run/sr-mount/$sruuid/${vdiuuid}.vhd to secondarystorage"
    cleanup
    exit 0
  fi
elif [ $type == "lvmoiscsi" -o $type == "lvm" -o $type == "lvmohba" ]; then
  lvchange -ay /dev/VG_XenStorage-$sruuid/VHD-$vdiuuid
  if [ $? -ne 0 ]; then
    echo "9#lvm can not make VDI $vdiuuid  visible"
    cleanup
    exit 0
  fi
  size=$(vhd-util query -s -n /dev/VG_XenStorage-$sruuid/VHD-$vdiuuid)
  if [ $? -ne 0 ]; then
    echo "10#can not get physical size of /dev/VG_XenStorage-$sruuid/VHD-$vdiuuid"
    cleanup
    exit 0
  fi
#in 2M unit
  size=$((size>>21))
  size=$((size+1))
  dd if=/dev/VG_XenStorage-$sruuid/VHD-$vdiuuid of=$vhdfile bs=2M count=$size
  if [ $? -ne 0 ]; then
    rm -f $vhdfile
    echo "8#failed to copy /dev/VG_XenStorage-$sruuid/VHD-$vdiuuid to secondarystorage"
    cleanup
    exit 0
  fi
#in byte unit
  size=$((size<<21))
  vhd-util modify -s $size -n $vhdfile
  if [ $? -ne 0 ]; then
    rm -f $vhdfile
    echo "11#failed to change $vhdfile physical size"
    cleanup
    exit 0
  fi
else 
  echo "15#doesn't support sr type $type"
  cleanup
  exit 0
fi

echo "0#$vdiuuid"
cleanup
exit 0
