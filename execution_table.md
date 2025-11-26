# 체결, 미체결 탭 구현하기

체결 미체결은 실시간 TR O1에서 값들을 보내줍니다.

그러므로, 앞에서 했듯이 connectReceiveReal이라는 함수로 부터 실시간 데이터들을 받아서 처리해야합니다.
```ruby
def connectReceiveReal(self, realCode: str, realKey: str, recvData: str, UserArea):
```

## 전체 코드 보기
```ruby
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

                if ord_sts_tp == '6':
                    ord_sts_tp_text = "체결"
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

```
다소 길어 보이지만 나누어서 보면 별 것 아닙니다.

## 세부 코드 분석

코드를 쪼개서 봐보겠습니다.

먼저 데이터를 처리할때에는 인코딩과 디코딩처리를 해야합니다.

```ruby
recvData_ = recvData.encode('euc-kr')
code = recvData_[114:146].decode('euc-kr').replace(' ', '')
```
위에서, encode를 euc-kr로 먼저 해주고 나서 다시 decode를 해서 값을 가져오는 것이 보입니다.

이렇게 하는 이유는, 써핑보드 API로 데이터를 받아올 때,

#### 써핑보드에 나와있는 문서에 데이터길이대로 자르려면 한글 바이트 계산을 하기쉽게 euc-kr로 변환해주는게 편하기 때문입니다. (한글은 2바이트, 그 외에는 1바이트)

위에 처럼 하면 API 문서에 나온대로 해당 길이를 추출하면 원하는 값을 얻어낼 수가 있습니다.

위에서는 써핑보드 API 문서에 나와있는대로 O1에서 114~146번째에 해당하는 값을 추출하면 종목코드를 얻어낼 수가 있습니다.

그후에,
```ruby
# 국내인지 체크
            if code in self.stock_rel_code_name_dict.keys():    
```
종목이 국내 종목들을 담아놓은 딕셔너리 변수에 있는지를 확인해서, 종목코드가 해외인지 국내인지를 확인합니다.

(현재, 국내와 해외가 모두 O1으로 들어 오고 있기 때문에, 이것이 국내인지 해외인지를 판별해야됩니다.)

그 후에는 종목이 현재 정정인지 취소인지, 일반주문인지, 그리고 체결인지 미체결인지 등의 값들을 가져옵니다.
```ruby
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
```
정정과 체결일 경우에는, 기존 미체결 주문을 지웁니다. (removeRow)
```ruby
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
```
체결, 미체결 테이블에 각각의 값들을 집어 넣어줍니다. 기존에 업데이트 해야되는 정보들은 업데이트를 해주고, 신규로 생성된 주문은 신규로 생성해주면 됩니다.


마지막으로는, 체결이 만약 됬다면, 미체결 약정 테이블을 업데이트 해줍니다.
```ruby
if ord_sts_tp == '6':
                    ord_sts_tp_text = "체결"
                    data_string = "1" + self.acc_no + self.encoded_pwd + self.daynight + ' ' * 156
                    self.pySBtrader.doRequestData(-1, "sdbs3085q01", data_string, "", "")
```
미체결 약정 테이블을 왜 다른 곳에서 업데이트하냐고 생각할 수 있는데, 이는 미체결 약정 테이블에서 다시 설명드리겠습니다.


해외 코드 역시 동일하기 때문에 추가적인 설명 없이 코드만 보여드리겠습니다.
```ruby
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
```
