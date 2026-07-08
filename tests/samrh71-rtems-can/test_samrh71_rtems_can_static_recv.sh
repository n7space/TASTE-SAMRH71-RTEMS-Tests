#!/bin/sh
ssh "${SAMRH71_REMOTE_USER}@${SAMRH71_REMOTE_IP}" "cansend can0 0BA#0001" && echo "Frame sent"
