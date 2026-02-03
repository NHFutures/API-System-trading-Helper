# 부록

## 주야간 확인

주야간을 확인하는 방법은 python 라이브러리 중 apscheduler라는 라이브러리를 이용하여 스케줄러를 돌릴 것 입니다.

스케줄러는 백그라운드에서 실행되며 주기적으로 어떤 함수들을 실행해주는 역할을 합니다.

```ruby
from apscheduler.schedulers.background import BackgroundScheduler

...
...

self.sched = BackgroundScheduler()

...
...

self.sched.start()
self.sched.add_job(self.dayNight, 'interval', minutes=1, id='daynight')
```

스케줄러를 사용하는 방법은 아래와 같이,
```ruby
self.sched.add_job(self.dayNight, 'interval', minutes=1, id='daynight')
```

함수, ‘interval’, 1분마다, 스케줄러 이름의 순서대로 값들을 넣어주면 됩니다.

더 자세한 내용은 apscheduler 공식 [documentation](https://apscheduler.readthedocs.io/en/3.x/)을 참고하는 것이 좋습니다.

dayNight 함수는 아래와 같습니다.
```ruby
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
```

현재 시간을 가져와서 오전 6 이전이고 오후 6 이후면 야간장으로 계산합니다.

#### 그때마다 getAllStockList 함수를 호출해서 주간과 야간 종목들을 가져와야 합니다. 주간 종목들과 야간 종목들이 다를 수 있기 때문에 반드시 구분을 해서 가져와야 합니다.

보면 코드상에는 똑같이 함수를 호출하지만 getAllStockList함수 내부를 보면 주간과 야간을 구분하고 있다는 것을 알 수 있습니다. 아래는, getAllStockList 함수입니다.
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

        # 주간일 경우,
                if self.daynight == '1' and daynight == 'day':
                    stock_list.append(name)
                    stock_code_list.append(code + " (" + name + ")")
                    self.stock_rel_code_name_dict[code] = name
                    self.stock_rel_name_code_dict[name] = code
                    self.stock_rel_code_relcode_dict[code] = relcode
                    self.stock_rel_code_ctrt_size_dict[code] = ctrt_size

        # 야간일 경우,
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

## 분봉데이터 만들기

일봉을 기준으로 예를 들어 보겠습니다.
```ruby
self.doRequestData("0", "sdif7201q03", "1101T6000    000000009999999900100", '', '')
```

데이터를 요청을 합니다. 순서대로 마켓코드, tr코드, 데이터스트링입니다. API 문서를 참고하여 어떤 분봉을 가져올 것인지를 정합니다.

이후에는 connectReceiveData에서 봉데이터를 처리해줍니다.

```ruby

recvData_ = recvData.encode('euc-kr')
cnt = int(recvData_[49:53].decode('euc-kr'))
code = recvData_[25:37].decode('euc-kr').replace(' ', '')
data_body = recvData_[53:]
price_list = []
for i in range(0, cnt):
idx = i * 83
data_body_ = data_body[0 + idx : 83 + idx]

t = data_body_[0:8].decode('euc-kr').replace(' ', '')
o = data_body_[8:16].decode('euc-kr').replace(' ', '')
h = data_body_[16:24].decode('euc-kr').replace(' ', '')
l = data_body_[24:32].decode('euc-kr').replace(' ', '')
c = data_body_[32:40].decode('euc-kr').replace(' ', '')
v = data_body_[56:68].decode('euc-kr').replace(' ', '')
price_list.append([t, o, h, l, c, v])

with open("test.txt", 'w+') as f:
f.write("\n".join(",".join(i) for i in price_list))
```
파싱관련은 API 문서를 참고하셔야 합니다.
