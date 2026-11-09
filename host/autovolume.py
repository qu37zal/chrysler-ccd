"""Deterministic relative autovolume compensation model.

The input is an already-decoded desired compensation level, expressed in
head-unit button-step equivalents. It is not a CCD frame decoder and makes no
claim about the Prowler's actual message IDs or payload encoding.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AutoVolumeMode(Enum):
    OFF = "off"
    LOW = "low"
    HIGH = "high"


@dataclass(frozen=True)
class VolumePulse:
    direction: int
    automatic: bool


class AutoVolumeController:
    """Translate BCM compensation-level changes into bounded relative steps.

    ``commanded_offset`` tracks only automatic steps this controller has
    emitted. It is not the head unit's absolute volume or an acknowledgement
    that the head unit accepted a pulse. Manual button presses pass through
    independently and do not modify this ledger.
    """

    def __init__(self, max_abs_offset_steps: int,
                 min_auto_pulse_interval_ms: int,
                 offset_stale_timeout_ms: int,
                 initial_mode: AutoVolumeMode = AutoVolumeMode.LOW):
        if max_abs_offset_steps < 0:
            raise ValueError("max_abs_offset_steps must be non-negative")
        if min_auto_pulse_interval_ms <= 0:
            raise ValueError("min_auto_pulse_interval_ms must be positive")
        if offset_stale_timeout_ms <= 0:
            raise ValueError("offset_stale_timeout_ms must be positive")
        if not isinstance(initial_mode, AutoVolumeMode):
            raise ValueError("initial_mode must be an AutoVolumeMode")
        self.max_abs_offset_steps = max_abs_offset_steps
        self.min_auto_pulse_interval_ms = min_auto_pulse_interval_ms
        self.offset_stale_timeout_ms = offset_stale_timeout_ms
        self.mode = initial_mode
        self.requested_offset: Optional[int] = None
        self.request_timestamp_ms: Optional[int] = None
        self.commanded_offset = 0
        self.last_auto_pulse_ms: Optional[int] = None
        self.baseline_known = False
        self._last_time_ms: Optional[int] = None

    def receive_offset(self, requested_steps: int, timestamp_ms: int):
        """Accept a fresh decoded BCM offset level and emit at most one step."""
        self._check_time(timestamp_ms)
        self.requested_offset = max(-self.max_abs_offset_steps,
                                    min(self.max_abs_offset_steps,
                                        int(requested_steps)))
        self.request_timestamp_ms = timestamp_ms
        return self.tick(timestamp_ms)

    def set_mode(self, mode: AutoVolumeMode, timestamp_ms: int):
        """Change selector mode; OFF targets zero, LOW/HIGH follow BCM levels."""
        self._check_time(timestamp_ms)
        if not isinstance(mode, AutoVolumeMode):
            raise ValueError("mode must be an AutoVolumeMode")
        self.mode = mode
        return self.tick(timestamp_ms)

    def manual_press(self, direction: int):
        """Pass a manual steering volume press without changing auto tracking."""
        if direction not in (-1, 1):
            raise ValueError("manual direction must be -1 or +1")
        return [VolumePulse(direction=direction, automatic=False)]

    def tick(self, timestamp_ms: int):
        """Emit at most one bounded automatic step if fresh data permits it."""
        self._check_time(timestamp_ms)
        if not self.baseline_known or self.requested_offset is None:
            return []
        if self.request_timestamp_ms is None:
            return []
        if timestamp_ms - self.request_timestamp_ms > self.offset_stale_timeout_ms:
            return []

        target = 0 if self.mode is AutoVolumeMode.OFF else self.requested_offset
        if target == self.commanded_offset:
            return []
        if (self.last_auto_pulse_ms is not None and
                timestamp_ms - self.last_auto_pulse_ms <
                self.min_auto_pulse_interval_ms):
            return []

        direction = 1 if target > self.commanded_offset else -1
        self.commanded_offset += direction
        self.last_auto_pulse_ms = timestamp_ms
        return [VolumePulse(direction=direction, automatic=True)]

    def controller_reset(self):
        """Mark the auto-contribution ledger unknown after MCU reset.

        Automatic pulses remain inhibited until a head-unit power cycle is
        confirmed, because the controller cannot know whether prior steps
        remain applied. Manual steering commands may still pass through.
        """
        self.requested_offset = None
        self.request_timestamp_ms = None
        self.commanded_offset = 0
        self.last_auto_pulse_ms = None
        self.baseline_known = False

    def confirm_head_unit_power_cycle(self, timestamp_ms: int):
        """Re-establish zero automatic contribution after a confirmed HU cycle."""
        self._check_time(timestamp_ms)
        self.commanded_offset = 0
        self.last_auto_pulse_ms = None
        self.baseline_known = True
        return self.tick(timestamp_ms)

    def _check_time(self, timestamp_ms: int):
        if timestamp_ms < 0:
            raise ValueError("timestamp_ms must be non-negative")
        if self._last_time_ms is not None and timestamp_ms < self._last_time_ms:
            raise ValueError("timestamp_ms must be monotonic")
        self._last_time_ms = timestamp_ms
