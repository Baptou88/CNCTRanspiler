import unittest

from H_Reader import HReader
from translator import Siemens
from writer import Writer



class TestH(unittest.TestCase):
    def test1(self):
        translator = Siemens()
        reader = HReader(translator)
        writer = Writer()
        reader.convert("4545 L X+10 Y-50")
        reader.convert("4546 L Y+0")
        a = reader.convert("4547 CR X+0 Y+10 R+10 DR+")
        self.assertEqual(a,"G03 X0.0 Y10.0 I=AC(0.0000) J=AC(0.0000)\n")
    
    def test2(self):
        translator = Siemens()
        reader = HReader(translator)
        writer = Writer()
        reader.convert("4545 L X-10 Y-50")
        reader.convert("4546 L Y+0")
        a = reader.convert("4547 CR X+0 Y+10 R+10 DR-")
        self.assertEqual(a,"G02 X0.0 Y10.0 I=AC(-0.0000) J=AC(0.0000)\n")
    
    def test3(self):
        translator = Siemens()
        reader = HReader(translator)
        writer = Writer()
        a=reader.convert("4545 CALL PGM TNC:\FIN")

        
        self.assertEqual(a,"")

if __name__ == "__main__":
    #verbose: 
    # 0 for quiet
    # 1 for normal
    # 2 for detailed
    unittest.main(verbosity=2)