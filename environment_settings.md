## 1. NH API 다운로드

1. NH선물 계좌개설 및 사용등록
2. NH선물 모의 API 사용신청
    - 써핑보드(HTS) 접속 후 "[2043] API 서비스 사용등록" 에서 신청 가능
3. [NH선물 홈페이지](https://www.futures.co.kr/content/Getcontent.do?content=3000034#tab3) > 시스템트레이딩 > API > 자료실 > 하단에 모듈 다운로드
4. 모듈이 다운로드가 다 되면 C:\NH 폴더를 만들어 그 아래에 압축을 풀어줍니다.

** 컴퓨터 환경에 따라 다운로드 폴더가 변경될 수 있습니다.


## 2. Python 설치

[파이썬 홈페이지](https://www.python.org/downloads/)에서 파이썬 최신버전을 다운로드 받습니다.

## 3. vscode 설치

vscode는 개발 통합 환경 프로그램(이하 IDE툴)입니다.

자신의 PC 운영체제에 맞는 버전을 설치해줍니다.

아래는 64비트 운영체제 윈도우 다운로드 설치 페이지입니다.

## 4. OCX 등록

OCX란 윈도우에서 프로그램간 데이터 연결을 위해 작성된 규칙입니다. OCX를 등록해야만 NH에서 제공하는 함수들을 사용할 수가 있습니다.

저희는 NH에서 제공하는 SBOpenApiX.ocx를 등록해서 사용을 하게 됩니다.

아까전 C드라이브 밑에 NH 폴더에 압축을 잘 풀어두었다면 아래와 같이 경로를 입력해서 등록을 해줍니다.

#### > regsvr32 
<img src="https://wikidocs.net/images/page/197677/%EC%BA%A1%EC%B2%982.JPG" width="1200" height="600"/>

## 5. 미니콘다 등록

미니콘다란 가상환경에서 개발을 할 수 있게 해주는 툴입니다.

프로젝트를 하다보면 각각 환경이 다른데, 이처럼 가상환경에서 환경을 분리해서 개발을 해주면 편합니다.

여기서는 NH ocx 개발을 위한 환경을 만들기 위해 32bit 가상환경을 만들어 진행합니다.

[콘다 홈페이지](https://www.anaconda.com/docs/getting-started/miniconda/main) 이동 후 Window 64-bit version의 미니콘다를 클릭해서 다운 받습니다.

다운로드 받은 미니콘다 파일을 실행하면 설치를 시작할 수 있습니다.

<img src="https://wikidocs.net/images/page/197678/EB8BA4EC9AB4EBA19CEB939C.jpg" width="500" height="400"/>

다음을 계속 누르다가 아래 화면에서 멈춰줍니다. 상단 체크박스는 환경변수 설정 부분으로 체크 안해도 큰 문제는 없지만 추후 환경변수 설정을 따로 해야하는 번거로움이 있을 수 있기 때문에 체크 후 install 합니다.

<img src="https://wikidocs.net/images/page/197678/EB8BA4EC9AB4EBA19CEB939C_3.jpg" width="500" height="400"/>

계속 다음을 눌러 finish를 합니다.

검색창에 ‘Anaconda Prompt’를 입력해 설치된 ‘Anaconda Prompt’를 관리자 권한으로 실행합니다.

<img src="https://wikidocs.net/images/page/197678/EC8AA4ED81ACEBA6B0EC83B7_2023-04-06_171550.png" width="500" height="600"/>

다음과 같이 입력해서 미니콘다가 잘 설치되었는지 conda —version을 확인해 봅니다.

<img src="https://wikidocs.net/images/page/197678/EC8AA4ED81ACEBA6B0EC83B7_2023-04-06_172445.png" width="600" height="100"/>

설치가 잘 되었다면 다음과 같이 입력하여 미니콘다를 32bit 환경으로 변경해 줍니다. (국내 증권사 프로그램들은 전부 32비트를 사용) 

<img src="https://wikidocs.net/images/page/197678/EC8AA4ED81ACEBA6B0EC83B7_2023-04-06_174938.png" width="600" height="400"/>

다음과 같이 ‘conda info’를 입력해 32bit로 설정이 되었는지 확인합니다.

<img src="https://wikidocs.net/images/page/197678/EC8AA4ED81ACEBA6B0EC83B7_2023-04-06_175405.png" width="300" height="50"/>

32bit 환경설정이 되었다면 prompt에 ‘conda env list’를 입력해 아나콘다 환경을 확인해 봅니다.

<img src="https://wikidocs.net/images/page/197678/EC8AA4ED81ACEBA6B0EC83B7_2023-04-06_181940.png" width="500" height="80"/>

그러면 위와 같이 base라는 기본환경 1개만 setting이 되어 있는 걸 확인할 수 있는데 여기에 작업을 할 새로운 가상환경을 추가해 주기 위해 ‘conda create -n {가상환경명 - 임의대로 작성} python={버전}’을 입력해 줍니다.

<img src="https://wikidocs.net/images/page/197678/EC8AA4ED81ACEBA6B0EC83B7_2023-04-06_182529.png" width="550" height="50"/>

다시 ‘conda env list’를 입력해 아나콘다 환경을 확인해보면 가상환경이 추가된 것을 확인할 수가 있습니다.

<img src="https://wikidocs.net/images/page/197678/EC8AA4ED81ACEBA6B0EC83B7_2023-04-06_182946.png" width="400" height="100"/>

추가된 가상환경을 활성화 하는 명령어 ‘conda activate {가상환경명}’ 를 입력 후 (base) 표시가 ({가상환경명})으로 바뀌면 가상환경 설정이 끝납니다.

## 6. 가상환경에 패키지 설치

가상환경이 생성되었다면, 해당 가상환경을 활성화합니다.
```
conda activate py37_32
```

이제 써핑보드 API개발에 필요한 pyqt5와 apscheduler, 그리고 pysbapi를 설치하기 위해 다음과 같은 명령어를 입력합니다.
```
pip install pyqt5
pip install apscheduler
pip install pysbapi
```
위의 명령어는 PyPI (Python Package Index)에서 pyqt5와 apscheduler를 다운로드하여 설치하는 명령어입니다. 이 때, pip은 Python 패키지를 설치하고 관리하기 위한 패키지 관리자입니다.

pyqt5는 Qt 프레임워크를 Python에서 사용할 수 있도록 해주는 라이브러리로, Windows 애플리케이션 개발을 위해 사용될 수 있습니다. apscheduler는 간단한 스케쥴링 기능을 수행하는 라이브러리로, 주기적인 작업을 수행해야 하는 경우 등에 사용될 수 있습니다.

pysbapi는 써핑보드 API를 쉽게 사용할 수 있게 해주는 라이브러리입니다.

아래는 pyqt5와 apscheduler가 설치되었으므로, 해당 라이브러리를 사용하여 간단한 프로그램을 작성한 예시입니다.

```
from PyQt5.QtWidgets import QApplication, QLabel
from apscheduler.schedulers.background import BackgroundScheduler

def task():
    print("Task is executed")

if __name__ == '__main__':
    app = QApplication([])
    label = QLabel("Hello World!")
    label.show()

    scheduler = BackgroundScheduler()
    scheduler.add_job(task, 'interval', seconds=3)
    scheduler.start()

    app.exec_()
```

해당 프로그램은 PyQt5를 사용하여 "Hello World!"라는 텍스트를 보여주는 창을 생성하고, apscheduler를 이용하여 3초마다 task() 함수를 실행하는 예제입니다. BackgroundScheduler()는 백그라운드에서 스케쥴링을 수행할 수 있도록 도와주며, add_job() 함수를 이용하여 수행할 작업과 주기를 설정할 수 있습니다.

최종적으로, 해당 프로그램을 실행하면 "Hello World!" 텍스트가 보이며, 3초마다 "Task is executed"라는 메시지가 출력됩니다.

이처럼 Anaconda 가상환경 py37_32에서 pyqt5와 apscheduler를 설치하고 활용하는 방법에 대해 알아보았습니다. 이를 활용하여 데이터 분석, 머신러닝과 같은 작업에서 PyQt5와 apscheduler가 제공하는 기능들을 활용할 수 있습니다.

## 7. 디자인 툴 설치

python에서 프로그램의 UI 작업을 하게 해주는 Qt Designer를 설치해보겠습니다.

가상환경을 열어서 아래 패키지를 설치해줍니다.
```
pip install pyside2
```
설치 후 아래 코드를 입력하여, 가상환경의 경로를 찾습니다.
```
conda info
```
<img src="https://wikidocs.net/images/page/197801/Untitled.png" width="300" height="50"/>
<img src="https://wikidocs.net/images/page/197801/ECBD98EB8BA42.png" width="900" height="500"/>
찾고나서 파일탐색기 경로에 pyside2를 붙여서 입력해줍니다.

<img src="https://wikidocs.net/images/page/197801/EC9584EB8298ECBD98EB8BA41_1.png" width="600" height="350"/>

그러면 designer라는 파일이 보이는데요. 바로가기 생성을 해서 바탕화면에 놓아주시면 준비가 끝납니다.

<img src="https://wikidocs.net/images/page/197801/EC8AA4ED81ACEBA6B0EC83B7_2023-04-07_183210.png" width="900" height="500"/>

디자이너의 사용법은 2장에서 자세하게 다루겠습니다.

## 8. vscode 환경설정

개발 하기에 앞서 vscode는 항상 관리자 권한으로 켜주어야 합니다.

그리고 작업할 폴더를 생성합니다.

<img src="https://wikidocs.net/images/page/197804/EC8AA4ED81ACEBA6B0EC83B7_2023-04-07_095444.png" width="700" height="200"/>

vscode 우측 하단 상태표시줄에서 인터프리터 부분을 클릭합니다.

<img src="https://wikidocs.net/images/page/197804/EC8AA4ED81ACEBA6B0EC83B7_2023-04-07_095958.png" width="600" height="90"/>

상단부에 열린 인터프리터 선택 창에서 설정했던 32bit 가상환경을 선택합니다.

<img src="https://wikidocs.net/images/page/197804/EC8AA4ED81ACEBA6B0EC83B7_2023-04-07_100114.png" width="600" height="200"/>

인터프리터가 변환된 걸 확인할 수 있습니다.

<img src="https://wikidocs.net/images/page/197804/EC8AA4ED81ACEBA6B0EC83B7_2023-04-07_100311.png" width="500" height="50"/>

이처럼 윈도우 운영체제가 64bit이여도 임의로 만든 32bit 가상환경에서 우리는 python 프로그램을 실행시킬 수 있습니다.
