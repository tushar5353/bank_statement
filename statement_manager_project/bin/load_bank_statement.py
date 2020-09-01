import os
import sys

current_path =os.path.dirname(os.path.abspath(__file__))+'/../'
sys.path.append(current_path+"config/")
sys.path.append(current_path+"lib/")
sys.path.append(current_path+"utility/")
sys.path.append(current_path+"stage/")
sys.path.append(current_path+"master/")

from LoadData import *


obj = LoadStatementData()
obj.run()
