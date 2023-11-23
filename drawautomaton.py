from graphviz import *
dotstring_path = "sandbox/output/newfolder/myregex1.dotstring"


render('dot', 'png', dotstring_path).replace('\\', '/')
