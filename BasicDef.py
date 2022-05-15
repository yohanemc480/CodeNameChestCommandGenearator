import os
Indention = '\n'
PathBase = os.path.dirname(__file__) + '/'#このファイルがあるディレクトリ

def Write(Contents,Path):#パスと書き込み内容を指定して、ファイル内容の書き込みをする。
  Path = PathBase + Path
  with open(Path,'w') as WriteFile:
    WriteFile.write(Contents)
def Read(Path):#指定したパスにあるファイル内容を返す
  Path= PathBase + Path
  with open(Path,'r') as ReadFile:
    return ReadFile.read()