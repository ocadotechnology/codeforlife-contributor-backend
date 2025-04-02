"""
© Ocado Group
Created on 01/04/2025 at 09:25:12(+01:00).
"""

from codeforlife.tests import CeleryTestCase

# pylint: disable=missing-class-docstring


class TestSession(CeleryTestCase):
    def test_clear(self):
        """Can clear all expired sessions."""
        self.apply_periodic_task("clear_sessions")
