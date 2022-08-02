import pytest 
class Test_libs:
    def test_importlibs(self):
        # Check if os import correctly
        import os
        assert type(os.getcwd()) == str

        # Check if re import correctly
        import re
        assert len(re.split("\ ", "This is a test.")) == 4 

        # Check if math import correctly
        import math
        assert print("{0:0.5f}".format(math.asin(0.5))) == \
               print("{0:0.5f}".format(math.pi * 30/180.))
    
