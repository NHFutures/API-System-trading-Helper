## 종목 받아오기

#### main.py 프로그램이 실행되면 (메인 화면이 로딩이 될때) 종목들을 전부 불러옵니다.
#### 종목들은 sfile03.dat파일 아래에서 API문서에 나와져 있는대로 파싱을 하면 됩니다.

```ruby
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
```
