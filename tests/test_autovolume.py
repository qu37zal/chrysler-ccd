import unittest

from host.autovolume import AutoVolumeController, AutoVolumeMode


def controller(**overrides):
    options = {
        "max_abs_offset_steps": 4,
        "min_auto_pulse_interval_ms": 250,
        "offset_stale_timeout_ms": 1000,
    }
    options.update(overrides)
    instance = AutoVolumeController(**options)
    instance.confirm_head_unit_power_cycle(0)
    return instance


class AutoVolumeTests(unittest.TestCase):
    def test_unknown_initial_baseline_inhibits_auto_until_confirmed(self):
        c = AutoVolumeController(4, 250, 1000)
        self.assertEqual(c.receive_offset(2, 0), [])
        self.assertFalse(c.baseline_known)
        self.assertEqual(c.confirm_head_unit_power_cycle(10)[0].direction, 1)

    def test_rising_and_falling_offset_follow_relative_steps(self):
        c = controller()
        self.assertEqual(c.receive_offset(3, 0)[0].direction, 1)
        self.assertEqual(c.tick(250)[0].direction, 1)
        self.assertEqual(c.tick(500)[0].direction, 1)
        self.assertEqual(c.commanded_offset, 3)

        self.assertEqual(c.receive_offset(1, 600), [])
        self.assertEqual(c.tick(750)[0].direction, -1)
        self.assertEqual(c.tick(1000)[0].direction, -1)
        self.assertEqual(c.commanded_offset, 1)

    def test_offset_is_bounded_and_repeated_level_does_not_storm(self):
        c = controller(max_abs_offset_steps=2)
        self.assertEqual(c.receive_offset(50, 0)[0].direction, 1)
        pulses = [c.tick(t) for t in (250, 500, 750, 1000)]
        self.assertEqual(sum(bool(p) for p in pulses), 1)
        self.assertEqual(c.commanded_offset, 2)
        self.assertEqual(c.receive_offset(50, 1100), [])

    def test_manual_volume_press_does_not_change_auto_offset_ledger(self):
        c = controller()
        c.receive_offset(2, 0)
        before = c.commanded_offset
        manual = c.manual_press(1)[0]
        self.assertEqual(manual.direction, 1)
        self.assertFalse(manual.automatic)
        self.assertEqual(c.commanded_offset, before)

    def test_lost_head_unit_pulse_is_not_retried_forever(self):
        c = controller()
        emitted = c.receive_offset(1, 0)
        self.assertEqual(len(emitted), 1)
        # Simulate the head unit missing the emitted pulse; there is no ACK.
        self.assertEqual(c.receive_offset(1, 250), [])
        self.assertEqual(c.commanded_offset, 1)
        trim = c.manual_press(-1)[0]
        self.assertEqual(trim.direction, -1)
        self.assertFalse(trim.automatic)

    def test_off_mode_removes_only_automatic_contribution(self):
        c = controller()
        c.receive_offset(2, 0)
        c.tick(250)
        self.assertEqual(c.commanded_offset, 2)
        self.assertEqual(c.set_mode(AutoVolumeMode.OFF, 300), [])
        self.assertEqual(c.tick(500)[0].direction, -1)
        self.assertEqual(c.tick(750)[0].direction, -1)
        self.assertEqual(c.commanded_offset, 0)

    def test_stale_offset_pauses_and_latest_received_level_recovers(self):
        c = controller()
        c.receive_offset(2, 0)
        self.assertEqual(c.tick(1001), [])
        self.assertEqual(c.commanded_offset, 1)
        self.assertEqual(c.receive_offset(1, 1100), [])
        self.assertEqual(c.tick(1250), [])
        self.assertEqual(c.commanded_offset, 1)

    def test_reset_inhibits_auto_until_head_unit_cycle_is_confirmed(self):
        c = controller()
        c.receive_offset(2, 0)
        c.controller_reset()
        self.assertEqual(c.receive_offset(2, 300), [])
        self.assertFalse(c.baseline_known)
        self.assertEqual(c.confirm_head_unit_power_cycle(400)[0].direction, 1)

    def test_time_must_be_monotonic(self):
        c = controller()
        c.receive_offset(1, 100)
        with self.assertRaises(ValueError):
            c.tick(99)


if __name__ == "__main__":
    unittest.main()
