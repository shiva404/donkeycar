"""
Battery / power monitoring via INA219 (I2C), plus helpers to interpret
multimeter readings.

Default I2C address is 0x41 because 0x40 is usually taken by the PCA9685.
Confirm with: sudo i2cdetect -y 1
"""
import logging
import time

logger = logging.getLogger(__name__)

# Resting / light-load LiPo guidance (per cell)
CELL_FULL = 4.20
CELL_GOOD = 3.80
CELL_OK = 3.70
CELL_LOW = 3.50
CELL_CRITICAL = 3.30


def infer_cells(voltage):
    """Guess 2S vs 3S from pack voltage."""
    if voltage is None:
        return None
    if 6.0 <= voltage <= 8.8:
        return 2
    if 9.0 <= voltage <= 13.0:
        return 3
    # fallback: nearest
    if voltage < 9.0:
        return 2
    return 3


def pack_health(voltage, cells=None):
    """
    Return (cells, v_per_cell, status, advice).
    status: full | good | ok | low | critical | unknown
    """
    if voltage is None or voltage <= 0:
        return None, None, 'unknown', 'No voltage reading.'

    cells = cells or infer_cells(voltage)
    v_cell = voltage / cells

    if v_cell >= CELL_FULL - 0.05:
        status, advice = 'full', 'Fully / near fully charged.'
    elif v_cell >= CELL_GOOD:
        status, advice = 'good', 'Healthy — fine to calibrate and drive.'
    elif v_cell >= CELL_OK:
        status, advice = 'ok', 'OK for short runs; charge soon.'
    elif v_cell >= CELL_LOW:
        status, advice = 'low', 'Low — charge before hard driving/calibration.'
    else:
        status, advice = 'critical', 'Critical — stop and charge (risk of LVC/damage).'

    return cells, v_cell, status, advice


def format_health(voltage, current=None, power=None, cells=None,
                  session_min=None, session_max=None):
    cells, v_cell, status, advice = pack_health(voltage, cells=cells)
    lines = [f"Pack: {voltage:.2f} V"]
    if cells and v_cell is not None:
        lines.append(f"Cells: {cells}S  ({v_cell:.2f} V/cell)  health={status}")
        lines.append(f"Advice: {advice}")
    if current is not None:
        lines.append(f"Current: {current:.2f} A")
    if power is not None:
        lines.append(f"Power: {power:.1f} W")
    if session_min is not None and session_max is not None:
        sag = session_max - session_min
        lines.append(
            f"Session: max {session_max:.2f} V  min {session_min:.2f} V  "
            f"sag {sag:.2f} V")
        if cells and sag > 0.6 * cells:
            lines.append(
                "Large sag under load — pack may be weak, cold, or undersized.")
    return '\n'.join(lines)


class INA219BatteryMonitor:
    """
    Donkeycar part that outputs bus voltage (V), current (A), power (W).
    Tracks session min/max for sag / health while driving.
    """

    def __init__(self, address=0x41, busnum=1, shunt_ohms=0.1,
                 max_expected_amps=3.0, log_every_s=5.0, cells=None):
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
        self.cells = cells
        self._last_log = 0.0
        self.voltage = 0.0
        self.current = 0.0
        self.power = 0.0
        self.session_min = None
        self.session_max = None

        i2c = ExplicitBusI2C(busnum)
        self.ina = adafruit_ina219.INA219(i2c, addr=address)
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
            self.voltage = float(self.ina.bus_voltage)
            try:
                self.current = float(self.ina.current) / 1000.0  # mA -> A
            except Exception:
                self.current = 0.0
            try:
                self.power = float(self.ina.power) / 1000.0  # mW -> W
            except Exception:
                self.power = abs(self.voltage * self.current)

            if self.session_min is None or self.voltage < self.session_min:
                self.session_min = self.voltage
            if self.session_max is None or self.voltage > self.session_max:
                self.session_max = self.voltage

            now = time.time()
            if self.log_every_s and (now - self._last_log) >= self.log_every_s:
                self._last_log = now
                cells, v_cell, status, _ = pack_health(
                    self.voltage, cells=self.cells)
                extra = ''
                if self.session_min is not None:
                    extra = (
                        f" | sag {self.session_max - self.session_min:.2f} V "
                        f"(min {self.session_min:.2f})")
                logger.info(
                    "battery: %.2f V (%.2f V/cell %sS %s) | %.2f A | %.1f W%s",
                    self.voltage,
                    v_cell if v_cell else 0.0,
                    cells or '?',
                    status,
                    self.current,
                    self.power,
                    extra)
                if status in ('low', 'critical'):
                    logger.warning(
                        "Pack health %s — reduce load or charge.", status)
        except Exception as e:
            logger.warning("INA219 read failed: %s", e)

        return self.voltage, self.current, self.power

    def shutdown(self):
        if self.session_min is not None:
            logger.info(
                "battery session summary:\n%s",
                format_health(
                    self.voltage,
                    self.current,
                    self.power,
                    cells=self.cells,
                    session_min=self.session_min,
                    session_max=self.session_max))


def read_once(address=0x41, busnum=1):
    """One-shot voltage read for CLI / scripts."""
    mon = INA219BatteryMonitor(address=address, busnum=busnum, log_every_s=0)
    return mon.run()
