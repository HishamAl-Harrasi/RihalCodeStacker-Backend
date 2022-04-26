import os
import pathlib

#print(os.path)

pwd = pathlib.Path(__file__).parent.resolve()
fileDir = "resumeFiles"
fileName = "test.pdf"

wholeName = os.path.join(pwd, fileDir, fileName)
print(wholeName)
