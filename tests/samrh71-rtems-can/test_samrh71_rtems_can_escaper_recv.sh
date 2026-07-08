#!/bin/sh
ssh "${SAMRH71_REMOTE_USER}@${SAMRH71_REMOTE_IP}" "cansend can0 142#00FE0002FE00BBFE && cansend can0 142#00CCFE00DDFE00EE && cansend can0 142#FF" && echo "Frame sent"
