## 실시간 호가창 구현하기

#### 이번에는 호가창 구현을 해보겠습니다.
<img src="https://wikidocs.net/images/page/197894/Untitled.png" width="400" height="600"/>

#### 호가창은 실시간 종목 가격 테이블(5장에서 구현한)에서 해당 종목의 row를 클릭하면 실시간 호가창에 호가 데이터들이 띄게 되는 방식입니다.
#### 해당 테이블의 row를 클릭하게되면 connectHoga함수를 호출하도록 연결해줍니다.
```ruby
self.dataTable.cellClicked.connect(self.connectHoga)
```

#### connectHoga함수에서는 현재 선택된 종목의 코드값을 가져와 실시간 호가 TR을 호출해줍니다.
#### 실시간 호가 TR은 KB입니다.
```ruby
def connectHoga(self):

        row_num = self.dataTable.currentRow()
        name = self.dataTable.item(row_num, 0).text()
        code = self.stock_rel_name_code_dict[name]
        if code != self.current_hoga_stock_code:
            self.textEdit_table.append("{} 가(이) 선택되었습니다.".format(name))
            self.pySBtrader.doUnRegistReal('KB', self.current_hoga_stock_code)
            self.current_hoga_stock_code = code
            self.pySBtrader.doRegistReal('KB', self.current_hoga_stock_code)
```

아래는 해외 호가창 코드입니다.
```ruby
def connectGlobalHoga(self):

        row_num = self.dataTable_glb.currentRow()
        name = self.dataTable_glb.item(row_num, 0).text()
        code = self.global_stock_rel_name_code_dict[name]
        if code != self.global_current_hoga_stock_code:
            self.textEdit_table_glb.append("{} 가(이) 선택되었습니다.".format(name))
            self.pySBtrader.doUnRegistReal('FB', self.global_current_hoga_stock_code)
            self.global_current_hoga_stock_code = code
            self.pySBtrader.doRegistReal('FB', self.global_current_hoga_stock_code)
```

이제 KB로 호출된 호가 데이터들이 서버에서부터 넘어오면 호가창 테이블에 띄워주면 됩니다.
```ruby
def connectReceiveReal(self, realCode: str, realKey: str, recvData: str, UserArea):
```

#### KB는 실시간 데이터이므로, connectReceiveReal 함수 밑에서 처리를 해주어야 합니다.
처리하는 코드는 아래와 같습니다.
```ruby
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
        self.HogaTable.item(0, 0).setText(nask5)
        self.HogaTable.item(1, 0).setText(nask4)
        self.HogaTable.item(2, 0).setText(nask3)
        self.HogaTable.item(3, 0).setText(nask2)
        self.HogaTable.item(4, 0).setText(nask1)
        self.HogaTable.item(10, 0).setText(nask)
        self.HogaTable.item(0, 1).setText(vask5)
        self.HogaTable.item(1, 1).setText(vask4)
        self.HogaTable.item(2, 1).setText(vask3)
        self.HogaTable.item(3, 1).setText(vask2)
        self.HogaTable.item(4, 1).setText(vask1)
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
```

해외호가 역시나 국내와 동일하게 처리해줍니다.

```ruby
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
                self.HogaTable_glb.item(0, 0).setText(nask5)
                self.HogaTable_glb.item(1, 0).setText(nask4)
                self.HogaTable_glb.item(2, 0).setText(nask3)
                self.HogaTable_glb.item(3, 0).setText(nask2)
                self.HogaTable_glb.item(4, 0).setText(nask1)
                self.HogaTable_glb.item(10, 0).setText(nask)
                self.HogaTable_glb.item(0, 1).setText(vask5)
                self.HogaTable_glb.item(1, 1).setText(vask4)
                self.HogaTable_glb.item(2, 1).setText(vask3)
                self.HogaTable_glb.item(3, 1).setText(vask2)
                self.HogaTable_glb.item(4, 1).setText(vask1)
                self.HogaTable_glb.item(10, 1).setText(vask)

                for i in range(5):
                    item = self.HogaTable_glb.item(i, 0)
                    item.setForeground(QColor("blue"))

                item = self.HogaTable_glb.item(10, 0)
                item.setForeground(QColor("blue"))

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

                for i in range(5, 11):
                    item = self.HogaTable_glb.item(i, 3)
                    item.setForeground(QColor("red"))

                item = self.HogaTable_glb.item(10, 3)
                item.setForeground(QColor("red"))

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
                        text = item.text().rstrip()  
                        item.setText(text)  
                        item.setFont(QFont('Inter', 9, QFont.Bold)) 
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter) 
```
