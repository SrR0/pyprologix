from numpy.core.numeric import True_
from numpy.f2py.auxfuncs import throw_error

from prologix import prologix
from dataclasses import dataclass
from time import sleep
from enum import Enum
import datetime




class pm2534(object):
    """Control Philips/Fluke PM2534 multimeters using a Prologix or a AR488 compatible dongle

    Attributes
    ----------

    addr : int
        Address of the targeted device
    gpib : prologix/ar488
        Prologix object used to communicate with the prologix dongle
    status : pm2534Status
        Current device status
    """

    addr: int = None
    gpib: prologix = None

    class Functions(Enum):
        VDC = 1
        VAC = 2
        RTW = 3
        RFW = 4
        IDC = 5
        IAC = 6
        TDC = 7


    class Triggers(Enum):
        I = 1
        B = 2
        E = 3
        K = 4


    #functions = ['VDC', 'VAC', 'RTW', 'RFW', 'IDC', 'IAC', 'TDC']



 #   TRIG_INT = 1
 #   TRIG_EXT = 2
 #   TRIG_SIN = 3
 #   TRIG_HLD = 4
 #   TRIG_FST = 5

    @dataclass
    class pm2534Status:
        """Current device status

        range : int
            numeric representation of currenly used measurement range:
            1: 30mV DC, 300mV AC, 30Ω, 300mA, Extended Ohms
            2: 300mV DC, 3V AC, 300Ω, 3A
            3: 3V DC, 30V AC, 3kΩ
            4: 30V DC, 300V AC, 30kΩ
            5: 300V DC, 300kΩ
            6: 3MΩ
            7: 30MΩ
            see also: getRange
        digits : int
            numeric representation of selected measurement resolution:
            1: 5½ Digits
            2: 4½ Digits
            3: 3½ Digits
            Lower resoluton allows for faster measurements
            see also: getDigits
        triggerExternal : bool
            External trigger enabled

        calRAM : bool
            Cal RAM enabled
        frontProts : bool
            Front/Read switch selected front measurement connectors
            True = Front Port
        freq50Hz : bool
            Device set up for 50Hz operation. False = 60Hz.
        autoZero : bool
            Auto-Zero is enabled
        autoRange : bool
            Auto-Range is enabled
        triggerInternal : bool
            Internal trigger is enabled. False = Single trigger.

        srqPon : bool
            Device asserts SRQ on power-on or Test/Reset/SDC
            Controlled by rear configuration switch 3
        srqCalFailed : bool
            Device asserts SRQ if CAL procedure failes
        srqKbd : bool
            Device asserts SRQ if keyboar SRQ is pressed
        srqHWErr : bool
            Device asserts SRQ if a hardware error occurs
        srqSyntaxErr : bool
            Device asserts SRQ if a syntax error occurs
        srqReading : bool
            Device asserts SRQ every time a new reading is available

        errADLink: bool
            Error while communicating with aDC
        errADSelfTest: bool
            ADC failed internal self-test
        errADSlope: bool
            ADC slope error
        errROM: bool
            ROM self-test failed
        errRAM: bool
            RAM self-test failed
        errChecksum: bool
            Self-test detecten an incorrect CAL RAM checksum
            Re-Asserted every time you use an affected range afterwards

        dac: int
            Raw DAC value

        fetched: datetime
            Date and time this status was updated
        """


        function: int = None
        range: int = None
        digits: int = None
        triggerExternal: bool = None
        calRAM: bool = None
        frontPorts: bool = None
        freq50Hz: bool = None
        autoZero: bool = None
        autoRange: bool = None
        triggerInternal: bool = None
        srqPon: bool = None
        srqCalFailed: bool = None
        srqKbd: bool = None
        srqHWErr: bool = None
        srqSyntaxErr: bool = None
        srqReading: bool = None
        errADLink: bool = None
        errADSelfTest: bool = None
        errADSlope: bool = None
        errROM: bool = None
        errRAM: bool = None
        errChecksum: bool = None
        dac: int = None
        fetched: datetime = None


    status = pm2534Status()

    def __init__(self, addr: int, port: str = None, baud: int = 115200, timeout: float = 0.25,
                 prologixGpib: prologix = None, debug: bool = False):
        """

        Parameters
        ----------
        addr : int
            Address of the targeted device
        port : str, optional
            path of the serial device to use. Example: `/dev/ttyACM0` or `COM3`
            If set a new prologix instance will be created
            Either port or prologixGpib must be given
            by default None
        baud : int, optional
            baudrate used for serial communication
            only used when port is given
            921600 should work with most USB dongles
            115200 or 9600 are common for devices using UART in between
            by default 921600
        timeout : float, optional
            number of seconds to wait at maximum for serial data to arrive
            only used when port is given
            by default 2.5 seconds
        prologixGpib : prologix, optional
            Prologix instance to use for communication
            Ths may be shared between multiple devices with different addresses
            Either port or prologixGpib must be given
            by default None
        debug : bool, optional
            Whether to print verbose status messages and all communication
            by default False
        """
        if port == None and prologixGpib == None:
            print("!! You must supply either a serial port or a prologix object")

        self.addr = addr

        if prologixGpib is None:
            self.gpib = prologix(port=port, baud=baud, timeout=timeout, debug=debug)
        else:
            self.gpib = prologixGpib

    def getMeasure(self) -> float:
        """Get last measurement as float

        Returns
        -------
        float
            last measurement
        """
        measurement = self.gpib.cmdPoll(" ", self.addr)

        if measurement is None:
            return None

        return float(measurement[6:])

    def getDigits(self, digits: int = None) -> float:
        """Get a human readable representation of currently used resolution

        Parameters
        ----------
        digits : int, optional
            numeric representation to interpret
            If None is given the last status reading is used
            by default None

        Returns
        -------
        """
        status = self.gpib.cmdPoll("DIG ?", self.addr, binary=True)

        return None

    def getFunction(self, function: int = None) -> str:
        """Get a human readable representation of currently used measurement function

        Parameters
        ----------
        function : int, optional
            numeric representation to interpret
            If None is given the last status reading is used
            by default None

        Returns
        -------
        Functions

        """
        if function is None:
            function = self.status.function

        if function == 1:
            return "VDC"
        elif function == 2:
            return "VAC"
        elif function == 3:
            return "RTW"
        elif function == 4:
            return "RFW"
        elif function == 5:
            return "IDC"
        elif function == 6:
            return "IAC"
        elif function == 7:
            return "TDC"
        else:
            return None

    def getRange(self, range: int = None, function: int = None, numeric: bool = False):
        """Get a human readable representation of currently used measurement range

        Parameters
        ----------
        range : int, optional
            numeric range representation to interpret
            If None is given the last status reading is used
            by default None
        function : int, optional
            numeric function representation to interpret
            If None is given the last status reading is used
            by default None
        numeric : bool, optional
            If True return the maximum value as Float instead
            of a human readable verison using SI-prefixes

        Returns
        -------
        str|float|None
            Maximum measurement value in current range
        """
        if range is None:
            range = self.status.range
        if function is None:
            function = self.status.function

        if range == 1:
            if function == 1:
                if numeric:
                    return 0.03
                else:
                    return "30mV"
            elif function == 2:
                if numeric:
                    return 0.3
                else:
                    return "300mV"
            elif function == 3 or function == 4:
                if numeric:
                    return 30.0
                else:
                    return "30Ω"
            elif function == 5 or function == 6:
                if numeric:
                    return 0.3
                else:
                    return "300mA"
            else:
                return None
        elif range == 2:
            if function == 1:
                if numeric:
                    return 0.3
                else:
                    return "300mV"
            elif function == 2:
                if numeric:
                    return 3.0
                else:
                    return "3V"
            elif function == 3 or function == 4:
                if numeric:
                    return 300.0
                else:
                    return "300Ω"
            elif function == 5 or function == 6:
                if numeric:
                    return 3.0
                else:
                    return "3A"
            else:
                return None
        elif range == 3:
            if function == 1:
                if numeric:
                    return 3.0
                else:
                    return "3V"
            elif function == 2:
                if numeric:
                    return 30.0
                else:
                    return "30V"
            elif function == 3 or function == 4:
                if numeric:
                    return 3000.0
                else:
                    return "3kΩ"
            else:
                return None
        elif range == 4:
            if function == 1:
                if numeric:
                    return 30.0
                else:
                    return "30V"
            elif function == 2:
                if numeric:
                    return 300.0
                else:
                    return "300V"
            elif function == 3 or function == 4:
                if numeric:
                    return 30000.0
                else:
                    return "30kΩ"
            else:
                return None
        elif range == 5:
            if function == 1:
                if numeric:
                    return 300.0
                else:
                    return "300V"
            elif function == 3 or function == 4:
                if numeric:
                    return 300000.0
                else:
                    return "300kΩ"
            else:
                return None
        elif range == 6:
            if function == 3 or function == 4:
                if numeric:
                    return 3000000.0
                else:
                    return "3MΩ"
            else:
                return None
        elif range == 7:
            if function == 3 or function == 4:
                if numeric:
                    return 30000000.0
                else:
                    return "30MΩ"
            else:
                return None

    def getStatus(self) -> pm2534Status:
        """Read current device status and populate status object

        Returns
        -------
        pm2534Status
            Updated status object
        """
        status = self.gpib.cmdPoll("B", self.addr, binary=True)

        # Update last readout time
        self.status.fetched = datetime.datetime.now()

        # Byte 5: RAW DAC value
        self.status.dac = status[4]

        # Byte 4: Error Information
        self.status.errChecksum = (status[3] & (1 << 0) != 0)
        self.status.errRAM = (status[3] & (1 << 1) != 0)
        self.status.errROM = (status[3] & (1 << 2) != 0)
        self.status.errADSlope = (status[3] & (1 << 3) != 0)
        self.status.errADSelfTest = (status[3] & (1 << 4) != 0)
        self.status.errADLink = (status[3] & (1 << 5) != 0)

        # Byte 3: Serial Poll Mask
        self.status.srqReading = (status[2] & (1 << 0) != 0)
        # Bit 1 not used
        self.status.srqSyntaxErr = (status[2] & (1 << 2) != 0)
        self.status.srqHWErr = (status[2] & (1 << 3) != 0)
        self.status.srqKbd = (status[2] & (1 << 4) != 0)
        self.status.srqCalFailed = (status[2] & (1 << 5) != 0)
        # Bit 6 always zero
        self.status.srqPon = (status[2] & (1 << 7) != 0)

        # Byte 2: Status Bits
        self.status.triggerInternal = (status[1] & (1 << 0) != 0)
        self.status.autoRange = (status[1] & (1 << 1) != 0)
        self.status.autoZero = (status[1] & (1 << 2) != 0)
        self.status.freq50Hz = (status[1] & (1 << 3) != 0)
        self.status.frontPorts = (status[1] & (1 << 4) != 0)
        self.status.calRAM = (status[1] & (1 << 5) != 0)
        self.status.triggerExternal = (status[1] & (1 << 6) != 0)

        # Byte 1: Function/Range/Digits
        sb1 = status[0]
        self.status.digits = (sb1 & 0b00000011)
        sb1 = sb1 >> 2
        self.status.range = (sb1 & 0b00000111)
        sb1 = sb1 >> 3
        self.status.function = (sb1 & 0b00000111)

        return self.status

    def getFrontRear(self) -> bool:
        """Get position of Front/Rear switch

        May also be used to easily determine if the device is responding

        Returns
        -------
        bool
            True  -> Front-Port
            False -> Rear-Port
            None  -> Device did not respond
        """
        check = self.gpib.cmdPoll("S")
        if check == "1":
            return True
        elif check == "0":
            return False
        else:
            return None

    def getCalibration(self, filename: str = None) -> bytearray:
        """Read device calibration data

        Code based on work by
            Steve1515 (EEVblog)
            fenugrec (EEVblog)
            Luke Mester (https://mesterhome.com/)

        Parameters
        ----------
        filename : str, optional
            filename to save calibration to
            file will be overwritten if it exists
            by default None

        Returns
        -------
        bytearray
            Raw calibration data
        """

        self.callReset()
        self.setTrigger(self.TRIG_HLD)

        check = self.getFrontRear()
        if check is None:
            print("Can not connect to instrument")
            return None

        self.setDisplay("CAL READ 00%")

        p = 0
        lp = 0
        cdata = b""

        for dbyte in range(0, 255):
            din = self.gpib.cmdPoll(self.gpib.escapeCmd("W" + chr(dbyte)), binary=True)
            cdata += din
            p = (int)(dbyte / 25.5)
            if p != lp:
                self.setDisplay("CAL READ " + str(p) + "0%")
                lp = p

        self.setDisplay("CAL READ OK")

        if filename is not None:
            fp = open("calibration.data", "wb")
            for byte in cdata:
                fp.write(byte.to_bytes(1, byteorder='big'))
            fp.close()

        sleep(1)
        self.setDisplay(None)

        self.callReset()

        return cdata

    def setAutoZero(self, autoZero: bool, noUpdate: bool = False) -> bool:
        """change Auto-Zero setting

        Parameters
        ----------
        autoZero : bool
            Whether to enable or disable Auto-Zero
        noUpdate : bool, optional
            If True do not update status object to verify change was successful
            by default False

        Returns
        -------
        bool
            new status of autoZero; presumed status if `noUpdate` was True
        """
        raise Exception("Function not implemented yet!")

    def setDisplay(self, text: str = None, online: bool = True) -> bool:
        """Change device display

        Parameters
        ----------
        text : str, optional
            When text is None or empty device will resume standard display mode
                as in show measurements
            When text is set it will be displayed on the device

            Only ASCII 32-95 are valid. Function aborts for invalid characters
            Must be <= 12 Characters while , and . do not count as character.
                consecutive , and . may not work
                using . or , after character 12 may not work
                Function aborts for too long strings
        online : bool, optional
            When True the device just shows the text but keeps all functionality online
            When False the device will turn off all dedicated annunciators and stop updating
                the display once the text was drwn. This will free up ressources and enable
                faster measurement speeds. Using False takes about 30mS to complete. If the
                updating is stopped for over 10 minutes if will shut down as in blank screen.
            by default True

        Returns
        -------
        bool
            Wheather setting the text worked as expected
        """
        raise Exception("Function not implemented yet!")

    def setFunction(self, function: Functions, noUpdate: bool = False) -> bool:
        """Change current measurement function

        Parameters
        ----------
        function : int
            numeric function representation
            you may also use the following class constants:
                VDC,VAC,Ω2W,Ω4W,ADC,AAC,EXTΩ
        noUpdate : bool, optional
            If True do not update status object to verify change was successful
            by default False

        Returns
        -------
        bool
            Whether update succeeded or not; not verified if `noUpdate` was True
        """
        if function in self.Functions:
            self.gpib.cmdWrite("FNC " + str(function.name), self.addr)
            """
                if not noUpdate:
                    self.getStatus()
                    if self.status.function != function:
                        print("!! Set failed. Tried to set " + self.getFunction(
                            function) + " but device returned " + self.getFunction(self.status.function))
                        return False
                    elif self.gpib.debug:
                        print(".. Changed to function " + self.getFunction(function))
                elif self.gpib.debug:
                    print(".. Probably changed to function " + self.getFunction(function))
        """
            return True

        print("!! Invalid function")
        return False

    def setRange(self, range, noUpdate: bool = False) -> bool:
        """Change current measurement range
        range : str|float
            Range as SI-Value or float
            Valid values:
            AUTO to enable Auto-Range

            Not all ranges can be used in all measurement functions
            VDC: 300E-3,3E0,30E0,300E0
            VAC: 300E-3,3E0,30E0,300E0
            RTW: 3E3,30E3,300E3,3E6,30E6,300E6
            RFW: 3E3,30E3,300E3,3E6
            IDC: 30E-3, 3E0
            IAC: 30E-3, 3E0
            TDC: 0
        noUpdate : bool, optional
            If True do not update status object to verify change was successful
            by default False
        Returns
        -------
        bool
            Whether update succeeded or not; not verified if `noUpdate` was True
        """
        if range=='AUTO':
            self.gpib.cmdWrite("RNG " + range, self.addr)
            return True
        else:
            self.gpib.cmdWrite('RNG {:1.3E}'.format(range))
            return True
        return False

    def setDigits(self, digits: int, noUpdate: bool = False) -> bool:
        """Change current measurement resolution
        Parameters
        ----------
        digits : float
            desired measurement resolution
            Valid values: 3,3.5,4,4.5,5,5.5
        noUpdate : bool, optional
            If True do not update status object to verify change was successful
            by default False

        Returns
        -------
        bool
            Whether update succeeded or not; not verified if `noUpdate` was True
        """
        if digits in range(1,7):
            self.gpib.cmdWrite("DIG " + str(digits), self.addr)
            return True
        return False

    def setTrigger(self, trigger: Triggers, noUpdate: bool = False) -> bool:
        """Change current measurement trigger

        Parameters
        ----------
        trigger : Triggers
            different kinds of Trigger

        noUpdate : bool, optional
            If True do not update status object to verify change was successful
            by default False

        Returns
        -------
        bool
            Whether update succeeded or not; not verified if `noUpdate` was True
        """
        if trigger in self.Triggers:
            self.gpib.cmdWrite("TRG " + str(trigger.name), self.addr)
            return True
        return False

    def setSRQ(self, srq: int):
        """Set Serial Poll Register Mask

        @TODO Not tested and no validations

        Parameters
        ----------
        srq : int
            Parameter must be two digits exactly. Bits 0-5 of the binary representation
            are used to set the mask
        """
        raise Exception("Function not implemented yet!")

    def clearSPR(self):
        """Clear Serial Poll Register (SPR)
        """
        raise Exception("Function not implemented yet!")

    def clearERR(self) -> bytearray:
        """Clear Error Registers

        Returns
        -------
        bytearray
            Error register as octal digits
        """
        raise Exception("Function not implemented yet!")

    def callReset(self):
        """Reset the device
        """
        self.gpib.cmdClr(self.addr)
