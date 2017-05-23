import unittest
from api.apiwrapper import TCOL


class TestStringMethods(unittest.TestCase):
    {
    def test_wrapper(self):
        input1 = "41.015137,28.979530,1000km"
        output1 = len(TCOL.get_topsongs(input1))
        return self.assertContains(output1, 10)


    def test_wrapper2(self):
        input2 = "999.015137,28.123123123123123,1000km"
        output2 = len(TCOL.get_topsongs(input2))
        return self.assertContains(output2, 10)

]