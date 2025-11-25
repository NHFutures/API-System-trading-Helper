## 계좌 연결하기

#### 계좌연결은 전체 계좌 불러오기와 연결로 구성되어있습니다.
#### 전체계좌를 불러오는 함수는 아래와 같습니다.

```ruby
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
```

#### doGetAccountInfCount로 보유하고 있는 계좌의 총 개수를 불러온 다음에, doGetAccountInf 함수로 계좌의 i번째 인덱스에 해당하는 계좌의 계좌번호를 불러오는 방식입니다.
#### 아래는 계좌 목록에서 한 계좌를 연결 버튼을 눌렀을 때 실행되는 함수입니다.

```ruby
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
```

#### 계좌 예탁자산을 업데이트 하는 방식은 최초에 예탁자산 TR(sdbs5001q01)을 요청을 보내고,
```ruby
self.pySBtrader.doRequestData(-1, "sdbs5001q01", data_string, "", "")
```
#### 이후에는 5초마다 TR 요청을 보내는 함수를 스케줄러로 등록합니다. (스케줄러에 대한 보다 자세한 설명이 필요하다면 "11.부록 - 1)주야간 확인" 페이지를 참고해주세요.)
```ruby
self.sched.add_job(self.updateAccountInfo, 'interval', seconds=5, id='updateAccountInfo') 
self.button_connect_acc.setEnabled(False)
```

#### 그 외에는 처음에 계좌를 연결하면, 체결 미체결 내역과 미결제 내역등을 최초에 내역들을 가져와야 하기 때문에 관련된 TR들을 호출해주면 됩니다.
```ruby
data_string = "1" + self.acc_no + self.encoded_pwd + self.daynight + ' ' * 156
self.pySBtrader.doRequestData(-1, "sdbs3085q01", data_string, "", "")

# sdbs3066q01: 초기 체결 조회
data_string = "11" + ' ' * 8 + self.acc_no + self.encoded_pwd + ' ' * 50 + '00' + ' ' * 32 + '00010 Y   ' + ' ' * 101
self.pySBtrader.doRequestData(-1, "sdbs3066q01", data_string, "", "")

# sdbs3066q01: 초기 미체결 조회
data_string = "11" + ' ' * 8 + self.acc_no + self.encoded_pwd + ' ' * 50 + '00' + ' ' * 32 + '00020 Y   ' + ' ' * 101
self.pySBtrader.doRequestData(-1, "sdbs3066q01", data_string, "", "")
```

#### 계좌에 실시간 체결 내용들도 받아와지게끔 추가해주면 계좌를 연결했을때, 해야할 일들은 마무리가 됩니다.
```ruby
self.pySBtrader.doRegistReal('O1', self.acc_no)
```

#### 아래는 해외 부분의 코드입니다.
```ruby
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
```
