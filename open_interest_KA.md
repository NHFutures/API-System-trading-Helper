## 실시간 KA(현재가)를 미결제약정 테이블에 업데이트

미결제 약정 테이블에는 해당 종목에 현재가와 수익률을 가져오는 부분이 있습니다.

#### 현재가와 수익률을 실시간으로 업데이트 해주기 위해서는 실시간 TR인 KA에서 처리를 해줘야합니다.

아래는 connectReceiveReal 함수 밑에 KA 부분입니다.
```ruby
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
여기서 중요하게 봐야할 부분은 미결제 약정 테이블 업데이트 입니다.

```ruby
    if self.stock_rel_name_code_dict[stock_name] == code:
                    ctrt_size = self.stock_rel_code_ctrt_size_dict[code] 
                    self.OpeninterestTable.setItem(row_num, 4, QTableWidgetItem(c))
                    if stock_type == "매수":
                        profit = round(float((float(c)-float(prc)) * float(qty) * float(ctrt_size)) , 1)
                        perc = round(float((float(c)-float(prc)) / float(prc)) * 100, 2)
```
#### 만약 미결제 약정 테이블에서 실시간 KA(현재가)에서 가져온 종목이름과 일치하는 종목이 있다면, 위와 같은 방식으로 매수 또는 매도시에 profit(수익금)과 perc(수익률)을 계산해줍니다.
#### ctrt_size는 거래단위라는 값으로, 수익금을 계산할때 위와 같은 공식으로 구하도록 써핑보드 API에서 가이드를 하고 있습니다.

여기서는, 수익률을 계산하는 공식은 따로 자세히 설명하지 않겠습니다.

#### 해외는 FB라는 실시간 현재가 TR을 이용하고 있습니다.
