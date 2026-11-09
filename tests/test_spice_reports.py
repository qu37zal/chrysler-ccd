"""A solved circuit must not be mistaken for a passing electrical experiment."""
import json
from pathlib import Path
import tempfile
import unittest
from simulation.run_ltspice import assess


class SpiceReportTests(unittest.TestCase):
    def report(self, measurements, completed=True):
        with tempfile.TemporaryDirectory() as directory:
            circuit=Path(directory)/'buck.cir'
            circuit.write_text('* synthetic report test\n.end\n')
            log='LTspice test log\n'
            if completed:
                log+='Total elapsed time: 1 seconds.\n'
            log+='\n'.join(f'{name}: AVG(V(out))={value} FROM 0 TO 1' for name,value in measurements.items())
            circuit.with_suffix('.log').write_text(log)
            result=assess(circuit)
            saved=json.loads((circuit.parent/'results/buck_ltspice.json').read_text())
            self.assertEqual(result,saved)
            return result

    def test_unregulated_supply_fails_despite_completed_solver(self):
        result=self.report(dict(vout_light=0.001,vout_heavy=-0.1,vout_min=-0.7,
                                vout_max=0.4,inductor_peak=0.8))
        self.assertTrue(result['completed'])
        self.assertFalse(result['pass'])

    def test_missing_measurement_fails(self):
        result=self.report(dict(vout_light=5.0,vout_heavy=5.0,vout_min=4.9,vout_max=5.1))
        self.assertIsNone(result['checks']['inductor_peak']['value'])
        self.assertFalse(result['pass'])

    def test_complete_good_measurements_pass_but_incomplete_log_fails(self):
        values=dict(vout_light=5.0,vout_heavy=5.0,vout_min=4.9,vout_max=5.1,inductor_peak=0.8)
        self.assertTrue(self.report(values)['pass'])
        self.assertFalse(self.report(values,completed=False)['pass'])
