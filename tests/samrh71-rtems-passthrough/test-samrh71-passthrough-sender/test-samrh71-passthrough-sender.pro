TEMPLATE = lib
CONFIG -= qt
CONFIG += generateC

DISTFILES +=  $(HOME)/tool-inst/share/taste-types/taste-types.asn \
    samrh71.dv.xml
DISTFILES += interfaceview.xml
DISTFILES += work/binaries/coverage/index.html
DISTFILES += work/binaries/filters
DISTFILES += work/system.asn

DISTFILES += test-samrh71-passthrough-sender.asn
DISTFILES += test-samrh71-passthrough-sender.acn
include(work/taste.pro)
message($$DISTFILES)

