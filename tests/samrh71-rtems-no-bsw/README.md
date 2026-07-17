# samrh71-rtems-bsw

This is the project for to test if the TASTE-SAMX-RTEMS-Runtime can be executed from flash, without any BSW.

## Test steps

  1. Build the project using `make samrh71 debug`.
  2. Start gdb-multiarch, and upload image using the following commands:
     - file work/binaries/partition_1
     - target extended-remote <ip-and-port-of-gdb-server>
     - monitor reset
     - monitor flash erase
     - load
     - continue
  3. At this moment the application shall work and send data via Uart1, baudrate 38400, no parity.
  4. Application shall work after power-off & power-on of the Evaluation Kit board.
  5. The linux application can be started by: `work/binaries/partition_2` and if there is an access to UART device, it shall print messages about sending and receiving data.
