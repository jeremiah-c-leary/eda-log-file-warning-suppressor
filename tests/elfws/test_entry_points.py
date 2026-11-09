
import os
import subprocess
import sys
import unittest

from elfws import version


sRepoRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sExpected = 'EDA Log File Warning Suppressor (ELFWS) version ' + version.version


class test_entry_points(unittest.TestCase):

    def test_python_dash_m(self):
        oResult = subprocess.run([sys.executable, '-m', 'elfws', 'version'], cwd=sRepoRoot, capture_output=True, text=True)
        self.assertEqual(0, oResult.returncode)
        self.assertEqual(sExpected, oResult.stdout.strip())

    def test_bin_script_uses_checkout(self):
        oResult = subprocess.run([sys.executable, os.path.join(sRepoRoot, 'bin', 'elfws'), 'version'], cwd='/', capture_output=True, text=True)
        self.assertEqual(0, oResult.returncode)
        self.assertEqual(sExpected, oResult.stdout.strip())
