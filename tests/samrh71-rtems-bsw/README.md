# samrh71-rtems-bsw

This is the project for testing if the TASTE-SAMX-RTEMS-Runtime can be executed as an ASW, by N7S BSW.

## Test steps

  1. Build the project using `make samrh71 debug`.
  2. Make sure that SamRH71 Evaluation Kit Board has UART connection (Uart3, baudrate 9600, no parity, 1 stop bit) with your computer.
  3. Power-off EK board.
  4. Start BSWTool and select configuration BSW-Tool-Config-samrh71f20-mbep
  5. Select the correct UART device like `/dev/ttyUSB0` and click `Enter Standby`.
  6. Power-on board, the BSWTool shall receive a telemetry.
  7. Set `Path to the ASW File` to `work/binaries/partition_1` in this project.
  8. Click `Upload ASW Image` and confirm. Wait for the end.
  9. After upload click `Reset`, the BSW will try to boot ASW, some TMs will be received.
  10. Verify if TM-3-25 with finalBootReport was received.
  11. The ASW shall send data via Uart1 to the partition_2 executed on Linux.
