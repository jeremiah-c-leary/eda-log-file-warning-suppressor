
import unittest
import warnings

from elfws import suppression
from elfws import suppression_list
from elfws import warning
from elfws import warning_list


lModules = [
    (warning, warning.LogWarning, 'warning.create is deprecated and will be removed in a future release, use warning.LogWarning instead.'),
    (warning_list, warning_list.WarningList, 'warning_list.create is deprecated and will be removed in a future release, use warning_list.WarningList instead.'),
    (suppression, suppression.Suppression, 'suppression.create is deprecated and will be removed in a future release, use suppression.Suppression instead.'),
    (suppression_list, suppression_list.SuppressionList, 'suppression_list.create is deprecated and will be removed in a future release, use suppression_list.SuppressionList instead.'),
]


class test_create_aliases(unittest.TestCase):

    def test_create_is_the_class(self):
        for oModule, oClass, sMessage in lModules:
            with self.subTest(module=oModule.__name__):
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore', DeprecationWarning)
                    self.assertIs(oClass, oModule.create)
                    self.assertIsInstance(oModule.create(), oClass)

    def test_create_can_be_subclassed(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', DeprecationWarning)

            class ParserWarning(warning.create):
                pass

        self.assertIsInstance(ParserWarning('ID', 'msg'), warning.LogWarning)

    def test_create_issues_deprecation_warning(self):
        for oModule, oClass, sMessage in lModules:
            with self.subTest(module=oModule.__name__):
                with self.assertWarns(DeprecationWarning) as oContext:
                    oModule.create
                self.assertEqual(sMessage, str(oContext.warning))

    def test_deprecation_warning_points_at_caller(self):
        with self.assertWarns(DeprecationWarning) as oContext:
            warning.create
        self.assertEqual(__file__, oContext.filename)

    def test_unknown_attribute_raises_attribute_error(self):
        with self.assertRaises(AttributeError) as oContext:
            warning.does_not_exist
        self.assertEqual("module 'elfws.warning' has no attribute 'does_not_exist'", str(oContext.exception))
