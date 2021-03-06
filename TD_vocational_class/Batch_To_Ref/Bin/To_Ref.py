# coding: utf-8 
__author__ = '財'
__time__ = '2018/11/1 0:39'

import os
import maya.cmds as mc
from Qt import QtWidgets, QtCompat, QtCore
import Tools


class ToRef(QtWidgets.QWidget):
    def __init__(self):
        super(ToRef, self).__init__()
        QtCompat.loadUi(r'J:\python\python_learn\TD_vocational_class\Batch_To_Ref\Ui\BTR.ui', self)
        self.file = None
        self.iter = None
        self.namespaces = None
        self.thread = MyThread()
        self.thread.signal.connect(self.update_process)
        self.toolButton.clicked.connect(self.get_file)
        self.refButton.clicked.connect(self.check_params)

    def update_process(self, value):
        """

        Args:
            value:

        Returns:

        """
        self.ref_Bar.setValue(value)
        # 如果100，完成
        if self.ref_Bar.value() == 100:
            return

    def get_file(self):
        """

        Returns:

        """
        # 获取文件路径
        self.file = QtWidgets.QFileDialog.getOpenFileName(self, u'选择参考文件1', Tools.get_project_path())[0]
        self.pathEdit.setText(self.file)

    def check_params(self):
        """

        Returns:

        """
        # 进度条归零
        if self.ref_Bar.value() != 0:
            self.ref_Bar.setValue(0)
        # 判断路径是不是空的
        if not self.pathEdit.text():
            mc.warning(u'请设置文件路径')
            return
            # 判断是否是文件
        elif not os.path.isfile(self.file):
            mc.warning(u'请选择一个正确的参考文件')
            return
        # 判断空间名是否为空
        elif not self.namespace_edit.text():
            # 警告用户，不能为空，不能用默认空间名
            mc.warning(u'请务必输入一个空间名')
            return
        else:
            # 获取空间名信息
            self.namespaces = self.namespace_edit.text()
        # 获取次数，默认为1
        self.iter = self.spinBox.value()
        return self.ref()

    def ref(self):
        self.thread.action(self.iter, self.file, self.namespaces)


class MyThread(QtCore.QThread):
    signal = QtCore.Signal(int)

    def __init__(self):
        super(MyThread, self).__init__()
        self.count = 0

    def action(self, iter_, filename, namespaces):
        index = iter_
        while iter_:
            mc.file(filename, r=True, ignoreVersion=True, gl=True, mergeNamespacesOnClash=False,
                    namespace=namespaces, options="mo=1")
            self.count += 1.0
            self.signal.emit(int((self.count / index) * 100))
            iter_ -= 1

        self.count = 0
