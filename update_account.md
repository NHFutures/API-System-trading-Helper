## 1) 5초마다 예탁자산 화면 업데이트하기

#### 이전에 스케줄러에 updateaccountinfo를 등록해서 5초마다 예탁자산이 업데이트가 될 수 있게 했습니다.
#### 아래는 updateaccountinfo 함수입니다.

```ruby
def updateAccountInfo(self):

    """계좌 정보 업데이트. 스케줄러에 등록 후 사용"""

    date_string = datetime.datetime.today().strftime('%Y%m%d')
    data_string = date_string + self.acc_no + self.encoded_pwd
    self.pySBtrader.doRequestData(-1, "sdbs5001q01", data_string, "", "")
```

## 2) 예탁자산 화면 구현하기

#### receiveData 함수 밑으로 sdbs5001q01에 대한 tr값과 recvData들이 넘어옵니다.
#### receiveData 함수 밑에 아래 처럼 코드를 작성해줍니다.

```ruby
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
```
