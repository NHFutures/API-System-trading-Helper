## 실시간 OHLCV 받아오기

#### 실시간 OHLCV를 받아오는 창은 아래와 같이 생겼습니다.
<img src="https://wikidocs.net/images/page/197893/Untitled.png" width="600" height="400"/>

추가를 누르면 종목이 추가됩니다.

삭제를 누르면 테이블에서 선택된 종목이 삭제가 됩니다.

전체삭제를 누르면 테이블에 모든 종목들이 삭제가 됩니다.

종목 추가부터 보겠습니다.

```ruby
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
```

#### 콤보박스가 종목명인지 종목코드인지를 확인해서 종목과 코드 값을 가져옵니다.
#### 이때, 아래의 파이썬 딕셔너리는 각각 다음과 같은 값을 가지고 있습니다.

```ruby
self.stock_rel_name_code_dict[name]        # name과 매칭이 되는 code를 가져옴.
self.stock_rel_code_name_dict[code]        # code와 매칭이 되는 name을 가져옴.
```
#### 이후에 종목을 추가 하게 됩니다.

#### KA는 실시간 TR로 실시간 체결가 정보를 가져옵니다.
```ruby
self.pySBtrader.doRegistReal("KA", code)
```

#### 이런 실시간 데이터를 처리하는 시그널 함수는 connectReceiveReal입니다.
```ruby
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
```

#### 실시간 TRCode값이 KA라면 데이터에 해당부분을 잘라내서 o, h, l ,c, rate(등락률), tvol(거래량), code 값들을 가져옵니다.
```ruby
if realCode in ['KA']:
            o = recvData[22:31]
            h = recvData[32:41]
            l = recvData[42:51]
            c = recvData[52:61]
            rate = recvData[73:79]
            tvol = recvData[87:99]
            code = recvData[2:14].replace(" ", "")
```

#### 이후에는 dataTable, 즉, 실시간 OHLCV를 보여주고 있는 테이블에 해당 값들을 넣어주기만 하면 끝입니다.
```ruby
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
```

값들을 넣어준 이후에, 색깔을 입히고 정렬까지 하면 더 예쁘고 깔끔하게 완성이 됩니다.

그밖에도 실시간 데이터를 받아왔을때 처리해야될 부분이 있습니다.
바로, 미결제 약정 테이블에 현재가와 수익률을 실시간으로 업데이트 해주는 부분입니다.
#### 이는, 미결제 약정이 실시간 TR이 없기때문에 임시방편으로 KA를 처리하면서 미결제 약정 테이블도 업데이트를 해준다고 보시면 됩니다.

실시간 처리가 되지 않으면, 스케줄러로 처리해야되는데 5초마다 미결제 약정 페이지가 업데이트 된다고 한다면 너무 불편할 것입니다.

그래서, 아래는 미결제 약정 테이블을 KA에서 실시간으로 업데이트 해주는 부분입니다.
```ruby
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
```
여기서도, 색깔을 입히고 데이터들을 한쪽으로 예쁘게 정렬을 해주면 마무리가 됩니다.

자세한 내용은, 미결제 약정 페이지 구현에서 추후에 더 자세하게 설명하겠습니다.
