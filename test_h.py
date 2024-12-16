import unittest

from H_Reader import HReader
from translator import Siemens
from writer import Writer



class TestH(unittest.TestCase):
    def test1(self):
        translator = Siemens()
        reader = HReader(translator)

        reader.convert("4545 L X+10 Y-50")
        reader.convert("4546 L Y+0")
        a = reader.convert("4547 CR X+0 Y+10 R+10 DR+")
        self.assertEqual(a,"G03 X0.0 Y10.0 I=AC(0.0000) J=AC(0.0000)\n")
    
    def test2(self):
        translator = Siemens()
        reader = HReader(translator)

        reader.convert("4545 L X-10 Y-50")
        reader.convert("4546 L Y+0")
        a = reader.convert("4547 CR X+0 Y+10 R+10 DR-")
        self.assertEqual(a,"G02 X0.0 Y10.0 I=AC(-0.0000) J=AC(0.0000)\n")
    
    def test3(self):
        translator = Siemens()
        reader = HReader(translator)

        a=reader.convert("4545 CALL PGM TNC:\FIN")

        
        self.assertEqual(a,"CALL FIN.SPF\n")

    def test4(self):
        translator = Siemens()
        reader = HReader(translator)

        a=reader.convert("4545 L X+10.02 Y-10 Z0.02")

        
        self.assertEqual(a,"G01 X10.02 Y-10.0 Z0.02\n")

    def test5(self):
        translator = Siemens()
        reader = HReader(translator)

        a=reader.convert("4545 L X+10,02 Y-10 Z0,02")

        
        self.assertEqual(a,"G01 X10.02 Y-10.0 Z0.02\n")

    def testBlkForm(self):
        translator = Siemens()
        reader = HReader(translator)
        reader.convert("1 BLK FORM 0.1 Z X-175 Y0 Z-57,05")
        a=reader.convert("2 BLK FORM 0.2 X175 Y63 Z0")


        
        self.assertEqual(a,"min: {'X': -175.0, 'Y': 0.0, 'Z': -57.05}\nmax: {'X': 175.0, 'Y': 63.0, 'Z': 0.0}")


class TestCleValeur(unittest.TestCase):
    def test1(self):
        translator = Siemens()
        reader = HReader(translator)

        a = reader.CleValeur("X+10")
        result = {'X': float(10)}
        self.assertEqual(a,result)

if __name__ == "__main__":
    #verbose: 
    # 0 for quiet
    # 1 for normal
    # 2 for detailed
    unittest.main(verbosity=2)