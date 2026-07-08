#!/bin/sh
set -m # enable job control
ssh "${SAMRH71_REMOTE_USER}@${SAMRH71_REMOTE_IP}" "candump can0 -x -e -d" &
ssh "${SAMRH71_REMOTE_USER}@${SAMRH71_REMOTE_IP}" \
	"cansend can0 099# && cansend can0 098#01 && cansend can0 097#0102 && cansend can0 096#010203 && cansend can0 095#01020304 && cansend can0 094#0102030405 && cansend can0 093#010203040506 && cansend can0 092#01020304050607 && cansend can0 091#0102030405060708"
fg
