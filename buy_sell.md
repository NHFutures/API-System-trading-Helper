## 매수 매도 구현하기

매수창에는 4가지의 버튼이 있습니다. 매수, 매도, 정정, 취소입니다.
#### 항상 함수들을 사용하기전에 버튼들과 연결을 해두어야 합니다.

```ruby
# 국내
self.button_buy.clicked.connect(self.buystock)
self.button_sell.clicked.connect(self.sellstock)
self.button_modify.clicked.connect(self.modifystock)
self.button_cancel.clicked.connect(self.cancelstock)

# 해외
self.button_buy_glb.clicked.connect(self.buyGlobalstock)
self.button_sell_glb.clicked.connect(self.sellGlobalstock)
self.button_modify_glb.clicked.connect(self.modifyGlobalstock)
self.button_cancel_glb.clicked.connect(self.cancelGlobalstock)
```
#### 매수 함수는 buystock입니다.

```ruby
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
```

콤보박스인 combo_order_type이 지정가인지 시장가인지에 따라 다르게 처리를 해줍니다.
#### 사용자가 입력한 code, amount, price를 각각 받아와서 doRequestDomNewOrder라는 함수에 입력하면 매수가 됩니다.
self.daynight은 여기서 주간인지 야간인지를 판단하게 해주는 함수입니다. 이부분에 대한 설명은 부록에 따로 자세하게 나와 있습니다.

이번에는 매도 부분의 함수를 보겠습니다.
```ruby
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
```

매수와 동일하고 단지 doRequestDomNewOrder함수 중간에 넣는값이 2로 바뀌었습니다.

다음은 정정부분의 코드입니다.
```ruby
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
```

#### 정정부분의 코드는 사용자가 체결, 미체결 테이블의 row를 선택을 했는지를 확인합니다.
row를 선택하지 않으면
```
"정정할 주문을 선택해주세요."
```
라는 문구를 로그창에 띄워주고,

#### row를 선택했을 시에만, 해당 row에 해당하는 종목코드와 입력받은 정정수량과 가격으로 정정주문을 냅니다.
이때, 정정주문하는 함수는 doRequestDomModifyOrder입니다.

취소 주문도 정정 주문과 비슷하게 row를 선택해야 합니다.
```ruby
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
```

#### doRequestDomCancelOrder가 취소 주문을 내는 함수입니다.

이렇게 주문을 내고나면, 주문들이 잘 체결이 되었는지는 실시간 TR인 “O1”으로 오게됩니다. 이부분은 추후에 미체결약정 구현과 체결, 미체결 구현에서 자세하게 설명하겠습니다.

아래는 해외 코드로 국내와 거의 동일합니다.
```ruby
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
```
