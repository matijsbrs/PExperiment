# eVCC issues

Er kunnen problemen zijn met de eVCC.

## Logfile example with issue:

In onderstaande log is te zien dat de Lader probeert de firmware van de eVCC te updaten. 

```
    I 01/01/1970 00:04:39 {Xmodem upgrade thread} [XModem./dev/ttyXRUSB3]: wait for timed out; in buffer: ''
    I 01/01/1970 00:04:39 {Xmodem upgrade thread} [XModem./dev/ttyXRUSB3]: writing: at&qx
```    

Een aantal regels verder is te zien dat de update mislukt is

```
    I 01/01/1970 00:05:51 {80} [XModem./dev/ttyXRUSB3]: wait for nack timed out
    I 01/01/1970 00:05:51 {main} [SerialPortTransport./dev/ttyXRUSB3]: update firmware failed
```

Extra voorbeeld:

```
    S 01/01/1970 00:05:52 {main} [Connector.1]: Update firmware failed, retrying in 10 seconds
    S 01/01/1970 00:06:02 {main} [Connector.1]: Update connector firmware: ../latestevccFirmware1.bin
    I 01/01/1970 00:06:02 {main} [SerialPortTransport./dev/ttyXRUSB3]: Updating firmware ../latestevccFirmware1.bin
    I 01/01/1970 00:06:02 {main} [SerialPortTransport./dev/ttyXRUSB3]: Stopping
    I 01/01/1970 00:06:02 {89} [global]: Stopped serial data monitor thread
    S 01/01/1970 00:06:02 {ST 14} [SerialPortTransport./dev/ttyXRUSB3]: No evcc communication for 362 seconds; trying reset of transport: 
    S 01/01/1970 00:06:02 {ST 14} [SerialPortTransport./dev/ttyXRUSB3]: Reseting com
    I 01/01/1970 00:06:02 {ST 14} [SerialPortTransport./dev/ttyXRUSB3]: Stopping
    I 01/01/1970 00:06:03 {main} [SerialPortTransport./dev/ttyXRUSB3]: Stopped
```

## Logfile example succes:

```
    I 01/01/1970 00:08:26 {main} [SerialPortTransport./dev/ttyXRUSB4]: Starting /dev/ttyXRUSB4
    S 01/01/1970 00:08:26 {main} [FDUtil]: 
    java.lang.NoSuchFieldException: handle
        at java.lang.Class.getDeclaredField(Class.java:2070)
        at com.enovates.lccl.debug.FDUtil.logFD(FDUtil.java:36)
        at com.enovates.lccl.debug.FDUtil.logFD(FDUtil.java:56)
        at com.enovates.lccl.chargepoint.driver.transport.evcc.SerialPortTransport.start(SerialPortTransport.java:101)
        at com.enovates.lccl.ChargePointServer.initChargePoint(ChargePointServer.java:1587)
        at com.enovates.lccl.ChargePointServer.init(ChargePointServer.java:335)
        at com.enovates.lccl.ChargePointServer.main(ChargePointServer.java:162)
    S 01/01/1970 00:08:26 {main} [FDUtil]: {evcc transport start} native info of /dev/ttyXRUSB4 fd: 131 handle: -1
    I 01/01/1970 00:08:26 {main} [SerialPortTransport./dev/ttyXRUSB4]: opened /dev/ttyXRUSB4
    I 01/01/1970 00:08:26 {Thread-62} [global]: Starting serial data monitor thread: false
    I 01/01/1970 00:08:26 {main} [EVCCDriver.2]: started driver
    I 01/01/1970 00:08:26 {main} [SerialPortTransport./dev/ttyXRUSB4]: >req[LCC0000-00.00-000000-000]:00;atlog|17;
    I 01/01/1970 00:08:26 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: ErrOR:?x?xx????x?xx??xxx?????x??req[LCC0000-00.00-000000-000]:00;atlog|17;
    I 01/01/1970 00:08:27 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: resp[eNo0027-09.01-900001-000]00:OK;|00;
    I 01/01/1970 00:08:27 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: log[eNo0027-09.01-900001-000]:N300x;0;0;12;0;100.00;4414760,,,,,,,,0,0,0,240,239,241,0,0,0,5000,;;;S32A|10|3|11-->1176,24:0;m1:0,m2:0;;|29;
    I 01/01/1970 00:08:27 {main} [SerialPortTransport./dev/ttyXRUSB4]: >req[eNo0027-09.01-900001-000]:00;at&ready=2|7F;
    I 01/01/1970 00:08:27 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: resp[eNo0027-09.01-900001-000]00:OK;ready command:2|80;
    I 01/01/1970 00:08:28 {main} [Connector.2]: Checking evcc version
    I 01/01/1970 00:08:28 {main} [SerialPortTransport./dev/ttyXRUSB4]: >req[eNo0027-09.01-900001-000]:01;ati|3E;
    I 01/01/1970 00:08:28 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: resp[eNo0027-09.01-900001-000]01:OK;> eVCC_V3 Firmware 110.8.3 256d3|B1;
    I 01/01/1970 00:08:28 {main} [SerialPortTransport./dev/ttyXRUSB4]: >req[eNo0027-09.01-900001-000]:00;atlog|17;
    I 01/01/1970 00:08:28 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: resp[eNo0027-09.01-900001-000]00:OK;|00;
    I 01/01/1970 00:08:28 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: log[eNo0027-09.01-900001-000]:N200x;0;0;12;0;100.00;4414760,,,,,,,,0,0,0,240,239,241,0,0,0,5001,;;;S32A|10|3|11-->1178,24:0;m1:0,m2:0;;|2B;
    I 01/01/1970 00:08:28 {EVCCDriverthread: /dev/ttyXRUSB4} [EVCCDriver.2]: EV is plugged out.
    I 01/01/1970 00:08:28 {EVCCDriverthread: /dev/ttyXRUSB4} [SerialPortTransport./dev/ttyXRUSB4]: >req[eNo0027-09.01-900001-000]:02;at&led=7|A4;
    I 01/01/1970 00:08:28 {PT 3} [Connector.1]: Checking evcc version
    I 01/01/1970 00:08:28 {PT 3} [SerialPortTransport./dev/ttyXRUSB3]: >req[eNo0027-09.01-900001-000]:09;ati|3E;
    I 01/01/1970 00:08:28 {PT 4} [Connector.2]: Checking evcc version
    I 01/01/1970 00:08:29 {main} [License]: Allowed license for Smart charging
    I 01/01/1970 00:08:29 {main} [License]: Allowed license for Load balancing
    I 01/01/1970 00:08:29 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: resp[eNo0027-09.01-900001-000]02:OK;> LED : 7|E4;
    I 01/01/1970 00:08:29 {PT 4} [SerialPortTransport./dev/ttyXRUSB4]: >req[eNo0027-09.01-900001-000]:03;ati|3E;
    I 01/01/1970 00:08:29 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: resp[eNo0027-09.01-900001-000]03:OK;> eVCC_V3 Firmware 110.8.3 256d3|B1;
    I 01/01/1970 00:08:29 {PT 4} [SerialPortTransport./dev/ttyXRUSB4]: >req[eNo0027-09.01-900001-000]:04;atCommProtoVersion=1|C9;
    I 01/01/1970 00:08:29 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: resp[eNo0027-09.01-900001-000]04:OK;version:1|71;
    S 01/01/1970 00:08:29 {PT 4} [AbstractEVCCTransport]: currentProtocolVersion: V1
    I 01/01/1970 00:08:29 {PT 4} [SerialPortTransport./dev/ttyXRUSB4]: >req[eNo0027-09.01-900001-000]:05;at_wbtype?|0E;
    I 01/01/1970 00:08:29 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: resp[eNo0027-09.01-900001-000]05:OK;> Wb_type: LCCPROd3F1CMRA|86;
    I 01/01/1970 00:08:29 {PT 4} [SerialPortTransport./dev/ttyXRUSB4]: >req[eNo0027-09.01-900001-000]:06;atLockMoter?|A4;
    I 01/01/1970 00:08:30 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: resp[eNo0027-09.01-900001-000]06:OK;> Lock moter type: 2|9C;
    I 01/01/1970 00:08:30 {PT 4} [SerialPortTransport./dev/ttyXRUSB4]: >req[eNo0027-09.01-900001-000]:07;atLockMoter=1|D3;
    I 01/01/1970 00:08:30 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: ... Saving Configuration ...
    I 01/01/1970 00:08:30 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: config checksum: 157D
    I 01/01/1970 00:08:30 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: resp[eNo0027-09.01-900001-000]07:OK;> Lock moter type: 1|9B;
    I 01/01/1970 00:08:30 {PT 4} [SerialPortTransport./dev/ttyXRUSB4]: >req[eNo0027-09.01-900001-000]:08;atdim?|4E;
    I 01/01/1970 00:08:30 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: resp[eNo0027-09.01-900001-000]08:OK;> DIM : 100%|68;
    I 01/01/1970 00:08:30 {PT 4} [SerialPortTransport./dev/ttyXRUSB4]: >req[eNo0027-09.01-900001-000]:09;atdimS?|A1;
    I 01/01/1970 00:08:31 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: resp[eNo0027-09.01-900001-000]0b:OK;suspend:1|6D;
    I 01/01/1970 00:08:31 {PT 4} [SerialPortTransport./dev/ttyXRUSB4]: >req[eNo0027-09.01-900001-000]:0c;atContactorprotect=5|F5;
    I 01/01/1970 00:08:32 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: ... Saving Configuration ...
    I 01/01/1970 00:08:32 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: config checksum: 157D
    I 01/01/1970 00:08:32 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: resp[eNo0027-09.01-900001-000]0c:OK;> Contactorprotect: 5|9B;
    I 01/01/1970 00:08:32 {PT 4} [SerialPortTransport./dev/ttyXRUSB4]: >req[eNo0027-09.01-900001-000]:0d;at
```

## Status chargepoint

In onderstaande status weergave van de lader is te zien dat er bij Connector 1 een error wordt gemeld: 'MODE_3_UNRESPONSIVE'
Dit betekend dat er een probleem is met de de eVCC controller.

```
    Chargepoint PP001830 ON(Offline [backlog size: 4])(Reconnect procedure active)[JOCPP16]
    Temperature: 22.44?
    No latest token
    Uptime: 0days 0hrs 13min 6sec.
    Version: 1.8.7-1675874432794 (2023-02-08 16:40 +0000)
    hard limit: 24.00A
    evses: [evse 1 conn 1, evse 2 conn 2]
    Connectors:
        Connector 1 (eNo0027-09.01-900001-000) on-ERROR
            hard limit: 16.00A
            limited to: null
            Connected phases: null
            expected limit to: L1: 0.00A, L2: 0.00A, L3: 0.00A
            plugged out | idle | unlocked | Type2 Socket | LockSet: TRANSACTION
            Raw LogLine: nothing
            Errors: 1
                MODE_3_UNRESPONSIVE since Thu Jan 01 00:09:02 UTC 1970 message: No log line recieved from evcc since startup of lccl.
        Connector 2 (eNo0027-09.01-900001-000) on-ON
            hard limit: 16.00A
            limited to: Current [current=0A, phases=PHASE3]
            Connected phases: null
            expected limit to: L1: 0.00A, L2: 0.00A, L3: 0.00A
            plugged out | idle | unlocked | Type2 Socket | LockSet: TRANSACTION
            Raw LogLine: N000x;0;0;12;0;100.00;4414760,,,,,,,,0,0,0,239,240,240,0,0,0,5006,;;;S32A|10|7|11-->1175,24:0;m1:0,m2:0;;|2E;
```