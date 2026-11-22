import pytest
from .setup import on_pi
from donkeycar.parts.controller import (
    PS3Joystick,
    PS3JoystickController,
    xbox_drive_signals,
    xbox_trigger_magnitude,
)


def test_ps3_joystick():
    js = PS3Joystick()
    assert js is not None
    js.init()

def test_ps3_joystick_controller():
    js = PS3JoystickController()
    assert js is not None
    js.init_js()
    js.run_threaded(None)
    js.print_controls()
    def test_fn():
        pass
    js.set_button_down_trigger("x", test_fn)
    js.erase_last_N_records()
    js.on_throttle_changes()
    js.emergency_stop()
    #js.update()
    js.set_steering(0.0)
    js.set_throttle(0.0)
    js.toggle_manual_recording()
    js.increase_max_throttle()
    js.decrease_max_throttle()
    js.toggle_constant_throttle()
    js.toggle_mode()
    js.chaos_monkey_on_left()
    js.chaos_monkey_on_right()
    js.chaos_monkey_off()


def test_xbox_trigger_magnitude_ranges():
    # Rest at -1 (classic) -> 0 throttle; fully pressed +1 -> 1.0
    assert xbox_trigger_magnitude(-1.0) == pytest.approx(0.0)
    assert xbox_trigger_magnitude(1.0) == pytest.approx(1.0)
    assert xbox_trigger_magnitude(0.0) == pytest.approx(0.0)  # 0..1 rest
    assert xbox_trigger_magnitude(0.5) == pytest.approx(0.5)
    assert xbox_trigger_magnitude(1.0, reversed=True) == pytest.approx(-1.0)


def test_xbox_drive_signals_stick_and_triggers():
    sig = xbox_drive_signals(
        {
            'left_stick_horz': 0.5,
            'right_stick_vert': -1.0,  # pull back on stick
            'right_trigger': -1.0,     # rest
            'left_trigger': -1.0,
        },
        throttle_dir=-1.0,
        throttle_scale=0.5,
        steering_scale=1.0,
    )
    assert sig['steering'] == pytest.approx(0.5)
    # throttle_dir=-1 * stick=-1 * scale=0.5 => +0.5 forward
    assert sig['stick_throttle'] == pytest.approx(0.5)
    assert sig['right_trigger_throttle'] == pytest.approx(0.0)
    assert sig['throttle'] == pytest.approx(0.5)
    assert sig['active_throttle_source'] == 'stick'

    sig_rt = xbox_drive_signals(
        {
            'left_stick_horz': 0.0,
            'right_stick_vert': 0.0,
            'right_trigger': 1.0,
            'left_trigger': -1.0,
        },
        throttle_dir=-1.0,
        throttle_scale=0.5,
    )
    # magnitude(1.0)=1.0; * dir=-1 * scale=0.5 => -0.5
    assert sig_rt['right_trigger_throttle'] == pytest.approx(-0.5)
    assert sig_rt['active_throttle_source'] == 'right_trigger'


def test_xbox_drive_signals_swapped():
    sig = xbox_drive_signals(
        {
            'right_stick_horz': -0.25,
            'left_stick_vert': 0.8,
            'right_trigger': -1.0,
            'left_trigger': -1.0,
        },
        throttle_dir=1.0,
        throttle_scale=1.0,
        swapped=True,
    )
    assert sig['steer_axis'] == 'right_stick_horz'
    assert sig['stick_axis'] == 'left_stick_vert'
    assert sig['steering'] == pytest.approx(-0.25)
    assert sig['stick_throttle'] == pytest.approx(0.8)
