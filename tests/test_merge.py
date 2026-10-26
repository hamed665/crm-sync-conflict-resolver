import unittest
from mergedesk.core import merge, resolve, fingerprint, normalize, apply_if_unchanged

class MergeTests(unittest.TestCase):
    def test_independent_edits(self):
        p = merge({'a':1,'b':1},{'a':2,'b':1},{'a':1,'b':2})
        self.assertTrue(p['ready']); self.assertEqual(p['record'],{'a':2,'b':2})
    def test_conflict_requires_review(self):
        p = merge({'s':'new'},{'s':'won'},{'s':'lost'})
        self.assertFalse(p['ready']); self.assertEqual(p['record']['s'],'new')
        self.assertEqual(resolve(p,{'s':'remote'}),{'s':'lost'})
    def test_delete_vs_null(self):
        p = merge({'x':1},{},{'x':None})
        self.assertFalse(p['ready']); self.assertEqual(resolve(p,{'x':'local'}),{})
        self.assertEqual(resolve(p,{'x':'remote'}),{'x':None})
    def test_single_side_deletion(self):
        self.assertEqual(merge({'x':1},{},{'x':1})['record'],{})
    def test_same_addition(self):
        self.assertTrue(merge({},{'x':1},{'x':1})['ready'])
    def test_missing_decision(self):
        with self.assertRaises(ValueError): resolve(merge({}, {'x':1},{'x':2}),{})
    def test_fingerprint_order_and_stale(self):
        self.assertEqual(fingerprint({'a':1,'b':2}),fingerprint({'b':2,'a':1}))
        with self.assertRaises(ValueError): apply_if_unchanged({'a':2}, fingerprint({'a':1}),{})
    def test_no_mutation(self):
        b = {'x':[1]}; p = merge(b,b,b); p['record']['x'].append(2)
        self.assertEqual(b,{'x':[1]})
    def test_normalization_is_explicit(self):
        self.assertEqual(normalize({'name':' A  B ', 'email':' A@EXAMPLE.TEST '}),{'name':'A B','email':'a@example.test'})
