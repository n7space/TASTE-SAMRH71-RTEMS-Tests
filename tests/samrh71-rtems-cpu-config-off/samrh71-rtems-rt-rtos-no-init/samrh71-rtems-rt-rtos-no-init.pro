TEMPLATE = lib
CONFIG -= qt
CONFIG += generateC

DISTFILES +=  $(HOME)/tool-inst/share/taste-types/taste-types.asn \
    samrh71.dv.xml
DISTFILES += samrh71-rtems-rt-rtos-no-init.msc
DISTFILES += interfaceview.xml
DISTFILES += work/binaries/*.msc
DISTFILES += work/binaries/coverage/index.html
DISTFILES += work/binaries/filters
DISTFILES += work/system.asn

DISTFILES += samrh71-rtems-rt-rtos-no-init.asn
DISTFILES += samrh71-rtems-rt-rtos-no-init.acn
include(work/taste.pro)
message($$DISTFILES)

