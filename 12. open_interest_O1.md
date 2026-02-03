# 미결제약정 실시간으로 구현하는 방법

써핑보드에는 미결제 약정을 실시간으로 받아올 수 있는 TR이 없습니다.


그렇기 때문에,

1) 실시간으로 체결 값이 받아와졌을때, (실시간 TR명 O1)

2) 실시간 현재가가 업데이트 됬을 때, (실시간 TR명 KA)

마다 미결제 약정 테이블을 업데이트 해주어야 합니다.

#### 혹시 1초마다 미결제 약정을 호출해서 업데이트 하면 되지 않냐라고 생각하실 수도 있는데, 서버쪽에 과부하가 걸릴 수 있기 때문에, 써핑보드에서는 1초당 20번의 요청 제한이 걸려 있습니다.

그래서 가급적이면, 실시간 TR을 최대한 활용하는 것이 좋습니다.

## 실시간 O1에서 미결제약정 테이블 업데이트
앞에 8장 체결 미체결 구현에서 설명하였듯이 체결, 미체결 데이터를 받아서 만약에 체결이 됬다면, 미결제 약정을 업데이트 해주어야합니다.

아래는 체결 미체결 실시간 데이터에서 체결이 됬을때 처리하는 부분입니다.
```ruby
# 종목이 체결되면 ord_sts_tp 값 6
if ord_sts_tp == '6':
            data_string = "1" + self.acc_no + self.encoded_pwd + self.daynight + ' ' * 156
            self.pySBtrader.doRequestData(-1, "sdbs3085q01", data_string, "", "")
```

ord_sts_tp가 6이면 체결이 됬다는 뜻이고, 체결이 됬을때, sdbs3085q01 TR에 요청을 합니다.

sdbs3085q01 TR은 미체결 약정 데이터들을 호출하는 TR 값입니다.

미체결 약정 데이터는 connectReceiveData 함수를 통해 전달 받게 됩니다.

아래는 connectReceiveData 함수안에 미체결 약정 데이터를 처리하는 부분입니다.

```ruby
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
```

#### 중요한 부분은 데이터값이 여러개로 넘어오기 때문에, 데이터를 항목별로 길이를 잘 잘라서 사용하는 것이 중요합니다.
```ruby
    for i in range(0, cnt):
                idx = i * 458
                data_body_ = data_body[0 + idx : 458 + idx]
                row_num = i
```

#### 위에 이부분 처럼 한 항목당 길이가 458이기 때문에, idx 값을 줘서 구간별로 잘라내는 작업을 합니다.

저렇게 한 종목마다 데이터를 자르고 나면, 해당 종목에 현재가, 매수가, 등락율 등등을 파싱해서 가져오면 됩니다. 그리고 나서 다른 챕터에서 했던 것처럼, 색상을 입히고 정렬을 해주면 됩니다.

아래는 해외코드입니다.
```ruby
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
```
