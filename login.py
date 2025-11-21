import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt5.QtWidgets import *
from PyQt5 import uic   # ui 파일을 사용하기 위한 모듈 import
from PyQt5.QtCore import Qt
from PyQt5.QAxContainer import QAxWidget
from main import mainWindow
import configparser
from pysbapi import pySBtraderOCX
from PyQt5.QtGui import QFont, QIcon
import resources  # 디자인 리소스

class WindowClass(QMainWindow) :

    def __init__(self) :
        super().__init__()
        path = 'login_View.ui'       
        uic.loadUi(path,self)
        self.setWindowIcon(QIcon('./icon/taskbaricon.png'))

        # 설정파일
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')

        # 마스터 파일 다운로드 경로
        self.data_path = config.get('PATH', 'data_path')
        self.NH_filespace = self.data_path
        ocx_module_name = config.get('PATH', 'ocx_module_name')

        self.pySBtrader = pySBtraderOCX(ocx_module_name)
        self.lineEdit_ID.setText(config["SYSTEM"]["id"])

        self.socket_status = 1
        self.connection = False

        # OCX를 문서파일로 내보내기
        with open(os.path.dirname(os.path.realpath(__file__)) + "\\documentation.txt", 'w+') as f:
            f.write(self.pySBtrader.SBtrader.generateDocumentation())

        # 주요 시그널 연결
        self.pySBtrader.SBtrader.LoginOK.connect(self.connectLoginOK)
        self.pySBtrader.SBtrader.SocketClosed.connect(self.connectSocketClosed)
        self.pySBtrader.SBtrader.FinMasterdown.connect(self.connectFinMasterdown)

        # 디자인 컴포넌트들 세팅
        self.LoginButton.setEnabled(False)
        self.lineEdit_PW.setEchoMode(QLineEdit.Password)
        self.lineEdit_CERT.setEchoMode(QLineEdit.Password) 

        # 버튼 함수 연결
        self.LoginButton.clicked.connect(self.LoginProcess)

        # 로그인 버튼 활성화 함수 연결
        self.lineEdit_ID.textChanged.connect(self.update_login_button_state)
        self.lineEdit_PW.textChanged.connect(self.update_login_button_state)
        self.lineEdit_CERT.textChanged.connect(self.update_login_button_state)

    def update_login_button_state(self):

        """사용자 이름과 비밀번호가 모두 입력되면 로그인 버튼을 활성화"""

        if self.practiceButton.isChecked():
            if self.lineEdit_ID.text() and self.lineEdit_PW.text():
                self.LoginButton.setEnabled(True)
            else:
                self.LoginButton.setEnabled(False)
        if self.actualButton.isChecked():
            if self.lineEdit_ID.text() and self.lineEdit_PW.text() and self.lineEdit_CERT.text():
                self.LoginButton.setEnabled(True)
            else:
                self.LoginButton.setEnabled(False)

    def LoginProcess(self):

        if self.connection == True:
            self.pySBtrader.doMasterDownload()
        else: 
            result = self.pySBtrader.doConnect()
            if result == 1:
                self.showPopupWindow("서버 연결 성공")
                self.connection = True
                self.pySBtrader.doMasterDownload()
            else:
                self.showPopupWindow("서버 연결 실패")

    def login(self):

        if self.practiceButton.isChecked():

            self.id = self.lineEdit_ID.text()
            pwd = self.lineEdit_PW.text()
            cert_pwd = self.lineEdit_CERT.text()
            self.pySBtrader.doLogin(2, self.id, pwd, cert_pwd, 0)

        if self.actualButton.isChecked():

            self.id = self.lineEdit_ID.text()
            pwd = self.lineEdit_PW.text()
            cert_pwd = self.lineEdit_CERT.text()
            self.pySBtrader.doLogin(0, self.id, pwd, cert_pwd, 0)

    def save_id(self):

        # 아이디 저장
        if os.path.exists("./config.ini"):
            config = configparser.ConfigParser()
            config.read('./config.ini')
            config.set('SYSTEM', 'id', self.id)
            with open('./config.ini', 'w+') as f:
                config.write(f)

        else:
            config = configparser.ConfigParser()
            config.read('./config.ini')
            config.add_section('SYSTEM')
            config.set('SYSTEM', 'id', self.id)
            with open('./config.ini', 'w+') as f:
                config.write(f)

    def afterlogin(self):

        self.save_id()
        self.w = mainWindow(self.pySBtrader, self.data_path)
        self.w.show()
        self.hide()

    def connectSocketClosed(self, errcode):

        if errcode == 0:
            self.socket_status = 0

        else:
            self.socket_status = 1
            self.showPopupWindow("연결 끊김")
            self.connection = False

    def connectFinMasterdown(self, result):

        if result == 1:
            self.showPopupWindow("마스터 파일 다운로드 완료")
            self.login()

        else:
            self.showPopupWindow("마스터 파일 다운로드 실패")

    def connectLoginOK(self, errcode: str, recvData: str):
        """
        로그인 응답 이벤트.
            Args:
                Errcode`str`: 00000일 시 정상, 아닌 경우는 5자리의 숫자로 반환.
                RecvData`str`: 정상(00000) 일 경우 SCBS0000Q01 output 구조체 전달 (로그인 정보)
            Returns:
                None
        """
        # 로그인 정상
        if errcode == "00000":
            self.showPopupWindow("로그인 성공")
            self.afterlogin()
        # 로그인 에러
        else:
            self.showPopupWindow("로그인 에러코드: {}, 에러메세지: {}".format(errcode, recvData))

    def showPopupWindow(self, text):

        msg = QMessageBox()
        msg.setText(text) # 윈도우에 내용
        msg.setWindowTitle("Alarm") # 윈도우 제목
        msg.setWindowModality(Qt.ApplicationModal) # 모달 형식
        msg.exec_() # 메시지창을 띄워라

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Inter", 9)
    app.setFont(font)
    Window = WindowClass() 
    Window.show()
    app.exec_()
