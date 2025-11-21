import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QCheckBox, QTableWidgetItem, QTableWidget, QLineEdit
from PyQt5.QtWidgets import *
from PyQt5 import uic   # ui 파일을 사용하기 위한 모듈 import
from PyQt5.QtCore import Qt, QVariant, QTimer, QDateTime
from PyQt5.QtGui import QColor
from PyQt5.QAxContainer import QAxWidget
from ExtendedComboBox import ExtendedComboBox
from apscheduler.schedulers.background import BackgroundScheduler
import time
import datetime
import configparser
from PyQt5.QtGui import QFont, QTextCharFormat, QIcon

currentpath = os.getcwd()        # 현재 작업 디렉터리 얻기

class mainWindow(QMainWindow) :
    def __init__(self, SBtrader: QAxWidget, data_path) :
        super().__init__()
        path = currentpath +'\main_View.ui'       
        uic.loadUi(path,self)   
        self.setWindowIcon(QIcon(currentpath + './icon/taskbaricon.png'))

        self.sched = BackgroundScheduler()

        self.checkbox_list = []
        self.gcbon_list = []
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        self.NH_filespace = data_path
        self.pySBtrader = SBtrader      
        self.stock_rel_name_code_dict = {}
        self.stock_rel_code_relcode_dict = {}
        self.stock_rel_code_name_dict = {}
        self.stock_rel_code_ctrt_size_dict = {}
        self.global_stock_rel_name_code_dict = {}
        self.global_stock_rel_code_relcode_dict = {}
        self.global_stock_rel_code_name_dict = {}
        self.global_stock_rel_code_exchange_dict = {}
        self.global_stock_rel_code_ctrt_size_dict = {}
        self.current_hoga_stock_code = ''
        self.global_current_hoga_stock_code = ''

        self.dataseq = ''
        self.register_real_list = []
        self.datatable_stock_list = []
        self.global_datatable_stock_list = []
        self.acc_no = ''
        self.acc_no_glb = ''
        self.encoded_pwd = ''
        self.encoded_pwd_glb = ''
        self.pwd = ''
        self.glb_pwd = ''

        # 시그널 연결
        self.pySBtrader.SBtrader.ReceiveData.connect(self.connectReceiveData)
        self.pySBtrader.SBtrader.ReceiveReal.connect(self.connectReceiveReal)       

        # 버튼 연결
        self.button_connect_acc.clicked.connect(self.connectAccount)        
        self.button_connect_acc_glb.clicked.connect(self.connectGlobalAccount)        
        self.button_load_acc.clicked.connect(self.doGetAccountInfAll)
        self.button_load_acc_glb.clicked.connect(self.doGetGlobalAccountInfAll)
        self.button_add.clicked.connect(self.addStock)
        self.button_add_glb.clicked.connect(self.addGlobalStock)
        self.button_delete.clicked.connect(self.deleteStock) 
        self.button_delete_glb.clicked.connect(self.deleteGlobalStock) 
        self.button_delete_all.clicked.connect(self.deleteStockAll)
        self.button_delete_all_glb.clicked.connect(self.deleteGlobalStockAll)
        self.button_buy.clicked.connect(self.buystock)
        self.button_buy_glb.clicked.connect(self.buyGlobalstock)
        self.button_sell.clicked.connect(self.sellstock)
        self.button_sell_glb.clicked.connect(self.sellGlobalstock)
        self.button_modify.clicked.connect(self.modifystock)
        self.button_modify_glb.clicked.connect(self.modifyGlobalstock)
        self.button_cancel.clicked.connect(self.cancelstock)
        self.button_cancel_glb.clicked.connect(self.cancelGlobalstock)

        # 호가 종목 클릭 
        self.dataTable.cellClicked.connect(self.connectHoga)
        self.dataTable_glb.cellClicked.connect(self.connectGlobalHoga)

        # 하단 link button group 비활성화
        self.button_wikidocs.setEnabled(False)
        self.button_api.setEnabled(False)
        self.button_youtube.setEnabled(False)
        self.button_faq.setEnabled(False)
        self.button_wikidocs_glb.setEnabled(False)
        self.button_api_glb.setEnabled(False)
        self.button_youtube_glb.setEnabled(False)
        self.button_faq_glb.setEnabled(False)

        # 계좌 연결하기 전 매수매도 비활성화
        self.button_buy.setEnabled(False)
        self.button_sell.setEnabled(False)
        self.button_modify.setEnabled(False)
        self.button_cancel.setEnabled(False)
        self.button_buy_glb.setEnabled(False)
        self.button_sell_glb.setEnabled(False)
        self.button_modify_glb.setEnabled(False)
        self.button_cancel_glb.setEnabled(False)

        # table header길이 수정
        self.dataTable.verticalHeader().setVisible(False)
        self.dataTable.setColumnWidth(0, 140)
        self.dataTable.setColumnWidth(1, 100)
        for i in range(2, 5):
            self.dataTable.setColumnWidth(i, 60)
        for i in range(5, 6):
            self.dataTable.setColumnWidth(i, 100)
        for i in range(6, 7):
            self.dataTable.setColumnWidth(i, 60)

        self.dataTable_glb.verticalHeader().setVisible(False)
        self.dataTable_glb.setColumnWidth(0, 140)
        self.dataTable_glb.setColumnWidth(1, 100)
        for i in range(2, 5):
            self.dataTable_glb.setColumnWidth(i, 60)
        for i in range(5, 6):
            self.dataTable_glb.setColumnWidth(i, 100)
        for i in range(6, 7):
            self.dataTable_glb.setColumnWidth(i, 60)

        self.ExecutionTable.verticalHeader().setVisible(False)
        self.ExecutionTable.setColumnWidth(0, 140)
        self.ExecutionTable.setColumnWidth(1, 100)
        for i in range(2, 7):
            self.ExecutionTable.setColumnWidth(i, 60)
        for i in range(7, 9):
            self.ExecutionTable.setColumnWidth(i, 100)

        self.ExecutionTable_glb.verticalHeader().setVisible(False)
        self.ExecutionTable_glb.setColumnWidth(0, 140)
        self.ExecutionTable_glb.setColumnWidth(1, 100)
        for i in range(2, 7):
            self.ExecutionTable_glb.setColumnWidth(i, 60)
        for i in range(7, 9):
            self.ExecutionTable_glb.setColumnWidth(i, 100)

        self.OpeninterestTable.verticalHeader().setVisible(False)
        self.OpeninterestTable.setColumnWidth(0, 140)
        self.OpeninterestTable.setColumnWidth(1, 60)
        self.OpeninterestTable.setColumnWidth(2, 80)
        for i in range(3, 7):
            self.OpeninterestTable.setColumnWidth(i, 100)
        self.OpeninterestTable.setColumnWidth(7, 60)

        self.OpeninterestTable_glb.verticalHeader().setVisible(False)
        self.OpeninterestTable_glb.setColumnWidth(0, 140)
        self.OpeninterestTable_glb.setColumnWidth(1, 60)
        self.OpeninterestTable_glb.setColumnWidth(2, 80)
        for i in range(3, 7):
            self.OpeninterestTable_glb.setColumnWidth(i, 100)
        self.OpeninterestTable_glb.setColumnWidth(7, 60)

        # 국내 호가 테이블 초기화
        self.HogaTable.verticalHeader().setVisible(False)
        self.HogaTable.setColumnWidth(2, 80)

        for i in range(self.HogaTable.columnCount()):
            if i != 2:
                self.HogaTable.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        self.HogaTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)       

        # 해외 호가 테이블 초기화 
        self.HogaTable_glb.verticalHeader().setVisible(False)
        self.HogaTable_glb.setColumnWidth(2, 80)

        for i in range(self.HogaTable_glb.columnCount()):
            if i != 2:
                self.HogaTable_glb.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)  
        self.HogaTable_glb.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # combo
        # 국내선물
        self.combo_stockname2 = ExtendedComboBox(self.combo_stockname)
        self.combo_stockname2.setStyleSheet("QComboBox { border: 1px solid #e0e4e7; border-radius: 4px; padding: 5px 15px; } QComboBox:hover { border: 1px solid #0091F0; } QComboBox::drop-down { background-color: #FFFFFF; border-radius: 4px;  padding-right: 4px; } QComboBox::down-arrow {  image: url(:/image/images/down_arrow.png); width: 20px; height: 10px; }")
        self.combo_stockname.hide()
        self.combo_stockname = self.combo_stockname2
        self.combo_stockname.setMinimumSize(250,30)
        self.ChoiceLayout.insertWidget(2, self.combo_stockname2)

        self.combo_stockcode2 = ExtendedComboBox(self.combo_stockname)
        self.combo_stockcode2.setStyleSheet("QComboBox { border: 1px solid #e0e4e7; border-radius: 4px; padding: 5px 15px; } QComboBox:hover { border: 1px solid #0091F0; } QComboBox::drop-down { background-color: #FFFFFF; border-radius: 4px;  padding-right: 4px; } QComboBox::down-arrow {  image: url(:/image/images/down_arrow.png); width: 20px; height: 10px; }")
        self.combo_stockcode.hide()
        self.combo_stockcode = self.combo_stockcode2
        self.combo_stockcode.setMaximumSize(300,30)     
        self.ChoiceLayout_3.insertWidget(1, self.combo_stockcode)

        # 해외선물
        self.combo_stockname_glb2 = ExtendedComboBox(self.combo_stockname_glb)
        self.combo_stockname_glb2.setStyleSheet("QComboBox { border: 1px solid #e0e4e7; border-radius: 4px; padding: 5px 15px; } QComboBox:hover { border: 1px solid #0091F0; } QComboBox::drop-down { background-color: #FFFFFF; border-radius: 4px;  padding-right: 4px; } QComboBox::down-arrow {  image: url(:/image/images/down_arrow.png); width: 20px; height: 10px; }")
        self.combo_stockname_glb.hide()
        self.combo_stockname_glb = self.combo_stockname_glb2
        self.combo_stockname_glb.setMinimumSize(250,30)
        self.ChoiceLayout_5.insertWidget(2, self.combo_stockname_glb)

        self.combo_stockcode_glb2 = ExtendedComboBox(self.combo_stockname_glb)
        self.combo_stockcode_glb2.setStyleSheet("QComboBox { border: 1px solid #e0e4e7; border-radius: 4px; padding: 5px 15px; } QComboBox:hover { border: 1px solid #0091F0; } QComboBox::drop-down { background-color: #FFFFFF; border-radius: 4px;  padding-right: 4px; } QComboBox::down-arrow {  image: url(:/image/images/down_arrow.png); width: 20px; height: 10px; }")
        self.combo_stockcode_glb.hide()
        self.combo_stockcode_glb = self.combo_stockcode_glb2
        self.combo_stockcode_glb.setMaximumSize(300,30)     
        self.ChoiceLayout_8.insertWidget(1, self.combo_stockcode_glb)

        # 주야간 변수
        self.daynight = "1"
        self.dayNight()
        self.getAllStockList()
        self.getAllGlobalStockList()

        # 시장가, 지정가 comboBox setting
        self.edit_price.setEnabled(False)
        self.edit_price_glb.setEnabled(False)
        self.combo_order_type.currentIndexChanged.connect(self.priceChoice)
        self.combo_order_type_glb.currentIndexChanged.connect(self.priceGlobalChoice)
        self.combo_searchtype.currentIndexChanged.connect(self.onChangedSearchType)
        self.combo_searchtype_glb.currentIndexChanged.connect(self.onChangedSearchTypeGlb)

        self.sched.start()
        self.sched.add_job(self.dayNight, 'interval', minutes=1, id='daynight')

    def onChangedSearchType(self):

        # 종목명
        if self.combo_searchtype.currentText() == "종목명":
            self.combo_stockname.clear()
            self.combo_stockname.addItems(["", *list(self.stock_rel_name_code_dict.keys())])

        # 종목코드
        else:
            self.combo_stockname.clear()
            self.combo_stockname.addItems(["", *list(self.stock_rel_code_name_dict.keys())])

    def onChangedSearchTypeGlb(self):

        # 종목명
        if self.combo_searchtype_glb.currentText() == "종목명":
            self.combo_stockname_glb.clear()
            self.combo_stockname_glb.addItems(["", *list(self.global_stock_rel_name_code_dict.keys())])
        # 종목코드
        else:
            self.combo_stockname_glb.clear()
            self.combo_stockname_glb.addItems(["", *list(self.global_stock_rel_code_name_dict.keys())])

    def priceChoice(self):

        '''시장가, 지정가 comboBox 선택에 따라 금액 editBox 활성,비활성'''

        if self.combo_order_type.currentText() == '시장가':
            self.edit_price.setEnabled(False)
            self.edit_price.setText('')
        elif self.combo_order_type.currentText() == '지정가':
            self.edit_price.setText('')
            self.edit_price.setEnabled(True)
        else:
            self.edit_price.setText('')
            self.edit_price.setEnabled(False)

    def priceGlobalChoice(self):

        '''시장가, 지정가 comboBox 선택에 따라 금액 editBox 활성,비활성'''

        if self.combo_order_type_glb.currentText() == '시장가':
            self.edit_price_glb.setEnabled(False)
            self.edit_price_glb.setText('')
        elif self.combo_order_type_glb.currentText() == '지정가':
            self.edit_price_glb.setText('')
            self.edit_price_glb.setEnabled(True)
        else:
            self.edit_price_glb.setText('')
            self.edit_price_glb.setEnabled(False)

    def dayNight(self):

        """주야간 구분해주는 함수. 스케줄러에 등록해서 사용"""

        now = datetime.datetime.now().time()
        if now.hour >= 18 or now.hour < 6:
            if self.daynight == '1':
                self.daynight = "2"
                self.getAllStockList()              

        else:
            if self.daynight == '2':
                self.daynight = "1"
                self.getAllStockList()      

    def updateAccountInfo(self):

        """계좌 정보 업데이트. 스케줄러에 등록 후 사용"""

        date_string = datetime.datetime.today().strftime('%Y%m%d')
        data_string = date_string + self.acc_no + self.encoded_pwd
        self.pySBtrader.doRequestData(-1, "sdbs5001q01", data_string, "", "")

    def updateGlobalAccountInfo(self):

        """계좌 정보 업데이트. 스케줄러에 등록 후 사용"""

        date_string = datetime.datetime.today().strftime('%Y%m%d')
        data_string = date_string + self.acc_no_glb + 'USD1' + self.encoded_pwd_glb
        self.pySBtrader.doRequestData(-1, "SGBS3205Q01", data_string, "", "")

    def doGetAccountInfAll(self):

        cnt = self.pySBtrader.doGetAccountInfCount()
        acc_list = []
        for i in range(0, cnt):
            acc_info = self.pySBtrader.doGetAccountInf(i)
            acc_list.append(acc_info)

        self.AccountChoice.clear()
        for acc_info in acc_list:
            if len(acc_info) >= 7 and acc_info[6] == '1':
                self.AccountChoice.addItem(acc_info)
        self.textEdit_table.append("계좌를 불러왔습니다.")

    def doGetGlobalAccountInfAll(self):

        cnt = self.pySBtrader.doGetAccountInfCount()
        acc_list = []
        for i in range(0, cnt):
            acc_info = self.pySBtrader.doGetAccountInf(i)
            acc_list.append(acc_info)

        self.AccountChoice_glb.clear()
        for acc_info in acc_list:
            if len(acc_info) >= 7 and acc_info[6] == '2':
                self.AccountChoice_glb.addItem(acc_info)
        self.textEdit_table_glb.append("계좌를 불러왔습니다.")   

    # 국내 계좌 연결
    def connectAccount(self):

        """버튼 눌렀을시 국내 계정연결"""

        self.acc_no = self.AccountChoice.currentText()
        date_string = datetime.datetime.today().strftime('%Y%m%d')
        pwd_text = self.lineEdit_acc_pwd.text()
        if pwd_text == "":
            self.showPopupWindow("계좌 비밀번호를 입력하세요.")
            self.button_connect_acc.setEnabled(True) 
            return
        self.pwd = self.lineEdit_acc_pwd.text()
        self.encoded_pwd = self.pySBtrader.getEncodeText(self.lineEdit_acc_pwd.text())
        data_string = date_string + self.acc_no + self.encoded_pwd
        self.pySBtrader.doRequestData(-1, "sdbs5001q01", data_string, "", "")
        self.pySBtrader.doRegistReal('O1', self.acc_no)
        self.textEdit_table.append("{}에 연결되었습니다.".format(self.acc_no))

        # sdbs3085q01: 초기 미결제 조회
        data_string = "1" + self.acc_no + self.encoded_pwd + self.daynight + ' ' * 156
        self.pySBtrader.doRequestData(-1, "sdbs3085q01", data_string, "", "")

        # sdbs3066q01: 초기 체결 조회
        data_string = "11" + ' ' * 8 + self.acc_no + self.encoded_pwd + ' ' * 50 + '00' + ' ' * 32 + '00010 Y   ' + ' ' * 101
        self.pySBtrader.doRequestData(-1, "sdbs3066q01", data_string, "", "")

        # sdbs3066q01: 초기 미체결 조회
        data_string = "11" + ' ' * 8 + self.acc_no + self.encoded_pwd + ' ' * 50 + '00' + ' ' * 32 + '00020 Y   ' + ' ' * 101
        self.pySBtrader.doRequestData(-1, "sdbs3066q01", data_string, "", "")

        # 5초마다 계좌 정보 업데이트
        self.sched.add_job(self.updateAccountInfo, 'interval', seconds=5, id='updateAccountInfo') 
        self.button_connect_acc.setEnabled(False)

        self.button_buy.setEnabled(True)
        self.button_sell.setEnabled(True)
        self.button_modify.setEnabled(True)
        self.button_cancel.setEnabled(True)

    # 해외 계좌 연결
    def connectGlobalAccount(self):

        """버튼 눌렀을시 해외 계정연결"""

        self.acc_no_glb = self.AccountChoice_glb.currentText()
        # SGBS3205Q01
        date_string = datetime.datetime.today().strftime('%Y%m%d')
        pwd_text = self.lineEdit_acc_pwd_glb.text()
        while pwd_text == "": # password가 없을 시
            self.showPopupWindow("계좌 비밀번호를 입력하세요.")
            self.button_connect_acc_glb.setEnabled(True) # 버튼 활성화
            return
        self.glb_pwd = self.lineEdit_acc_pwd_glb.text()
        self.encoded_pwd_glb = self.pySBtrader.getEncodeText(self.glb_pwd)
        data_string = date_string + self.acc_no_glb + 'USD1' + self.encoded_pwd_glb
        self.pySBtrader.doRequestData(-1, "SGBS3205Q01", data_string, "", "")
        self.pySBtrader.doRegistReal('O1', self.acc_no_glb)
        self.textEdit_table_glb.append("{}에 연결되었습니다.".format(self.acc_no_glb))

        # sdbs3085q01: 초기 미결제 조회
        data_string = "0" * 100 + '2' + self.acc_no_glb + ' ' * 50 + '9'
        self.pySBtrader.doRequestData(-1, "sgbs9001q03", data_string, "", "")

        # sdbs3066q01: 초기 체결, 미체결 조회
        data_string = "9" * 100 + '2' + self.acc_no_glb + ' ' * 50 + '0' +  ' ' * 10 + '09'
        self.pySBtrader.doRequestData(-1, "sgbs9001q01", data_string, "", "")

        # 5초마다 계좌 정보 업데이트
        self.sched.add_job(self.updateGlobalAccountInfo, 'interval', seconds=5, id='updateGlobalAccountInfo') 
        self.button_connect_acc_glb.setEnabled(False)

        self.button_buy_glb.setEnabled(True)
        self.button_sell_glb.setEnabled(True)
        self.button_modify_glb.setEnabled(True)
        self.button_cancel_glb.setEnabled(True)

    def buystock(self):

        if self.combo_order_type.currentText() == "시장가":
            if self.combo_stockcode.currentText():
                if self.edit_amount != 0:
                    code = self.combo_stockcode.currentText().split("(")[0].replace(' ', '')
                    amount = self.edit_amount.text()
                    price = self.edit_price.text()

                    self.dataseq = self.pySBtrader.doRequestDomNewOrder(self.daynight, self.acc_no, self.pwd, code, "1", "2", "1", amount, 0, '')
                    self.textEdit_table.append("{}, {} 매수 주문이 들어 갔습니다.".format(code, amount))
                else:
                    self.textEdit_table.append("수량을 입력해주세요.")
            else:
                self.textEdit_table.append("종목을 선택해주세요.")


        elif self.combo_order_type.currentText() == "지정가":
            if self.combo_stockcode.currentText():
                if self.edit_price.text() != "":
                    if self.edit_amount != 0:
                        code = self.combo_stockcode.currentText().split("(")[0].replace(' ', '')
                        amount = self.edit_amount.text()
                        price = self.edit_price.text()

                        self.dataseq = self.pySBtrader.doRequestDomNewOrder(self.daynight, self.acc_no, self.pwd, code, "1", "1", "1", amount, price, '')
                        self.textEdit_table.append("{}, {} 매수 주문이 들어 갔습니다.".format(code, amount))

                    else:
                        self.textEdit_table.append("수량을 입력해주세요.")
                else:
                    self.textEdit_table.append("가격을 입력해주세요.")
            else:
                self.textEdit_table.append("종목을 선택해주세요.")

    def buyGlobalstock(self):

        if self.combo_order_type_glb.currentText() == "시장가":
            if self.combo_stockcode_glb.currentText():
                if self.edit_amount_glb != 0:
                    code = self.combo_stockcode_glb.currentText().split("(")[0].replace(' ', '')
                    amount = self.edit_amount_glb.text()
                    price = self.edit_price_glb.text()

                    self.dataseq = self.pySBtrader.doRequestGlbNewOrder(self.acc_no_glb, self.glb_pwd, code, "1", "1", amount, '', '', '0', '', '')
                    self.textEdit_table_glb.append("{}, {} 매수 주문이 들어 갔습니다.".format(code, amount))
                else:
                    self.textEdit_table_glb.append("수량을 입력해주세요.")
            else:
                self.textEdit_table_glb.append("종목을 선택해주세요.")


        elif self.combo_order_type_glb.currentText() == "지정가":
            if self.combo_stockcode_glb.currentText():
                if self.edit_price_glb.text() != "":
                    if self.edit_amount_glb != 0:
                        code = self.combo_stockcode_glb.currentText().split("(")[0].replace(' ', '') 
                        amount = self.edit_amount_glb.text()
                        price = self.edit_price_glb.text()

                        self.dataseq = self.pySBtrader.doRequestGlbNewOrder(self.acc_no_glb, self.glb_pwd, code, "1", "2", amount, price, '', '0', '', '')
                        self.textEdit_table_glb.append("{}, {} 매수 주문이 들어 갔습니다.".format(code, amount))

                    else:
                        self.textEdit_table_glb.append("수량을 입력해주세요.")
                else:
                    self.textEdit_table_glb.append("가격을 입력해주세요.")
            else:
                self.textEdit_table_glb.append("종목을 선택해주세요.")

    def sellstock(self):

        if self.combo_order_type.currentText() == "시장가":
            if self.combo_stockcode.currentText():
                if self.edit_amount != 0:
                    code = self.combo_stockcode.currentText().split("(")[0].replace(' ', '')
                    amount = self.edit_amount.text()
                    price = self.edit_price.text()

                    self.dataseq = self.pySBtrader.doRequestDomNewOrder(self.daynight, self.acc_no, self.pwd, code, "2", "2", "1", amount, 0, '')
                    self.textEdit_table.append("{}, {} 매도 주문이 들어 갔습니다.".format(code, amount))
                else:
                    self.textEdit_table.append("수량을 입력해주세요.")
            else:
                self.textEdit_table.append("종목을 선택해주세요.")

        elif self.combo_order_type.currentText() == "지정가":
            if self.combo_stockcode.currentText():
                if self.edit_price.text() != "":
                    if self.edit_amount != 0:
                        code = self.combo_stockcode.currentText().split("(")[0].replace(' ', '')
                        amount = self.edit_amount.text()
                        price = self.edit_price.text()

                        self.dataseq = self.pySBtrader.doRequestDomNewOrder(self.daynight, self.acc_no, self.pwd, code, "2", "1", "1", amount, price, '')
                        self.textEdit_table.append("{}, {} 매도 주문이 들어 갔습니다.".format(code, amount))
                    else:
                        self.textEdit_table.append("수량을 입력해주세요.")
                else:
                    self.textEdit_table.append("가격을 입력해주세요.")
            else:
                self.textEdit_table.append("종목을 선택해주세요.")

    def sellGlobalstock(self):

        if self.combo_order_type_glb.currentText() == "시장가":
            if self.combo_stockcode_glb.currentText():
                if self.edit_amount_glb != 0:
                    code = self.combo_stockcode_glb.currentText().split("(")[0].replace(' ', '')
                    amount = self.edit_amount_glb.text()
                    price = self.edit_price_glb.text()

                    self.dataseq = self.pySBtrader.doRequestGlbNewOrder(self.acc_no_glb, self.glb_pwd, code, "2", "1", amount, '', '', '0', '', '')
                    self.textEdit_table_glb.append("{}, {} 매도 주문이 들어 갔습니다.".format(code, amount))
                else:
                    self.textEdit_table_glb.append("수량을 입력해주세요.")
            else:
                self.textEdit_table_glb.append("종목을 선택해주세요.")

        elif self.combo_order_type_glb.currentText() == "지정가":
            if self.combo_stockcode_glb.currentText():
                if self.edit_price_glb.text() != "":
                    if self.edit_amount_glb != 0:
                        code = self.combo_stockcode_glb.currentText().split("(")[0].replace(' ', '')
                        amount = self.edit_amount_glb.text()
                        price = self.edit_price_glb.text()

                        self.dataseq = self.pySBtrader.doRequestGlbNewOrder(self.acc_no_glb, self.glb_pwd, code, "2", "2", amount, price, '', '0', '', '')
                        self.textEdit_table_glb.append("{}, {} 매도 주문이 들어 갔습니다.".format(code, amount))
                    else:
                        self.textEdit_table_glb.append("수량을 입력해주세요.")
                else:
                    self.textEdit_table_glb.append("가격을 입력해주세요.")
            else:
                self.textEdit_table_glb.append("종목을 선택해주세요.")

    def modifystock(self):

        row_num = self.ExecutionTable.currentRow()
        if row_num == -1:
            self.textEdit_table.append("정정할 주문을 선택해주세요.")
        else:
            if self.edit_price.text() != "":
                if self.edit_amount.text() != "":
                    stock_name = self.ExecutionTable.item(row_num, 0).text()
                    code = self.stock_rel_name_code_dict[stock_name]
                    ord_num = self.ExecutionTable.item(row_num, 1).text()
                    buy_sell_type_text = self.ExecutionTable.item(row_num, 2).text()
                    if buy_sell_type_text == "매수":
                        buy_sell_type = "1"
                    else:
                        buy_sell_type = "2"
                    amount = self.edit_amount.text()
                    price = self.edit_price.text()
                    if self.combo_order_type.currentText() == "지정가":
                        self.dataseq = self.pySBtrader.doRequestDomModifyOrder(self.daynight, self.acc_no, self.pwd, code, buy_sell_type,  "1", "1", amount, price, ord_num, '')
                    else:
                        self.dataseq = self.pySBtrader.doRequestDomModifyOrder(self.daynight, self.acc_no, self.pwd, code, buy_sell_type,  "2", "1", amount, price, ord_num, '')
                    self.textEdit_table.append("원주문번호: {}가 수량: {}, 가격: {} 으로 정정 주문이 들어 갔습니다.".format(ord_num, amount, price))
                else:
                    self.textEdit_table.append("수량을 입력해주세요.")
            else:
                self.textEdit_table.append("가격을 입력해주세요.")

    def modifyGlobalstock(self):

        row_num = self.ExecutionTable_glb.currentRow()
        if row_num == -1:
            self.textEdit_table_glb.append("정정할 주문을 선택해주세요.")
        else:
            if self.edit_price_glb.text() != "":
                if self.edit_amount_glb.text() != "":
                    stock_name = self.ExecutionTable_glb.item(row_num, 0).text()
                    code = self.global_stock_rel_name_code_dict[stock_name]
                    ord_num = self.ExecutionTable_glb.item(row_num, 1).text()
                    buy_sell_type_text = self.ExecutionTable_glb.item(row_num, 2).text()
                    if buy_sell_type_text == "매수":
                        buy_sell_type = "1"
                    else:
                        buy_sell_type = "2"
                    amount = self.edit_amount_glb.text()
                    price = self.edit_price_glb.text()
                    if self.combo_order_type_glb.currentText() == "지정가":
                        self.dataseq = self.pySBtrader.doRequestGlbModifyOrder(self.acc_no_glb, self.glb_pwd, code, buy_sell_type,  "2", amount, price, '', '0', '', ord_num, '')
                    else:
                        self.dataseq = self.pySBtrader.doRequestGlbModifyOrder(self.acc_no_glb, self.glb_pwd, code, buy_sell_type,  "1", amount, price, '', '0', '', ord_num, '')
                    self.textEdit_table_glb.append("원주문번호: {}가 수량: {}, 가격: {} 으로 정정 주문이 들어 갔습니다.".format(ord_num, amount, price))
                else:
                    self.textEdit_table_glb.append("수량을 입력해주세요.")
            else:
                self.textEdit_table_glb.append("가격을 입력해주세요.")

    def cancelstock(self):

        row_num = self.ExecutionTable.currentRow()
        if row_num == -1:
            self.textEdit_table.append("취소할 주문을 선택해주세요.")
        else:
            stock_name = self.ExecutionTable.item(row_num, 0).text()
            code = self.stock_rel_name_code_dict[stock_name]
            ord_num = self.ExecutionTable.item(row_num, 1).text()
            buy_sell_type_text = self.ExecutionTable.item(row_num, 2).text()
            if buy_sell_type_text == "매수":
                buy_sell_type = "1"
            else:
                buy_sell_type = "2"
            ord_qty = self.ExecutionTable.item(row_num, 4).text()
            self.dataseq = self.pySBtrader.doRequestDomCancelOrder(self.daynight, self.acc_no, self.pwd, code, buy_sell_type, ord_qty, ord_num, '')
            self.textEdit_table.append("{}, {} 주문이 취소되었습니다.".format(code, ord_num))

    def cancelGlobalstock(self):

        row_num = self.ExecutionTable_glb.currentRow()
        if row_num == -1:
            self.textEdit_table_glb.append("취소할 주문을 선택해주세요.")
        else:
            stock_name = self.ExecutionTable_glb.item(row_num, 0).text()
            code = self.global_stock_rel_name_code_dict[stock_name]
            ord_num = self.ExecutionTable_glb.item(row_num, 1).text()
            buy_sell_type_text = self.ExecutionTable_glb.item(row_num, 2).text()
            if buy_sell_type_text == "매수":
                buy_sell_type = "1"
            else:
                buy_sell_type = "2"
            ord_qty = self.ExecutionTable_glb.item(row_num, 4).text()
            self.dataseq = self.pySBtrader.doRequestGlbCancelOrder(self.acc_no_glb, self.glb_pwd, code, buy_sell_type, ord_qty, ord_num, '')
            self.textEdit_table_glb.append("{}, {} 주문이 취소되었습니다.".format(code, ord_num))

    def connectReceiveData(self, nDataSeq: int, trCode: str, errCode: str, recvData: str, userArea: str):
        """
        조회 데이터 응답 이벤트.
            Args:
                nDataSeq`int`: 요청한 전문의 순서
                TrCode`str`: 받은 전문의 TR 코드
                ErrCode`str`: 숫자(5)자리의 에러코드
                RecvData`str`: 응답데이터 - TR별 데이터 (오류일 경우는 에러메시지)
                UserArea`str`: 주문과 같은 경우 사용자 정의 코드를 넣었을 시 반환되는 사용자 정의 값
            Returns:
                Data`json`: 처리후 응답 데이터
        """
        trCode = trCode.upper()
        if str(nDataSeq) == self.dataseq:
            if trCode == 'SGBS3500U03':
                if "정상처리" in recvData:
                    recvData_ = recvData.encode('euc-kr')
                    ord_num = recvData_[8:18].decode('euc-kr')
                    self.textEdit_table_glb.append(str(ord_num) + " 주문이 정상처리 되었습니다.")
                else:
                    self.textEdit_table_glb.append(str(recvData))
            else:
                self.textEdit_table.append(str(recvData))
            self.dataseq = ''

        # 국내 미결제
        if trCode =='SDBS3085Q01':
            self.OpeninterestTable.setRowCount(0)

            recvData_ = recvData.encode('euc-kr')
            cnt = int(recvData_[196:200].decode('euc-kr'))
            data_body = recvData_[200:]
            for i in range(0, cnt):
                idx = i * 458
                data_body_ = data_body[0 + idx : 458 + idx]
                row_num = i

                code = data_body_[62:94].decode('euc-kr').replace(' ', '')
                trd_div_nm = data_body_[145:195].decode('euc-kr').replace(' ', '')
                avg_prc = str(float(data_body_[262:284].decode('euc-kr')))
                rsrb_psb_qtyv = str(float(data_body_[240:262].decode('euc-kr')))
                c = str(float(data_body_[284:306].decode('euc-kr')))
                pft_rt = str(float(data_body_[328:348].decode('euc-kr')))
                stock_name = self.stock_rel_code_name_dict[code]
                ctrt_size = self.stock_rel_code_ctrt_size_dict[code]

                self.OpeninterestTable.insertRow(row_num)
                self.OpeninterestTable.setItem(row_num, 0, QTableWidgetItem(stock_name))

                if trd_div_nm == "매수":
                    color = QColor("red")
                    evl_pnl_amt = str(round(float((float(c) - float(avg_prc)) / float(avg_prc))  * float(rsrb_psb_qtyv) * float(ctrt_size), 1))


                else:
                    color = QColor("blue")
                    evl_pnl_amt = str(round(float((float(avg_prc) - float(c)) / float(avg_prc))  * float(rsrb_psb_qtyv) * float(ctrt_size), 1))

                item = QTableWidgetItem(trd_div_nm)
                item.setForeground(color)
                self.OpeninterestTable.setItem(row_num, 1, item) # 매수, 매도 구분
                self.OpeninterestTable.setItem(row_num, 2, QTableWidgetItem(rsrb_psb_qtyv))
                self.OpeninterestTable.setItem(row_num, 3, QTableWidgetItem(avg_prc))
                self.OpeninterestTable.setItem(row_num, 4, QTableWidgetItem(c))

                if float(evl_pnl_amt) > 0:
                    color = QColor("red")
                elif float(evl_pnl_amt) == 0:
                    color = QColor("black")
                else:
                    color = QColor("blue")

                evl_pnl_amt = '{:,}'.format(float(evl_pnl_amt))
                item = QTableWidgetItem(evl_pnl_amt)
                item.setForeground(color)
                self.OpeninterestTable.setItem(row_num, 5, item)
                item = QTableWidgetItem(pft_rt)
                item.setForeground(color)
                self.OpeninterestTable.setItem(row_num, 6, item)
                self.pySBtrader.doRegistReal('KA', code)

                for row in range(self.OpeninterestTable.rowCount()):
                    for col in range(self.OpeninterestTable.columnCount()):
                        if col != 0:
                            item = self.OpeninterestTable.item(row, col)
                        if item is not None:
                            if col == 1:
                                item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                            else:
                                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                # 국내 OpeninterestTable 우측정렬
                for col in range(self.OpeninterestTable.columnCount()):
                    if col in [4,5,6]: 
                        item = self.OpeninterestTable.item(row_num, col)
                        if item is not None:
                            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter) 

        # 국내 초기 체결, 미체결
        if trCode == 'SDBS3066Q01':
            recvData_ = recvData.encode('euc-kr')
            cnt = int(recvData_[100:104].decode('euc-kr'))
            data_body = recvData_[104:]
            for i in range(0, cnt):
                idx = i * 1325
                data_body_ = data_body[0 + idx : 1325 + idx]

                # 종목명           
                code = data_body_[100:132].decode('euc-kr').replace(' ', '')

                # 국내인지 체크
                if code in self.stock_rel_code_name_dict.keys():                
                    stock_name = self.stock_rel_code_name_dict[code]
                    # 거래구분
                    buy_sell_tp = data_body_[194:195].decode('euc-kr')
                    if buy_sell_tp == "1":
                        buy_sell_tp_text = "매수"
                        color = QColor("red")
                    else:
                        buy_sell_tp_text = "매도"
                        color = QColor("blue")              

                    # 상태
                    ord_sts_tp = str(data_body_[245:246].decode('euc-kr'))
                    if ord_sts_tp == "3":
                        ord_sts_tp_text = "미체결"
                    elif ord_sts_tp == "1":
                        ord_sts_tp_text = "미체결"
                    elif ord_sts_tp == "2":
                        ord_sts_tp_text = "미체결"
                    elif ord_sts_tp == "4":
                        ord_sts_tp_text = "일부체결"
                    elif ord_sts_tp == "6":
                        ord_sts_tp_text = "체결"
                    else:
                        ord_sts_tp_text = "Unknown Status"

                    # 주문번호
                    ord_no = str(data_body_[90:100].decode('euc-kr'))

                    # 주문량
                    ord_qty = str(float(data_body_[296:320].decode('euc-kr')))

                    # 체결량
                    exec_qtyv = str(float(data_body_[344:368].decode('euc-kr')))

                    # 잔량
                    ord_rmqy_qtyv = str(float(ord_qty) - float(exec_qtyv))

                    # 주문가
                    ord_prc = str(float(data_body_[320:344].decode('euc-kr')))

                    # 체결가
                    exec_prc = str(float(data_body_[368:392].decode('euc-kr')))

                    # 체결, 미체결 정보창
                    flag = 1
                    for row_num in range(self.ExecutionTable.rowCount()):

                        existed_ord_no = self.ExecutionTable.item(row_num, 1).text()                    

                        if existed_ord_no == ord_no:

                            self.ExecutionTable.setItem(row_num, 0, QTableWidgetItem(stock_name))
                            self.ExecutionTable.setItem(row_num, 1, QTableWidgetItem(ord_no))
                            item = QTableWidgetItem(buy_sell_tp_text)
                            item.setForeground(color)
                            self.ExecutionTable.setItem(row_num, 2, item)
                            self.ExecutionTable.setItem(row_num, 3, QTableWidgetItem(ord_sts_tp_text))
                            self.ExecutionTable.setItem(row_num, 4, QTableWidgetItem(ord_qty))
                            self.ExecutionTable.setItem(row_num, 5, QTableWidgetItem(exec_qtyv))
                            self.ExecutionTable.setItem(row_num, 6, QTableWidgetItem(ord_rmqy_qtyv))
                            self.ExecutionTable.setItem(row_num, 7, QTableWidgetItem(ord_prc))
                            self.ExecutionTable.setItem(row_num, 8, QTableWidgetItem(exec_prc))
                            flag = 0

                    # 없다면 새로 생성
                    if flag == 1:
                        row_num = self.ExecutionTable.rowCount()
                        self.ExecutionTable.insertRow(row_num)
                        self.ExecutionTable.setItem(row_num, 0, QTableWidgetItem(stock_name))
                        self.ExecutionTable.setItem(row_num, 1, QTableWidgetItem(ord_no))
                        item = QTableWidgetItem(buy_sell_tp_text)
                        item.setForeground(color)
                        self.ExecutionTable.setItem(row_num, 2, item)
                        self.ExecutionTable.setItem(row_num, 3, QTableWidgetItem(ord_sts_tp_text))
                        self.ExecutionTable.setItem(row_num, 4, QTableWidgetItem(ord_qty))
                        self.ExecutionTable.setItem(row_num, 5, QTableWidgetItem(exec_qtyv))
                        self.ExecutionTable.setItem(row_num, 6, QTableWidgetItem(ord_rmqy_qtyv))
                        self.ExecutionTable.setItem(row_num, 7, QTableWidgetItem(ord_prc))
                        self.ExecutionTable.setItem(row_num, 8, QTableWidgetItem(exec_prc))

                    # 국내 ExecutionTable 우측정렬
                    for row in range(self.ExecutionTable.rowCount()):
                        for col in range(self.ExecutionTable.columnCount()):
                            if col != 0:
                                item = self.ExecutionTable.item(row, col)
                            if item is not None:
                                if col == 2 or col == 3:
                                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                                else:
                                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # 해외 초기 체결, 미체결
        if trCode == 'SGBS9001Q01':

            recvData_ = recvData.encode('euc-kr')
            cnt = int(recvData_[100:104].decode('euc-kr'))
            data_body = recvData_[104:]
            for i in range(0, cnt):
                idx = i * 951
                data_body_ = data_body[0 + idx : 951 + idx]

                code = data_body_[52:84].decode('euc-kr').replace(" ", "")
                stock_name = self.global_stock_rel_code_name_dict[code]
                buy_sell_tp = data_body_[85:86].decode('euc-kr') # 거래구분
                if buy_sell_tp == "1":
                    buy_sell_tp_text = "매수"
                    color = QColor("red")
                else:
                    buy_sell_tp_text = "매도"
                    color = QColor("blue")

                # 상태
                mnp_tp = str(data_body_[86:87].decode('euc-kr'))
                ord_sts_tp = str(data_body_[84:85].decode('euc-kr'))
                if mnp_tp == "1":
                    if ord_sts_tp == "2":
                        ord_sts_tp_text = "접수"
                    elif ord_sts_tp == "1":
                        ord_sts_tp_text = "접수"
                    elif ord_sts_tp == "3":
                        ord_sts_tp_text = "미체결"
                    elif ord_sts_tp == "4":
                        ord_sts_tp_text = "미체결"
                    elif ord_sts_tp == "5":
                        ord_sts_tp_text = "정정"
                    elif ord_sts_tp == "6":
                        ord_sts_tp_text = "체결"
                    elif ord_sts_tp == "9":
                        ord_sts_tp_text = "거부"
                elif mnp_tp == "2":
                    if ord_sts_tp == "2":
                        ord_sts_tp_text = "접수"
                    elif ord_sts_tp == "1":
                        ord_sts_tp_text = "접수"
                    elif ord_sts_tp == "3":
                        ord_sts_tp_text = "미체결"
                    elif ord_sts_tp == "4":
                        ord_sts_tp_text = "미체결"
                    elif ord_sts_tp == "5":
                        ord_sts_tp_text = "정정"
                    elif ord_sts_tp == "6":
                        ord_sts_tp_text = "체결"
                    elif ord_sts_tp == "9":
                        ord_sts_tp_text = "거부"
                elif mnp_tp == "3":
                    ord_sts_tp_text = "취소"

                # 주문번호
                ord_no = str(data_body_[23:33].decode('euc-kr'))

                # 주문량
                ord_qty = str(float( data_body_[89:96].decode('euc-kr')))

                # 체결량
                exec_qtyv = str(float(data_body_[96:103].decode('euc-kr')))

                # 잔량
                ord_rmqy_qtyv = str(float(ord_qty) - float(exec_qtyv))

                # 주문가
                ord_prc = str(float(data_body_[117:132].decode('euc-kr')))

                # 체결가
                try:
                    exec_prc = str(float(data_body_[132:147].decode('euc-kr')))
                except:
                    exec_prc = str('')

                # 체결, 미체결 정보창
                flag = 1
                for row_num in range(self.ExecutionTable_glb.rowCount()):

                    existed_ord_no = self.ExecutionTable_glb.item(row_num, 1).text()

                    if existed_ord_no == ord_no:

                        self.ExecutionTable_glb.setItem(row_num, 0, QTableWidgetItem(stock_name))
                        self.ExecutionTable_glb.setItem(row_num, 1, QTableWidgetItem(ord_no))
                        item = QTableWidgetItem(buy_sell_tp_text)
                        item.setForeground(color)
                        self.ExecutionTable_glb.setItem(row_num, 2, item)
                        self.ExecutionTable_glb.setItem(row_num, 3, QTableWidgetItem(ord_sts_tp_text))
                        self.ExecutionTable_glb.setItem(row_num, 4, QTableWidgetItem(ord_qty))
                        self.ExecutionTable_glb.setItem(row_num, 5, QTableWidgetItem(exec_qtyv))
                        self.ExecutionTable_glb.setItem(row_num, 6, QTableWidgetItem(ord_rmqy_qtyv))
                        self.ExecutionTable_glb.setItem(row_num, 7, QTableWidgetItem(ord_prc))
                        self.ExecutionTable_glb.setItem(row_num, 8, QTableWidgetItem(exec_prc))
                        flag = 0

                # 없다면 새로 생성
                if flag == 1:
                    row_num = self.ExecutionTable_glb.rowCount()
                    self.ExecutionTable_glb.insertRow(row_num)
                    self.ExecutionTable_glb.setItem(row_num, 0, QTableWidgetItem(stock_name))
                    self.ExecutionTable_glb.setItem(row_num, 1, QTableWidgetItem(ord_no))
                    item = QTableWidgetItem(buy_sell_tp_text)
                    item.setForeground(color)
                    self.ExecutionTable_glb.setItem(row_num, 2, item)
                    self.ExecutionTable_glb.setItem(row_num, 3, QTableWidgetItem(ord_sts_tp_text))
                    self.ExecutionTable_glb.setItem(row_num, 4, QTableWidgetItem(ord_qty))
                    self.ExecutionTable_glb.setItem(row_num, 5, QTableWidgetItem(exec_qtyv))
                    self.ExecutionTable_glb.setItem(row_num, 6, QTableWidgetItem(ord_rmqy_qtyv))
                    self.ExecutionTable_glb.setItem(row_num, 7, QTableWidgetItem(ord_prc))
                    self.ExecutionTable_glb.setItem(row_num, 8, QTableWidgetItem(exec_prc))

                # 해외 ExecutionTable 우측정렬
                for row in range(self.ExecutionTable_glb.rowCount()):
                    for col in range(self.ExecutionTable_glb.columnCount()):
                        if col != 0:
                            item = self.ExecutionTable_glb.item(row, col)
                        if item is not None:
                            if col == 2 or col == 3:
                                item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                            else:
                                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # 해외 미결제
        if trCode == 'SGBS9001Q03':
            self.OpeninterestTable_glb.setRowCount(0)
            recvData_ = recvData.encode('euc-kr')
            cnt = int(recvData_[100:104].decode('euc-kr'))
            data_body = recvData_[104:]
            for i in range(0, cnt):
                idx = i * 480
                data_body_ = data_body[0 + idx : 480 + idx]
                row_num = i

                code = data_body_[34:66].decode('euc-kr').replace(' ', '')
                self.pySBtrader.doRegistReal('FA', code)
                trd_div_nm = data_body_[66:67].decode('euc-kr')
                if trd_div_nm == '1':
                    trd_div_nm = '매수'
                else:
                    trd_div_nm = '매도'
                avg_prc = str(float(data_body_[137:152].decode('euc-kr').replace(' ', ''))) # 평균단가
                rsrb_psb_qtyv = str(float(data_body_[97:107].decode('euc-kr').replace(' ', ''))) # 수량
                c = str(float(data_body_[310:325].decode('euc-kr'))) # 현재가
                # 수익률
                if trd_div_nm == '매수':
                    pft_rt = str(round((float(c) - float(avg_prc)) / float(avg_prc) * 100, 2))
                else:
                    pft_rt = str(round((float(avg_prc) - float(c)) / float(avg_prc) * 100, 2))

                stock_name = self.global_stock_rel_code_name_dict[code] # 종목이름
                ctrt_size = self.global_stock_rel_code_ctrt_size_dict[code] # 거래승수

                self.OpeninterestTable_glb.insertRow(row_num)
                self.OpeninterestTable_glb.setItem(row_num, 0, QTableWidgetItem(stock_name))

                if trd_div_nm == "매수":
                    color = QColor("red")
                    evl_pnl_amt = str(round(float((float(c) - float(avg_prc)) / float(avg_prc))  * float(rsrb_psb_qtyv) * float(ctrt_size), 3))

                else:
                    color = QColor("blue")
                    evl_pnl_amt = str(round(float((float(avg_prc) - float(c)) / float(avg_prc))  * float(rsrb_psb_qtyv) * float(ctrt_size), 3))
                item = QTableWidgetItem(trd_div_nm)
                item.setForeground(color)
                self.OpeninterestTable_glb.setItem(row_num, 1, item) # 매수, 매도 구분

                self.OpeninterestTable_glb.setItem(row_num, 2, QTableWidgetItem(rsrb_psb_qtyv))
                self.OpeninterestTable_glb.setItem(row_num, 3, QTableWidgetItem(avg_prc))
                self.OpeninterestTable_glb.setItem(row_num, 4, QTableWidgetItem(c))

                if float(evl_pnl_amt) > 0:
                    color = QColor("red")
                elif float(evl_pnl_amt) == 0:
                    color = QColor("black")
                else:
                    color = QColor("blue")
                evl_pnl_amt = '{:,}'.format(float(evl_pnl_amt))
                item = QTableWidgetItem(evl_pnl_amt)
                item.setForeground(color)
                self.OpeninterestTable_glb.setItem(row_num, 5, item)
                item = QTableWidgetItem(pft_rt)
                item.setForeground(color)
                self.OpeninterestTable_glb.setItem(row_num, 6, item)

                for row in range(self.OpeninterestTable_glb.rowCount()):
                    for col in range(self.OpeninterestTable_glb.columnCount()):
                        if col != 0:
                            item = self.OpeninterestTable_glb.item(row, col)
                        if item is not None:
                            if col == 1:
                                item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                            else:
                                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                # 국내 OpeninterestTable 우측정렬
                for col in range(self.OpeninterestTable_glb.columnCount()):
                    if col in [4,5,6]: 
                        item = self.OpeninterestTable_glb.item(row_num, col)
                        if item is not None:
                            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter) 

        # 국내 예탁자산 조회
        if trCode == 'SDBS5001Q01':         

            # 예탁금액
            if "처리" in recvData:
                self.textEdit_table.append(str(recvData))
                self.button_connect_acc.setEnabled(True)
                self.sched.remove_job('updateAccountInfo')
            else:
                dpg_aset_tot_amt = float(recvData[88:110])# 예탁자산총금액
                dpg_sbst_amt = float(recvData[132:154]) # 예탁대용금액
                dpg_fcur_amt = float(recvData[154:176]) # 예탁외화금액
                dpg_csh_amt = float(recvData[110:132]) # 예탁현금금액

                # 주문가능 금액
                ord_psb_tot_amt = float(recvData[176:198]) # 주문가능총금액
                ord_psb_csh_amt = float(recvData[198:220]) # 주문가능현금금액
                ord_psb_sbst_amt = float(recvData[220:242]) # 주문가능대용금액
                ord_psb_fcur_amt = float(recvData[242:264]) # 주문가능외화금액          

                # 인출가능 금액
                wdw_psb_tot_amt = float(recvData[264:286]) # 인출가능총금액
                wdw_psb_csh_amt = float(recvData[286:308]) # 인출가능현금금액
                wdw_psb_sbst_amt = float(recvData[308:330]) # 인출가능대용금액
                wdw_psb_fcur_amt = float(recvData[330:352]) # 인출가능외화금액          

                # 위탁증거금 금액
                brkg_mrgn_tam_amt = float(recvData[352:374]) # 위탁증거금총액금액
                brkg_mrgn_csh_amt = float(recvData[374:396]) # 위탁증거금현금금액
                brkg_mrgn_sbst_amt = float(recvData[396:418]) # 위탁증거금대용금액
                brkg_mrgn_fcur_amt = float(recvData[418:440]) # 위탁증거금외화금액

                # 유치증거금 금액
                mtn_mrgn_tam_amt = float(recvData[440:462]) # 유지증거금총액금액
                mtn_mrgn_csh_amt = float(recvData[462:484]) # 유지증거금현금금액
                mtn_mrgn_sbst_amt = float(recvData[484:506]) # 유지증거금대용금액
                mtn_mrgn_fcur_amt = float(recvData[506:528]) # 유지증거금외화금액

                # 추가증거금 금액
                adt_mrgn_tot_amt = float(recvData[528:550]) # 추가증거금총금액
                adt_mrgn_csh_amt = float(recvData[550:572]) # 추가증거금현금금액
                adt_mrgn_sbst_amt = float(recvData[572:594]) # 추가증거금대용금액
                adt_mrgn_fcur_amt = float(recvData[594:616]) # 추가증거금외화금액

                # 확정 손익금액
                fts_dfn_pnl_amt = float(recvData[754:776]) # 선물확정손익금액
                opt_dfn_pnl_amt = float(recvData[776:798]) # 옵션확정손익금액

                # 가결제/익일결제 금액
                fts_adj_deb_amt = float(recvData[1040:1062])   # 선물정산차금금액
                opt_stl_pmny_amt = float(recvData[1062:1084])   # 옵션결제대금금액
                rlth_delv_stl_pla_amt = float(recvData[1128:1150])   # 실물인수도결제예정금액
                fee = float(recvData[1150:1172])   # 수수료

                # 신규 매수 종목을 계좌 테이블에 추가.
                # 예탁금액
                # PyQt5를 사용하는 경우
                self.AccountInfoTable.setItem(0, 0, QTableWidgetItem(str(dpg_aset_tot_amt)))
                self.AccountInfoTable.setItem(0, 1, QTableWidgetItem(str(dpg_csh_amt)))
                self.AccountInfoTable.setItem(0, 2, QTableWidgetItem(str(dpg_sbst_amt)))
                self.AccountInfoTable.setItem(0, 3, QTableWidgetItem(str(dpg_fcur_amt)))
                # 주문가능 금액
                self.AccountInfoTable.setItem(1, 0, QTableWidgetItem(str(ord_psb_tot_amt)))
                self.AccountInfoTable.setItem(1, 1, QTableWidgetItem(str(ord_psb_csh_amt)))
                self.AccountInfoTable.setItem(1, 2, QTableWidgetItem(str(ord_psb_sbst_amt)))
                self.AccountInfoTable.setItem(1, 3, QTableWidgetItem(str(ord_psb_fcur_amt)))
                # 인출가능 금액
                self.AccountInfoTable.setItem(2, 0, QTableWidgetItem(str(wdw_psb_tot_amt)))
                self.AccountInfoTable.setItem(2, 1, QTableWidgetItem(str(wdw_psb_csh_amt)))
                self.AccountInfoTable.setItem(2, 2, QTableWidgetItem(str(wdw_psb_sbst_amt)))
                self.AccountInfoTable.setItem(2, 3, QTableWidgetItem(str(wdw_psb_fcur_amt)))
                # 위탁증거금 금액
                self.AccountInfoTable.setItem(3, 0, QTableWidgetItem(str(brkg_mrgn_tam_amt)))
                self.AccountInfoTable.setItem(3, 1, QTableWidgetItem(str(brkg_mrgn_csh_amt)))
                self.AccountInfoTable.setItem(3, 2, QTableWidgetItem(str(brkg_mrgn_sbst_amt)))
                self.AccountInfoTable.setItem(3, 3, QTableWidgetItem(str(brkg_mrgn_fcur_amt)))
                # 유치증거금 금액
                self.AccountInfoTable.setItem(4, 0, QTableWidgetItem(str(mtn_mrgn_tam_amt)))
                self.AccountInfoTable.setItem(4, 1, QTableWidgetItem(str(mtn_mrgn_csh_amt)))
                self.AccountInfoTable.setItem(4, 2, QTableWidgetItem(str(mtn_mrgn_sbst_amt)))
                self.AccountInfoTable.setItem(4, 3, QTableWidgetItem(str(mtn_mrgn_fcur_amt)))
                # 추가증거금 금액
                self.AccountInfoTable.setItem(5, 0, QTableWidgetItem(str(adt_mrgn_tot_amt)))
                self.AccountInfoTable.setItem(5, 1, QTableWidgetItem(str(adt_mrgn_csh_amt)))
                self.AccountInfoTable.setItem(5, 2, QTableWidgetItem(str(adt_mrgn_sbst_amt)))
                self.AccountInfoTable.setItem(5, 3, QTableWidgetItem(str(adt_mrgn_fcur_amt)))
                # 확정 손익금액
                self.AccountInfoTable.setItem(6, 1, QTableWidgetItem(str(fts_dfn_pnl_amt)))
                self.AccountInfoTable.setItem(6, 3, QTableWidgetItem(str(opt_dfn_pnl_amt)))
                # 가결제/익일결제 금액
                self.AccountInfoTable.setItem(7, 1, QTableWidgetItem(str(fts_adj_deb_amt)))
                self.AccountInfoTable.setItem(7, 3, QTableWidgetItem(str(opt_stl_pmny_amt)))
                self.AccountInfoTable.setItem(8, 1, QTableWidgetItem(str(rlth_delv_stl_pla_amt)))
                self.AccountInfoTable.setItem(8, 3, QTableWidgetItem(str(fee)))
                # 데이터 우측정렬
                for row in range(self.AccountInfoTable.rowCount()):
                    for col in range(self.AccountInfoTable.columnCount()):
                        item = self.AccountInfoTable.item(row, col)
                        if item is not None:
                            if not item.text().isalpha(): 
                                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # 해외 예탁자산 조회
        if trCode == 'SGBS3205Q01':         

            # 예탁금액
            if "처리" in recvData:
                self.textEdit_table_glb.append(str(recvData))
                self.button_connect_acc_glb.setEnabled(True)
                self.sched.remove_job('updateGlobalAccountInfo')
            else:
                recvData_ = recvData.encode('euc-kr')
                dpg_csh_amt = float(recvData_[191:215].decode('euc-kr'))   # 예탁현금금액 (Current day entrusted assets)
                rsrb_pnl_amt = float(recvData_[455:479].decode('euc-kr'))   # 청산손익금액 (Realized profit and loss)
                opt_trd_amt = float(recvData_[527:551].decode('euc-kr'))   # 옵션매매금액 (Option trading amount)
                brkg_fee = float(recvData_[623:647].decode('euc-kr'))   # 위탁수수료 (Brokerage fee)
                fts_nstl_evl_pnl_amt = float(recvData_[791:815].decode('euc-kr'))   # 선물미결제평가손익금액 (Futures evaluation profit and loss)
                dpg_aset_evl_amt = float(recvData_[839:863].decode('euc-kr'))   # 예탁자산평가금액 (Deposit asset evaluation amount)
                opt_buy_mkt_wth_amt = float(recvData_[887:911].decode('euc-kr'))   # 옵션매수시장가치금액 (Option market value of purchased options)
                opt_sell_mkt_wth_amt = float(recvData_[911:935].decode('euc-kr'))   # 옵션매도시장가치금액 (Option market value of sold options)
                fts_tp_opt_nstl_evl_pnl_amt = float(recvData_[815:839].decode('euc-kr'))   # 선물형옵션미결제평가손익금액 (Futures and options market value)
                tot_acc_aset_wth_amt = float(recvData_[935:959].decode('euc-kr'))   # 총계정자산가치금액 (Total account asset value)

                brkg_mrgn = float(recvData_[1055:1079].decode('euc-kr'))   # 위탁증거금 (Margin deposit)
                mtn_mrgn = float(recvData_[1175:1199].decode('euc-kr'))   # 유지증거금 (Maintenance margin)
                adt_mrgn = float(recvData_[1031:1055].decode('euc-kr'))   # 추가증거금 (Previous day margin call amount)
                urv_amt = float(recvData_[599:623].decode('euc-kr'))   # 미수금액 (Outstanding receivables)
                rnd_amt = float(recvData_[239:263].decode('euc-kr'))   # 입출금액 (Deposit and withdrawal amount)
                nxd_dpg_csh_amt = float(recvData_[743:767].decode('euc-kr'))   # 익일예탁현금금액 (Next day entrusted assets)
                ord_psb_amt = float(recvData_[1199:1223].decode('euc-kr'))   # 주문가능금액 (Orderable amount)
                wdw_psb_amt = float(recvData_[1223:1247].decode('euc-kr'))   # 인출가능금액 (Withdrawable amount)
                dpg_sbst_amt = float(recvData_[143:167].decode('euc-kr'))   # 예탁대용금액 (Collateral amount)
                mgg_incd_tot_acc_aset_wth_amt = float(recvData_[959:983].decode('euc-kr'))   # 담보포함총계정자산가치금액 (Total account asset value including collateral)

                # 신규 매수 종목을 계좌 테이블에 추가.
                self.AccountInfoTable_glb.setItem(0, 1, QTableWidgetItem(str(dpg_csh_amt)))
                self.AccountInfoTable_glb.setItem(1, 1, QTableWidgetItem(str(rsrb_pnl_amt)))
                self.AccountInfoTable_glb.setItem(2, 1, QTableWidgetItem(str(opt_trd_amt)))
                self.AccountInfoTable_glb.setItem(3, 1, QTableWidgetItem(str(brkg_fee)))
                self.AccountInfoTable_glb.setItem(4, 1, QTableWidgetItem(str(fts_nstl_evl_pnl_amt)))
                self.AccountInfoTable_glb.setItem(5, 1, QTableWidgetItem(str(dpg_aset_evl_amt)))
                self.AccountInfoTable_glb.setItem(6, 1, QTableWidgetItem(str(opt_buy_mkt_wth_amt)))
                self.AccountInfoTable_glb.setItem(7, 1, QTableWidgetItem(str(opt_sell_mkt_wth_amt)))
                self.AccountInfoTable_glb.setItem(8, 1, QTableWidgetItem(str(fts_tp_opt_nstl_evl_pnl_amt)))
                self.AccountInfoTable_glb.setItem(9, 1, QTableWidgetItem(str(tot_acc_aset_wth_amt)))

                self.AccountInfoTable_glb.setItem(0, 3, QTableWidgetItem(str(brkg_mrgn)))
                self.AccountInfoTable_glb.setItem(1, 3, QTableWidgetItem(str(mtn_mrgn)))
                self.AccountInfoTable_glb.setItem(2, 3, QTableWidgetItem(str(adt_mrgn)))
                self.AccountInfoTable_glb.setItem(3, 3, QTableWidgetItem(str(urv_amt)))
                self.AccountInfoTable_glb.setItem(4, 3, QTableWidgetItem(str(rnd_amt)))
                self.AccountInfoTable_glb.setItem(5, 3, QTableWidgetItem(str(nxd_dpg_csh_amt)))
                self.AccountInfoTable_glb.setItem(6, 3, QTableWidgetItem(str(ord_psb_amt)))
                self.AccountInfoTable_glb.setItem(7, 3, QTableWidgetItem(str(wdw_psb_amt)))
                self.AccountInfoTable_glb.setItem(8, 3, QTableWidgetItem(str(dpg_sbst_amt)))
                self.AccountInfoTable_glb.setItem(9, 3, QTableWidgetItem(str(mgg_incd_tot_acc_aset_wth_amt)))
                # 데이터 우측정렬
                for row in range(self.AccountInfoTable_glb.rowCount()):
                    for col in range(self.AccountInfoTable_glb.columnCount()):
                        item = self.AccountInfoTable_glb.item(row, col)
                        if item is not None:
                            if not item.text().isalpha():
                                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)


    def getAllStockList(self):

        stock_list = []
        stock_code_list = []
        self.stock_rel_code_name_dict = {}
        self.stock_rel_name_code_dict = {}
        self.stock_rel_code_relcode_dict = {}
        self.stock_rel_code_ctrt_size_dict = {}

        self.combo_stockcode.clear()
        self.combo_stockname.clear()

        # 국내 종목들 정보 파일 열기
        with open(self.NH_filespace + '\\sfile03.dat', 'r', encoding='euc-kr') as f:
            lines = f.read().split('\n')[:-1]
            for line in lines:
                data = line.replace('\'', '').split(',')
                name = data[10]
                code = data[8]
                daynight = data[5]
                relcode = data[23]
                ctrt_size = data[17]

                if self.daynight == '1' and daynight == 'day':
                    stock_list.append(name)
                    stock_code_list.append(code + " (" + name + ")")
                    self.stock_rel_code_name_dict[code] = name
                    self.stock_rel_name_code_dict[name] = code
                    self.stock_rel_code_relcode_dict[code] = relcode
                    self.stock_rel_code_ctrt_size_dict[code] = ctrt_size

                elif self.daynight == '2' and daynight == 'night':
                    stock_list.append(name)
                    stock_code_list.append(code + " (" + name + ")")
                    self.stock_rel_code_name_dict[code] = name
                    self.stock_rel_name_code_dict[name] = code
                    self.stock_rel_code_relcode_dict[code] = relcode
                    self.stock_rel_code_ctrt_size_dict[code] = ctrt_size

        self.combo_stockcode.addItems(['', *stock_code_list])
        self.combo_stockname.addItems(['', *stock_list])

        return stock_code_list, stock_list

    def getAllGlobalStockList(self):

        global_stock_list = []
        global_stock_code_list = []
        self.global_stock_rel_name_code_dict = {}
        self.global_stock_rel_code_relcode_dict = {}
        self.global_stock_rel_code_name_dict = {}
        self.global_stock_rel_code_exchange_dict = {}
        self.global_stock_rel_code_ctrt_size_dict = {}
        self.combo_stockcode_glb.clear()
        self.combo_stockname_glb.clear()

        # 해외 종목들 정보 파일 열기
        with open(self.NH_filespace + '\\fucode.dat', 'r', encoding='euc-kr') as f:
            lines = f.read().split('\n')[1:-1]
            for line in lines:
                data = line.replace('\'', '').split(',')
                name = data[4]
                code = data[1]              
                relcode = data[1]
                exchange = data[2]
                TickSize = data[11]
                AdjustValue = data[12]
                TickValue = data[18]

                global_stock_list.append(name)
                global_stock_code_list.append(code + " (" + name + ")")
                # 국내와의 차이점은 거래소가 추가되었다.
                self.global_stock_rel_code_name_dict[code] = name
                self.global_stock_rel_name_code_dict[name] = code
                self.global_stock_rel_code_relcode_dict[code] = relcode
                self.global_stock_rel_code_exchange_dict[code] = exchange
                ctrt_size = float(TickValue) * float(AdjustValue) / float(TickSize)
                self.global_stock_rel_code_ctrt_size_dict[code] = ctrt_size


        self.combo_stockname_glb.addItems(['', *global_stock_list])
        self.combo_stockcode_glb.addItems(['', *global_stock_code_list])

        return global_stock_code_list, global_stock_list

    def addStock(self):

        """국내 호가창 테이블에 종목 추가"""

        if self.combo_searchtype.currentText() == "종목명":
            name = self.combo_stockname.currentText()
            code = self.stock_rel_name_code_dict[name]
        else:
            code = self.combo_stockname.currentText()
            name = self.stock_rel_code_name_dict[code]

        if code not in self.datatable_stock_list:
            self.datatable_stock_list.append(code)
            row_num = self.dataTable.rowCount()
            self.dataTable.insertRow(row_num)
            self.dataTable.setItem(row_num, 0, QTableWidgetItem(name))          
            self.pySBtrader.doRegistReal("KA", code)
            self.textEdit_table.append("{} 가(이) 추가되었습니다.".format(name))

    def connectHoga(self):

        row_num = self.dataTable.currentRow()
        name = self.dataTable.item(row_num, 0).text()
        code = self.stock_rel_name_code_dict[name]
        if code != self.current_hoga_stock_code:
            self.textEdit_table.append("{} 가(이) 선택되었습니다.".format(name))
            self.pySBtrader.doUnRegistReal('KB', self.current_hoga_stock_code)
            self.current_hoga_stock_code = code
            self.pySBtrader.doRegistReal('KB', self.current_hoga_stock_code)

    def connectGlobalHoga(self):

        row_num = self.dataTable_glb.currentRow()
        name = self.dataTable_glb.item(row_num, 0).text()
        code = self.global_stock_rel_name_code_dict[name]
        if code != self.global_current_hoga_stock_code:
            self.textEdit_table_glb.append("{} 가(이) 선택되었습니다.".format(name))
            self.pySBtrader.doUnRegistReal('FB', self.global_current_hoga_stock_code)
            self.global_current_hoga_stock_code = code
            self.pySBtrader.doRegistReal('FB', self.global_current_hoga_stock_code)

    def addGlobalStock(self):

        """해외 호가창 테이블에 종목 추가"""

        if self.combo_searchtype_glb.currentText() == "종목명":
            name = self.combo_stockname_glb.currentText()
            code = self.global_stock_rel_name_code_dict[name]
        else:
            code = self.combo_stockname_glb.currentText()
            name = self.global_stock_rel_code_name_dict[code]

        if code not in self.global_datatable_stock_list:
            self.global_datatable_stock_list.append(code)
            row_num = self.dataTable_glb.rowCount()
            self.dataTable_glb.insertRow(row_num)
            self.dataTable_glb.setItem(row_num, 0, QTableWidgetItem(name))          
            self.pySBtrader.doRegistReal("FA", code)
            self.textEdit_table_glb.append("{} 가(이) 추가되었습니다.".format(name))

    def deleteStock(self):

        """국내 종목리스트 하나씩 삭제"""

        row_num = self.dataTable.currentRow()

        if row_num == -1:
            self.showPopupWindow("삭제할 종목을 선택하세요.")
        else:   
            name = self.dataTable.item(row_num, 0).text()
            code = self.stock_rel_name_code_dict[name]
            self.dataTable.removeRow(row_num)
            self.datatable_stock_list.remove(code)
            self.pySBtrader.doUnRegistReal("KA", code)
            self.dataTable.setCurrentCell(-1, -1)
            self.textEdit_table.append("{} 가(이) 삭제되었습니다.".format(name))

    def deleteGlobalStock(self):

        """해외 종목리스트 하나씩 삭제"""

        row_num = self.dataTable_glb.currentRow()

        if row_num == -1:
            self.showPopupWindow("삭제할 종목을 선택하세요.")
        else:   
            name = self.dataTable_glb.item(row_num, 0).text()
            code = self.global_stock_rel_name_code_dict[name]
            self.dataTable_glb.removeRow(row_num)
            self.global_datatable_stock_list.remove(code)
            self.pySBtrader.doUnRegistReal("FA", code)
            self.dataTable_glb.setCurrentCell(-1, -1)
            self.textEdit_table_glb.append("{} 가(이) 삭제되었습니다.".format(name))


    def deleteStockAll(self):

        """국내 종목리스트 전체 삭제"""

        rowCount = self.dataTable.rowCount()

        for row_num in range(rowCount-1, -1, -1):
            name = self.dataTable.item(row_num, 0).text()
            code = self.stock_rel_name_code_dict[name]
            self.dataTable.removeRow(row_num)
            self.datatable_stock_list.remove(code)
            self.pySBtrader.doUnRegistReal("KA", code)

        self.textEdit_table.append("종목이 모두 삭제되었습니다.")

    def deleteGlobalStockAll(self):

        """해외 종목리스트 전체 삭제"""

        rowCount = self.dataTable_glb.rowCount()

        for row_num in range(rowCount-1, -1, -1):
            name = self.dataTable_glb.item(row_num, 0).text()
            code = self.global_stock_rel_name_code_dict[name]
            self.dataTable_glb.removeRow(row_num)
            self.global_datatable_stock_list.remove(code)
            self.pySBtrader.doUnRegistReal("FA", code)

        self.textEdit_table_glb.append("종목이 모두 삭제되었습니다.")

    def connectReceiveReal(self, realCode: str, realKey: str, recvData: str, UserArea):
        """
        국내 실시간 데이터 응답
            Args:
                RealCode`str`: 실시간 업데이트 전문의 TR 코드
                RealKey`str`: 실시간 전문 요청시 넣었던 키값
                RecvData`str`: 응답데이터 - TR별 데이터
            Returns:
                Data`json`: 처리후 실시간 데이터
        """

        # 실시간 국내
        if realCode in ['KA']:
            o = recvData[22:31]
            h = recvData[32:41]
            l = recvData[42:51]
            c = recvData[52:61]
            rate = recvData[73:79]
            tvol = recvData[87:99]
            code = recvData[2:14].replace(" ", "")

            # 데이터 테이블 값들 실시간 업데이트 
            if code in self.datatable_stock_list:
                row_num = self.datatable_stock_list.index(code)
                self.dataTable.setItem(row_num, 1, QTableWidgetItem(c.rstrip()))
                self.dataTable.setItem(row_num, 2, QTableWidgetItem(o))
                self.dataTable.setItem(row_num, 3, QTableWidgetItem(h))
                self.dataTable.setItem(row_num, 4, QTableWidgetItem(l))
                self.dataTable.setItem(row_num, 5, QTableWidgetItem(tvol.rstrip()))

                # 등락률 color setting
                if float(rate) > 0:
                    color = QColor("red")
                elif float(rate) < 0:
                    color = QColor("blue")
                else:
                    color = QColor("black")

                item = QTableWidgetItem(rate.rstrip())
                item.setForeground(color)
                self.dataTable.setItem(row_num, 6, item)

                # 국내 datatable 우측정렬
                for row in range(self.dataTable.rowCount()):
                    for col in range(self.dataTable.columnCount()):
                        if col != 0:
                            item = self.dataTable.item(row, col)
                            if item is not None:
                                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            # 미결제 약정 테이블 업데이트
            for row_num in range(self.OpeninterestTable.rowCount()):

                stock_name = self.OpeninterestTable.item(row_num, 0).text()
                stock_type = self.OpeninterestTable.item(row_num, 1).text()
                qty = self.OpeninterestTable.item(row_num, 2).text()
                prc = self.OpeninterestTable.item(row_num, 3).text()

                if self.stock_rel_name_code_dict[stock_name] == code:
                    ctrt_size = self.stock_rel_code_ctrt_size_dict[code] 
                    self.OpeninterestTable.setItem(row_num, 4, QTableWidgetItem(c))
                    if stock_type == "매수":
                        profit = round(float((float(c)-float(prc)) * float(qty) * float(ctrt_size)) , 1)
                        perc = round(float((float(c)-float(prc)) / float(prc)) * 100, 2)

                        # 국내 평가손익,수익률 color setting
                        if float(profit) > 0:
                            color = QColor("red")
                        elif float(profit) < 0:
                            color = QColor("blue")
                        else:
                            color = QColor("black")
                        profit = '{:,}'.format(profit)
                        item = QTableWidgetItem(profit)
                        item.setForeground(color)
                        self.OpeninterestTable.setItem(row_num, 5, item)

                        if float(perc) > 0:
                            color = QColor("red")
                        elif float(perc) < 0:
                            color = QColor("blue")
                        else:
                            color = QColor("black")
                        item = QTableWidgetItem(str(perc))
                        item.setForeground(color)
                        self.OpeninterestTable.setItem(row_num, 6, item)

                    elif stock_type == "매도":
                        profit = round(float((float(prc)-float(c)) * float(qty) * float(ctrt_size)), 1)
                        perc = round(float((float(prc)-float(c)) / float(prc)) * 100, 2)

                        # 국내 평가손익,수익률 color setting
                        if float(profit) > 0:
                            color = QColor("red")
                        elif float(profit) < 0:
                            color = QColor("blue")
                        else:
                            color = QColor("black")
                        profit = '{:,}'.format(profit)
                        item = QTableWidgetItem(profit)
                        item.setForeground(color)
                        self.OpeninterestTable.setItem(row_num, 5, item)

                        if float(perc) > 0:
                            color = QColor("red")
                        elif float(perc) < 0:
                            color = QColor("blue")
                        else:
                            color = QColor("black")
                        item = QTableWidgetItem(str(perc))
                        item.setForeground(color)
                        self.OpeninterestTable.setItem(row_num, 6, item)

                # 국내 OpeninterestTable 정렬
                for row in range(self.OpeninterestTable.rowCount()):
                    for col in range(self.OpeninterestTable.columnCount()):
                        if col != 0:
                            item = self.OpeninterestTable.item(row, col)
                            if item is not None:
                                if col == 1:
                                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                                else:
                                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                for col in range(self.OpeninterestTable.columnCount()):
                    if col == 4 or col == 5 or col == 6: # 4, 5, 6번 컬럼인 경우
                        item = self.OpeninterestTable.item(row_num, col)
                        if item is not None:
                            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter) # 우측정렬

        # 국내 호가 실시간
        elif realCode in ['KB']:

            xhms = recvData[18:24]   # 거래소시간
            code = recvData[2:14].replace(' ', '') # 종목코드
            if code == self.current_hoga_stock_code:

                # 거래소시간 문자열에서 시, 분, 초 추출
                hour = xhms[:2]
                minute = xhms[2:4]
                second = xhms[4:]
                # 'hh:mm:ss' 형식으로 변환하여 QTableWidgetItem 객체 생성
                time_str = f"{hour}:{minute}:{second}"
                item = QTableWidgetItem(time_str)

                # 매도
                pask1 = str(recvData[77:86])   # 매도호가1
                pask2 = str(recvData[167:176])   # 매도호가2
                pask3 = str(recvData[257:266])   # 매도호가3
                pask4 = str(recvData[347:356])   # 매도호가4
                pask5 = str(recvData[437:446])   # 매도호가5
                vask1 = str(recvData[86:95])   # 매도수량1
                vask2 = str(recvData[176:185])   # 매도수량2
                vask3 = str(recvData[266:275])   # 매도수량3
                vask4 = str(recvData[356:365])   # 매도수량4
                vask5 = str(recvData[446:455])   # 매도수량5
                nask1 = str(recvData[95:102])   # 매도건수1
                nask2 = str(recvData[185:192])   # 매도건수2
                nask3 = str(recvData[275:282])   # 매도건수3
                nask4 = str(recvData[365:372])   # 매도건수4
                nask5 = str(recvData[455:462])   # 매도건수5
                vask = str(recvData[24:33])   # 총매도수량
                nask = str(recvData[33:40])   # 총매도건수
                # 매수
                pbid1 = str(recvData[122:131])   # 매수호가1
                pbid2 = str(recvData[212:221])   # 매수호가2
                pbid3 = str(recvData[302:311])   # 매수호가3
                pbid4 = str(recvData[392:401])   # 매수호가4
                pbid5 = str(recvData[482:491])   # 매수호가5
                vbid1 = str(recvData[131:140])   # 매수수량1
                vbid2 = str(recvData[221:230])   # 매수수량2
                vbid3 = str(recvData[311:320])   # 매수수량3
                vbid4 = str(recvData[401:410])   # 매수수량4
                vbid5 = str(recvData[491:500])   # 매수수량5
                nbid1 = str(recvData[140:147])   # 매수건수1
                nbid2 = str(recvData[230:237])   # 매수건수2
                nbid3 = str(recvData[320:327])   # 매수건수3
                nbid4 = str(recvData[410:417])   # 매수건수4
                nbid5 = str(recvData[500:507])   # 매수건수5
                vbid = str(recvData[50:59])   # 총매수수량
                nbid = str(recvData[59:66])   # 총매수건수

                # 호가 table 업데이트
                # 거래소시간                 
                self.HogaTable.setHorizontalHeaderItem(2, item)
                # 매도        
                self.HogaTable.item(0, 0).setText(nask1)
                self.HogaTable.item(1, 0).setText(nask2)
                self.HogaTable.item(2, 0).setText(nask3)
                self.HogaTable.item(3, 0).setText(nask4)
                self.HogaTable.item(4, 0).setText(nask5)
                self.HogaTable.item(10, 0).setText(nask)
                self.HogaTable.item(0, 1).setText(vask1)
                self.HogaTable.item(1, 1).setText(vask2)
                self.HogaTable.item(2, 1).setText(vask3)
                self.HogaTable.item(3, 1).setText(vask4)
                self.HogaTable.item(4, 1).setText(vask5)
                self.HogaTable.item(10, 1).setText(vask)

                # 첫 번째 열의 아이템 텍스트를 파란색으로 변경
                for i in range(5):
                    item = self.HogaTable.item(i, 0)
                    item.setForeground(QColor("blue"))

                item = self.HogaTable.item(10, 0)
                item.setForeground(QColor("blue"))

                # 두 번째 열의 아이템 텍스트를 파란색으로 변경
                for i in range(5):
                    item = self.HogaTable.item(i, 1)
                    item.setForeground(QColor("blue"))

                item = self.HogaTable.item(10, 1)
                item.setForeground(QColor("blue"))

                self.HogaTable.item(0, 2).setText(pask1)
                self.HogaTable.item(1, 2).setText(pask2)
                self.HogaTable.item(2, 2).setText(pask3)
                self.HogaTable.item(3, 2).setText(pask4)
                self.HogaTable.item(4, 2).setText(pask5)

                # 매수
                self.HogaTable.item(5, 3).setText(nbid1)
                self.HogaTable.item(6, 3).setText(nbid2)
                self.HogaTable.item(7, 3).setText(nbid3)
                self.HogaTable.item(8, 3).setText(nbid4)
                self.HogaTable.item(9, 3).setText(nbid5)
                self.HogaTable.item(10, 3).setText(nbid)
                self.HogaTable.item(5, 4).setText(vbid1)
                self.HogaTable.item(6, 4).setText(vbid2)
                self.HogaTable.item(7, 4).setText(vbid3)
                self.HogaTable.item(8, 4).setText(vbid4)
                self.HogaTable.item(9, 4).setText(vbid5)
                self.HogaTable.item(10, 4).setText(vbid)

                # 4 번째 열의 아이템 텍스트를 빨간색으로 변경
                for i in range(5, 11):
                    item = self.HogaTable.item(i, 3)
                    item.setForeground(QColor("red"))

                item = self.HogaTable.item(10, 3)
                item.setForeground(QColor("red"))

                # 5 번째 열의 아이템 텍스트를 빨간색으로 변경
                for i in range(5, 11):
                    item = self.HogaTable.item(i, 4)
                    item.setForeground(QColor("red"))

                item = self.HogaTable.item(10, 4)
                item.setForeground(QColor("red"))

                self.HogaTable.item(5, 2).setText(pbid1)
                self.HogaTable.item(6, 2).setText(pbid2)
                self.HogaTable.item(7, 2).setText(pbid3)
                self.HogaTable.item(8, 2).setText(pbid4)
                self.HogaTable.item(9, 2).setText(pbid5)

            # bold format 생성
            bold_format = QTextCharFormat()
            bold_format.setFontWeight(QFont.Bold)

            for row in range(self.HogaTable.rowCount()):
                for col in range(self.HogaTable.columnCount()):
                    item = self.HogaTable.item(row, col)
                    if item is not None:
                        text = item.text().rstrip()  # 우측 공백 제거
                        item.setText(text)  # 일반 텍스트로 설정
                        item.setFont(QFont('Inter', 9, QFont.Bold))  # bold font 적용
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)  # 우측정렬

        # 해외 호가 실시간
        elif realCode in ['FB']:

            xhms = recvData[33:39]   # 거래소시간
            code = recvData[2:22].replace(' ', '') # 종목코드
            if code == self.global_current_hoga_stock_code:

                # 거래소시간 문자열에서 시, 분, 초 추출
                hour = xhms[:2]
                minute = xhms[2:4]
                second = xhms[4:]
                # 'hh:mm:ss' 형식으로 변환하여 QTableWidgetItem 객체 생성
                time_str = f"{hour}:{minute}:{second}"
                item = QTableWidgetItem(time_str)

                # 매도
                pask1 = str(recvData[98:113])   # 매도호가1
                pask2 = str(recvData[182:197])   # 매도호가2
                pask3 = str(recvData[266:281])   # 매도호가3
                pask4 = str(recvData[350:365])   # 매도호가4
                pask5 = str(recvData[434:449])   # 매도호가5
                vask1 = str(recvData[113:122])   # 매도수량1
                vask2 = str(recvData[197:206])   # 매도수량2
                vask3 = str(recvData[281:290])   # 매도수량3
                vask4 = str(recvData[365:374])   # 매도수량4
                vask5 = str(recvData[449:458])   # 매도수량5
                nask1 = str(recvData[122:129])   # 매도건수1
                nask2 = str(recvData[206:213])   # 매도건수2
                nask3 = str(recvData[290:297])   # 매도건수3
                nask4 = str(recvData[374:381])   # 매도건수4
                nask5 = str(recvData[458:465])   # 매도건수5
                vask = str(recvData[45:54])   # 총매도수량
                nask = str(recvData[54:61])   # 총매도건수

                # 매수
                pbid1 = str(recvData[140:155])   # 매수호가1
                pbid2 = str(recvData[224:239])   # 매수호가2
                pbid3 = str(recvData[308:323])   # 매수호가3
                pbid4 = str(recvData[392:407])   # 매수호가4
                pbid5 = str(recvData[476:491])   # 매수호가5
                vbid1 = str(recvData[155:164])   # 매수수량1
                vbid2 = str(recvData[239:248])   # 매수수량2
                vbid3 = str(recvData[323:332])   # 매수수량3
                vbid4 = str(recvData[407:416])   # 매수수량4
                vbid5 = str(recvData[491:500])   # 매수수량5
                nbid1 = str(recvData[164:171])   # 매수건수1
                nbid2 = str(recvData[248:255])   # 매수건수2
                nbid3 = str(recvData[332:339])   # 매수건수3
                nbid4 = str(recvData[416:423])   # 매수건수4
                nbid5 = str(recvData[500:507])   # 매수건수5
                vbid = str(recvData[71:80])   # 총매수수량
                nbid = str(recvData[80:87])   # 총매수건수

                # 호가 table 업데이트
                # 거래소시간                 
                self.HogaTable_glb.setHorizontalHeaderItem(2, item) 
                # 매도        
                self.HogaTable_glb.item(0, 0).setText(nask1)
                self.HogaTable_glb.item(1, 0).setText(nask2)
                self.HogaTable_glb.item(2, 0).setText(nask3)
                self.HogaTable_glb.item(3, 0).setText(nask4)
                self.HogaTable_glb.item(4, 0).setText(nask5)
                self.HogaTable_glb.item(10, 0).setText(nask)
                self.HogaTable_glb.item(0, 1).setText(vask1)
                self.HogaTable_glb.item(1, 1).setText(vask2)
                self.HogaTable_glb.item(2, 1).setText(vask3)
                self.HogaTable_glb.item(3, 1).setText(vask4)
                self.HogaTable_glb.item(4, 1).setText(vask5)
                self.HogaTable_glb.item(10, 1).setText(vask)

                # 첫 번째 열의 아이템 텍스트를 파란색으로 변경
                for i in range(5):
                    item = self.HogaTable_glb.item(i, 0)
                    item.setForeground(QColor("blue"))

                item = self.HogaTable_glb.item(10, 0)
                item.setForeground(QColor("blue"))

                # 두 번째 열의 아이템 텍스트를 파란색으로 변경
                for i in range(5):
                    item = self.HogaTable_glb.item(i, 1)
                    item.setForeground(QColor("blue"))

                item = self.HogaTable_glb.item(10, 1)
                item.setForeground(QColor("blue"))

                self.HogaTable_glb.item(0, 2).setText(pask1)
                self.HogaTable_glb.item(1, 2).setText(pask2)
                self.HogaTable_glb.item(2, 2).setText(pask3)
                self.HogaTable_glb.item(3, 2).setText(pask4)
                self.HogaTable_glb.item(4, 2).setText(pask5)

                # 매수
                self.HogaTable_glb.item(5, 3).setText(nbid1)
                self.HogaTable_glb.item(6, 3).setText(nbid2)
                self.HogaTable_glb.item(7, 3).setText(nbid3)
                self.HogaTable_glb.item(8, 3).setText(nbid4)
                self.HogaTable_glb.item(9, 3).setText(nbid5)
                self.HogaTable_glb.item(10, 3).setText(nbid)
                self.HogaTable_glb.item(5, 4).setText(vbid1)
                self.HogaTable_glb.item(6, 4).setText(vbid2)
                self.HogaTable_glb.item(7, 4).setText(vbid3)
                self.HogaTable_glb.item(8, 4).setText(vbid4)
                self.HogaTable_glb.item(9, 4).setText(vbid5)
                self.HogaTable_glb.item(10, 4).setText(vbid)

                # 4 번째 열의 아이템 텍스트를 빨간색으로 변경
                for i in range(5, 11):
                    item = self.HogaTable_glb.item(i, 3)
                    item.setForeground(QColor("red"))

                item = self.HogaTable_glb.item(10, 3)
                item.setForeground(QColor("red"))

                # 5 번째 열의 아이템 텍스트를 빨간색으로 변경
                for i in range(5, 11):
                    item = self.HogaTable_glb.item(i, 4)
                    item.setForeground(QColor("red"))

                item = self.HogaTable_glb.item(10, 4)
                item.setForeground(QColor("red"))

                self.HogaTable_glb.item(5, 2).setText(pbid1)
                self.HogaTable_glb.item(6, 2).setText(pbid2)
                self.HogaTable_glb.item(7, 2).setText(pbid3)
                self.HogaTable_glb.item(8, 2).setText(pbid4)
                self.HogaTable_glb.item(9, 2).setText(pbid5)

            # bold format 생성
            bold_format = QTextCharFormat()
            bold_format.setFontWeight(QFont.Bold)

            for row in range(self.HogaTable_glb.rowCount()):
                for col in range(self.HogaTable_glb.columnCount()):
                    item = self.HogaTable_glb.item(row, col)
                    if item is not None:
                        text = item.text().rstrip()  # 우측 공백 제거
                        item.setText(text)  # 일반 텍스트로 설정
                        item.setFont(QFont('Inter', 9, QFont.Bold))  # bold font 적용
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)  # 우측정렬

        # 실시간 해외
        elif realCode in ['FA']:
            o = recvData[63:78]
            h = recvData[79:94]
            l = recvData[95:110]
            c = recvData[111:126]
            rate = recvData[144:150]
            tvol = recvData[158:170]
            code = recvData[2:22].replace(" ", "")

            # 데이터 테이블 값들 실시간 업데이트 
            if code in self.global_datatable_stock_list:
                row_num = self.global_datatable_stock_list.index(code)
                self.dataTable_glb.setItem(row_num, 1, QTableWidgetItem(c.rstrip()))
                self.dataTable_glb.setItem(row_num, 2, QTableWidgetItem(o))
                self.dataTable_glb.setItem(row_num, 3, QTableWidgetItem(h))
                self.dataTable_glb.setItem(row_num, 4, QTableWidgetItem(l))
                self.dataTable_glb.setItem(row_num, 5, QTableWidgetItem(tvol.rstrip()))

                # 해외 등락률 color stting
                if float(rate) > 0:
                    color = QColor("red")
                elif float(rate) < 0:
                    color = QColor("blue")
                else:
                    color = QColor("black")

                item = QTableWidgetItem(rate.rstrip())
                item.setForeground(color)
                self.dataTable_glb.setItem(row_num, 6, item)

                # 해외 datatable 우측정렬
                for row in range(self.dataTable_glb.rowCount()):
                    for col in range(self.dataTable_glb.columnCount()):
                        if col != 0:
                            item = self.dataTable_glb.item(row, col)
                            if item is not None:
                                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            for row_num in range(self.OpeninterestTable_glb.rowCount()):

                stock_name = self.OpeninterestTable_glb.item(row_num, 0).text()
                stock_type = self.OpeninterestTable_glb.item(row_num, 1).text()
                qty = self.OpeninterestTable_glb.item(row_num, 2).text()
                prc = self.OpeninterestTable_glb.item(row_num, 3).text()

                if self.global_stock_rel_name_code_dict[stock_name] == code:
                    ctrt_size = self.global_stock_rel_code_ctrt_size_dict[code] 
                    self.OpeninterestTable_glb.setItem(row_num, 4, QTableWidgetItem(c.rstrip()))
                    if stock_type == "매수":
                        profit = round(float((float(c)-float(prc)) * float(qty) * float(ctrt_size)), 3)
                        perc = round(float((float(c)-float(prc)) / float(prc)) * 100, 2)

                        # 해외 평가손익,수익률 color setting
                        if float(profit) > 0:
                            color = QColor("red")
                        elif float(profit) < 0:
                            color = QColor("blue")
                        else:
                            color = QColor("black")
                        item = QTableWidgetItem(str(profit))
                        item.setForeground(color)
                        self.OpeninterestTable_glb.setItem(row_num, 5, item)

                        if float(perc) > 0:
                            color = QColor("red")
                        elif float(perc) < 0:
                            color = QColor("blue")
                        else:
                            color = QColor("black")
                        item = QTableWidgetItem(str(perc))
                        item.setForeground(color)
                        self.OpeninterestTable_glb.setItem(row_num, 6, item)

                    elif stock_type == "매도":
                        profit = round(float((float(prc)-float(c)) * float(qty) * float(ctrt_size)), 3)
                        perc = round(float((float(prc)-float(c)) / float(prc)) * 100, 2)

                        # 해외 평가손익,수익률 color setting
                        if float(profit) > 0:
                            color = QColor("red")
                        elif float(profit) < 0:
                            color = QColor("blue")
                        else:
                            color = QColor("black")
                        item = QTableWidgetItem(str(profit))
                        item.setForeground(color)
                        self.OpeninterestTable_glb.setItem(row_num, 5, item)

                        if float(perc) > 0:
                            color = QColor("red")
                        elif float(perc) < 0:
                            color = QColor("blue")
                        else:
                            color = QColor("black")
                        item = QTableWidgetItem(str(perc))
                        item.setForeground(color)
                        self.OpeninterestTable_glb.setItem(row_num, 6, item)    

                # 해외 OpeninterestTable 정렬
                for row in range(self.OpeninterestTable_glb.rowCount()):
                    for col in range(self.OpeninterestTable_glb.columnCount()):
                        if col != 0:
                            item = self.OpeninterestTable_glb.item(row, col)
                            if item is not None:
                                if col == 1:
                                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                                else:
                                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                for col in range(self.OpeninterestTable_glb.columnCount()):
                        if col == 4 or col == 5 or col == 6: # 4, 5, 6번 컬럼인 경우
                            item = self.OpeninterestTable_glb.item(row_num, col)
                            if item is not None:
                                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter) # 우측정렬

        # 주문 체결, 미체결
        elif realCode == 'O1':

            recvData_ = recvData.encode('euc-kr')

            # 종목명           
            code = recvData_[114:146].decode('euc-kr').replace(' ', '')
            # 국내인지 체크
            if code in self.stock_rel_code_name_dict.keys():                
                stock_name = self.stock_rel_code_name_dict[code]
                # 거래구분
                buy_sell_tp = recvData_[147:148].decode('euc-kr')
                if buy_sell_tp == "1":
                    buy_sell_tp_text = "매수"
                    color = QColor("red")
                else:
                    buy_sell_tp_text = "매도"
                    color = QColor("blue")

                # 호가 유형
                mnp_tp = str(recvData_[148:149].decode('euc-kr'))
                ord_sts_tp = str(recvData_[146:147].decode('euc-kr'))
                org_ord_dt = str(recvData_[103:113].decode('euc-kr'))
                if mnp_tp == "1":
                    if ord_sts_tp == "3":
                        ord_sts_tp_text = "미체결"
                    elif ord_sts_tp == "1":
                        ord_sts_tp_text = "미접수"
                    elif ord_sts_tp == "4":
                        ord_sts_tp_text = "부분체결"
                    elif ord_sts_tp == "6":
                        ord_sts_tp_text = "체결"
                    elif ord_sts_tp == "9":
                        ord_sts_tp_text = "거부"
                    else:
                        ord_sts_tp_text = "미확인"
                elif mnp_tp == "2":
                    ord_sts_tp_text = "정정"
                    if ord_sts_tp == "3":
                        ord_sts_tp_text = "미체결"
                    elif ord_sts_tp == "1":
                        ord_sts_tp_text = "미접수"
                    elif ord_sts_tp == "4":
                        ord_sts_tp_text = "부분체결"
                    elif ord_sts_tp == "6":
                        ord_sts_tp_text = "체결"
                    elif ord_sts_tp == "9":
                        ord_sts_tp_text = "거부"
                    else:
                        ord_sts_tp_text = "미확인"
                    for row_num in range(self.ExecutionTable.rowCount()):
                        existed_ord_no = self.ExecutionTable.item(row_num, 1).text()                    
                        if existed_ord_no == org_ord_dt:
                            self.ExecutionTable.removeRow(row_num)

                elif mnp_tp == "3":
                    ord_sts_tp_text = "취소"
                    for row_num in range(self.ExecutionTable.rowCount()):
                        existed_ord_no = self.ExecutionTable.item(row_num, 1).text()                    
                        if existed_ord_no == org_ord_dt:
                            self.ExecutionTable.removeRow(row_num)


                # 상태


                # 주문번호
                ord_no = str(recvData_[85:95].decode('euc-kr'))

                # 주문량
                ord_qty = str(float( recvData_[151:158].decode('euc-kr')))

                # 체결량
                exec_qtyv = str(float(recvData_[158:165].decode('euc-kr')))

                # 잔량
                ord_rmqy_qtyv = str(float(ord_qty) - float(exec_qtyv))

                # 주문가
                ord_prc = str(float(recvData_[179:194].decode('euc-kr')))

                # 체결가
                try:
                    exec_prc = str(float(recvData_[194:209].decode('euc-kr')))
                except:
                    exec_prc = str('')

                # 체결, 미체결 정보창
                flag = 1
                for row_num in range(self.ExecutionTable.rowCount()):

                    existed_ord_no = self.ExecutionTable.item(row_num, 1).text()                    

                    if existed_ord_no == ord_no:

                        self.ExecutionTable.setItem(row_num, 0, QTableWidgetItem(stock_name))
                        self.ExecutionTable.setItem(row_num, 1, QTableWidgetItem(ord_no))
                        item = QTableWidgetItem(buy_sell_tp_text)
                        item.setForeground(color)
                        self.ExecutionTable.setItem(row_num, 2, item)
                        self.ExecutionTable.setItem(row_num, 3, QTableWidgetItem(ord_sts_tp_text))
                        self.ExecutionTable.setItem(row_num, 4, QTableWidgetItem(ord_qty))
                        self.ExecutionTable.setItem(row_num, 5, QTableWidgetItem(exec_qtyv))
                        self.ExecutionTable.setItem(row_num, 6, QTableWidgetItem(ord_rmqy_qtyv))
                        self.ExecutionTable.setItem(row_num, 7, QTableWidgetItem(ord_prc))
                        self.ExecutionTable.setItem(row_num, 8, QTableWidgetItem(exec_prc))
                        flag = 0

                # 없다면 새로 생성
                if flag == 1:
                    row_num = self.ExecutionTable.rowCount()
                    self.ExecutionTable.insertRow(row_num)
                    self.ExecutionTable.setItem(row_num, 0, QTableWidgetItem(stock_name))
                    self.ExecutionTable.setItem(row_num, 1, QTableWidgetItem(ord_no))
                    item = QTableWidgetItem(buy_sell_tp_text)
                    item.setForeground(color)
                    self.ExecutionTable.setItem(row_num, 2, item)
                    self.ExecutionTable.setItem(row_num, 3, QTableWidgetItem(ord_sts_tp_text))
                    self.ExecutionTable.setItem(row_num, 4, QTableWidgetItem(ord_qty))
                    self.ExecutionTable.setItem(row_num, 5, QTableWidgetItem(exec_qtyv))
                    self.ExecutionTable.setItem(row_num, 6, QTableWidgetItem(ord_rmqy_qtyv))
                    self.ExecutionTable.setItem(row_num, 7, QTableWidgetItem(ord_prc))
                    self.ExecutionTable.setItem(row_num, 8, QTableWidgetItem(exec_prc))

                # 국내 ExecutionTable 우측정렬
                for row in range(self.ExecutionTable.rowCount()):
                    for col in range(self.ExecutionTable.columnCount()):
                        if col != 0:
                            item = self.ExecutionTable.item(row, col)
                        if item is not None:
                            if col == 2 or col == 3:
                                item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                            else:
                                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                # 종목이 체결되면 ord_sts_tp 값 6
                if ord_sts_tp == '6':
                    data_string = "1" + self.acc_no + self.encoded_pwd + self.daynight + ' ' * 156
                    self.pySBtrader.doRequestData(-1, "sdbs3085q01", data_string, "", "")

            # 국내에 없으면 해외 주문임
            else:
                stock_name = self.global_stock_rel_code_name_dict[code]
                # 거래구분
                buy_sell_tp = recvData_[147:148].decode('euc-kr')
                if buy_sell_tp == "1":
                    buy_sell_tp_text = "매수"
                    color = QColor("red")
                else:
                    buy_sell_tp_text = "매도"
                    color = QColor("blue")

                # 상태
                mnp_tp = str(recvData_[148:149].decode('euc-kr'))
                ord_sts_tp = str(recvData_[146:147].decode('euc-kr'))
                org_ord_dt = str(recvData_[103:113].decode('euc-kr'))
                if mnp_tp == "1":
                    if ord_sts_tp == "3":
                        ord_sts_tp_text = "미체결"
                    elif ord_sts_tp == "1":
                        ord_sts_tp_text = "미접수"
                    elif ord_sts_tp == "4":
                        ord_sts_tp_text = "부분체결"
                    elif ord_sts_tp == "6":
                        ord_sts_tp_text = "체결"
                    elif ord_sts_tp == "9":
                        ord_sts_tp_text = "거부"
                elif mnp_tp == "2":
                    ord_sts_tp_text = "정정"
                    if ord_sts_tp == "3":
                        ord_sts_tp_text = "미체결"
                    elif ord_sts_tp == "1":
                        ord_sts_tp_text = "미접수"
                    elif ord_sts_tp == "4":
                        ord_sts_tp_text = "부분체결"
                    elif ord_sts_tp == "6":
                        ord_sts_tp_text = "체결"
                    elif ord_sts_tp == "9":
                        ord_sts_tp_text = "거부"
                    for row_num in range(self.ExecutionTable_glb.rowCount()):
                        existed_ord_no = self.ExecutionTable_glb.item(row_num, 1).text()                    
                        if existed_ord_no == org_ord_dt:
                            self.ExecutionTable_glb.removeRow(row_num)
                elif mnp_tp == "3":
                    ord_sts_tp_text = "취소"
                    for row_num in range(self.ExecutionTable_glb.rowCount()):
                        existed_ord_no = self.ExecutionTable_glb.item(row_num, 1).text()                    
                        if existed_ord_no == org_ord_dt:
                            self.ExecutionTable_glb.removeRow(row_num)

                # 주문번호
                ord_no = str(recvData_[85:95].decode('euc-kr'))

                # 주문량
                ord_qty = str(float( recvData_[151:158].decode('euc-kr')))

                # 체결량
                exec_qtyv = str(float(recvData_[158:165].decode('euc-kr')))

                # 잔량
                ord_rmqy_qtyv = str(float(ord_qty) - float(exec_qtyv))

                # 주문가
                ord_prc = str(float(recvData_[179:194].decode('euc-kr')))

                # 체결가
                try:
                    exec_prc = str(float(recvData_[194:209].decode('euc-kr')))
                except:
                    exec_prc = str('')

                # 체결, 미체결 정보창
                flag = 1
                for row_num in range(self.ExecutionTable_glb.rowCount()):

                    existed_ord_no = self.ExecutionTable_glb.item(row_num, 1).text()

                    if existed_ord_no == ord_no:

                        self.ExecutionTable_glb.setItem(row_num, 0, QTableWidgetItem(stock_name))
                        self.ExecutionTable_glb.setItem(row_num, 1, QTableWidgetItem(ord_no))
                        item = QTableWidgetItem(buy_sell_tp_text)
                        item.setForeground(color)
                        self.ExecutionTable_glb.setItem(row_num, 2, item)
                        self.ExecutionTable_glb.setItem(row_num, 3, QTableWidgetItem(ord_sts_tp_text))
                        self.ExecutionTable_glb.setItem(row_num, 4, QTableWidgetItem(ord_qty))
                        self.ExecutionTable_glb.setItem(row_num, 5, QTableWidgetItem(exec_qtyv))
                        self.ExecutionTable_glb.setItem(row_num, 6, QTableWidgetItem(ord_rmqy_qtyv))
                        self.ExecutionTable_glb.setItem(row_num, 7, QTableWidgetItem(ord_prc))
                        self.ExecutionTable_glb.setItem(row_num, 8, QTableWidgetItem(exec_prc))
                        flag = 0

                # 없다면 새로 생성
                if flag == 1:
                    row_num = self.ExecutionTable_glb.rowCount()
                    self.ExecutionTable_glb.insertRow(row_num)
                    self.ExecutionTable_glb.setItem(row_num, 0, QTableWidgetItem(stock_name))
                    self.ExecutionTable_glb.setItem(row_num, 1, QTableWidgetItem(ord_no))
                    item = QTableWidgetItem(buy_sell_tp_text)
                    item.setForeground(color)
                    self.ExecutionTable_glb.setItem(row_num, 2, item)
                    self.ExecutionTable_glb.setItem(row_num, 3, QTableWidgetItem(ord_sts_tp_text))
                    self.ExecutionTable_glb.setItem(row_num, 4, QTableWidgetItem(ord_qty))
                    self.ExecutionTable_glb.setItem(row_num, 5, QTableWidgetItem(exec_qtyv))
                    self.ExecutionTable_glb.setItem(row_num, 6, QTableWidgetItem(ord_rmqy_qtyv))
                    self.ExecutionTable_glb.setItem(row_num, 7, QTableWidgetItem(ord_prc))
                    self.ExecutionTable_glb.setItem(row_num, 8, QTableWidgetItem(exec_prc))

                # 해외 ExecutionTable 우측정렬
                for row in range(self.ExecutionTable_glb.rowCount()):
                    for col in range(self.ExecutionTable_glb.columnCount()):
                        if col != 0:
                            item = self.ExecutionTable_glb.item(row, col)
                        if item is not None:
                            if col == 2 or col == 3:
                                item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                            else:
                                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                if ord_sts_tp == '6':
                    ord_sts_tp_text = "체결"
                    data_string = "0" * 100 + '2' + self.acc_no_glb + ' ' * 50 + '9'
                    self.pySBtrader.doRequestData(-1, "SGBS9001Q03", data_string, "", "")

    def showPopupWindow(self, text):

        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle("Alarm")
        msg.setWindowModality(Qt.ApplicationModal)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    font = QFont("Inter", 9)
    app.setFont(font)
    Window = mainWindow() 
    Window.show()
    app.exec_()
