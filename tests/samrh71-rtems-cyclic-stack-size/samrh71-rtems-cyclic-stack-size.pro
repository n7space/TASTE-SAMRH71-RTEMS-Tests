TEMPLATE = lib
CONFIG -= qt
CONFIG += generateC

DISTFILES +=  $(HOME)/tool-inst/share/taste-types/taste-types.asn
DISTFILES += interfaceview.xml
DISTFILES += work/binaries/coverage/index.html
DISTFILES += work/binaries/filters
DISTFILES += work/system.asn

DISTFILES += samrh71.dv.xml
DISTFILES += samrh71-rtems-cyclic-stack-size.asn
DISTFILES += samrh71-rtems-cyclic-stack-size.acn
include(work/taste.pro)
message($$DISTFILES)

