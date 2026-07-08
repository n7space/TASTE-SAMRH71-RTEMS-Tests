#!/bin/sh
set -m # enable job control
ssh "${SAMRH71_REMOTE_USER}@${SAMRH71_REMOTE_IP}" "candump can0 -x -e -d" &
sleep 1
ssh "${SAMRH71_REMOTE_USER}@${SAMRH71_REMOTE_IP}" "cansend can0 142#00 && cansend can0 142#010305 && cansend can0 142#cccc"
fg
