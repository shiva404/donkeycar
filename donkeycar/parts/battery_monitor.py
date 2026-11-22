"""
Battery / power monitoring via INA219 (I2C).

Measures pack bus voltage (and optionally current/power if a shunt is present).
Default I2C address is 0x41 because 0x40 is usually taken by the PCA9685.

Hardware: Adafruit INA219 (or clone). For a 2S/3S LiPo, wire the load/battery
side per the breakout docs so bus voltage reads the pack. Confirm address with:
  sudo i2cdetect -y 1
"""
import logging
import time

logger = logging.getLogger(__name__)


class INA219BatteryMonitor:
    """
    Donkeycar part that outputs bus voltage (V), current (A), power (W).
    Current/power are 0.0 if the module has no useful shunt config.
    """

    def __init__(self, address=0x41, busnum=1, shunt_ohms=0.1,
                 max_expected_amps=3.0, log_every_s=5.0):
        from donkeycar.parts.i2c_bus import ExplicitBusI2C
        try:
            import adafruit_ina219
        except ImportError as e:
            raise ImportError(
                "Battery monitor needs adafruit-circuitpython-ina219. "
                "Install with: uv pip install adafruit-circuitpython-ina219"
            ) from e

        self.address = address
        self.busnum = busnum
        self.log_every_s = log_every_s
        self._last_log = 0.0
        self.voltage = 0.0
        self.current = 0.0
        self.power = 0.0

        i2c = ExplicitBusI2C(busnum)
        self.ina = adafruit_ina219.INA219(i2c, addr=address)
        # Prefer 32V range for 2S/3S LiPo packs when the driver exposes it.
        try:
            self.ina.bus_voltage_range = (
                adafruit_ina219.INA219.BusVoltageRange.RANGE_32V)
        except Exception as e:
            logger.warning("INA219 32V range not set: %s", e)

        logger.info(
            "INA219 battery monitor on bus %s address %s",
            busnum, hex(address))

    def run(self):
        try:
            # bus_voltage is load/battery side in volts
            self.voltage = float(self.ina.bus_voltage)
            try:
                self.current = float(self.ina.current) / 1000.0  # mA -> A
            except Exception:
                self.current = 0.0
            try:
                self.power = float(self.ina.power) / 1000.0  # mW -> W
            except Exception:
                self.power = abs(self.voltage * self.current)

            now = time.time()
            if self.log_every_s and (now - self._last_log) >= self.log_every_s:
                self._last_log = now
                logger.info(
                    "battery: %.2f V | %.2f A | %.1f W",
                    self.voltage, self.current, self.power)
        except Exception as e:
            logger.warning("INA219 read failed: %s", e)

        return self.voltage, self.current, self.power

    def shutdown(self):
        pass


def read_once(address=0x41, busnum=1):
    """One-shot voltage read for CLI / scripts."""
    mon = INA219BatteryMonitor(address=address, busnum=busnum, log_every_s=0)
    return mon.run()
