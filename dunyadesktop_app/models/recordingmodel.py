from __future__ import absolute_import

from PyQt4 import QtGui


class RecordingModel(QtGui.QStandardItemModel):
    def __init__(self):
        QtGui.QStandardItemModel.__init__(self)
