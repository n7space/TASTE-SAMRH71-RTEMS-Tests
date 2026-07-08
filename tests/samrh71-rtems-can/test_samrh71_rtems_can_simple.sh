#!/bin/sh
exec ssh "${SAMRH71_REMOTE_USER}@${SAMRH71_REMOTE_IP}" "candump can0 -x -e -d"
