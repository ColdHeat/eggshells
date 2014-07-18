import hashlib

from PySide import QtGui, QtCore


def codefont():
    font = QtGui.QFont()
    font.setFamily("Consolas")
    font.setPointSize(10)
    return font


def hash(*args):
	for item in args:
		print "Hashes for {}".format( item )
		print "md5        {}".format( hashlib.md5(item).hexdigest() )
		print "sha1       {}".format( hashlib.sha1(item).hexdigest() )
		print "sha224     {}".format( hashlib.sha224(item).hexdigest() )
		print "sha256     {}".format( hashlib.sha256(item).hexdigest() )
		print "sha384     {}".format( hashlib.sha384(item).hexdigest() )
		print "sha512     {}\n".format( hashlib.sha512(item).hexdigest() )
