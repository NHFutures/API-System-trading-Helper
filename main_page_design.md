## main page 만들기

#### login page 만들기 와 동일하게 Qt Designer를 실행한 다음 "Main Window"를 선택하고 ‘생성’ 버튼을 click 합니다.
#### 생성된 mainwindow page에 먼저 ‘Tab Widget’을 click,drag해 배치시킵니다.
<img src="https://wikidocs.net/images/page/198202/1.png" width="600" height="500"/>



#### 위젯 상자에서 "Grid Layout" 을 click 하여 생성된 Tab Widget으로 drag 해 반응형 page 형식을 만들준비를 합니다. ( tab1 과 tab2에 동일하게 두번 실행 )
<img src="https://wikidocs.net/images/page/198202/2.png" width="900" height="500"/>



#### 그런데 login page를 만들 때와 다르게 layout이 화면에 꽉 차지 않음을 볼 수 있습니다. 
#### 이유는 Tab Widget을 처음 page에 배치하면 grid 속성이 잠겨있기 때문인데 레이아웃 효과를 이용하려면 객체탐색기에서 풀어줘야 합니다.
<img src="https://wikidocs.net/images/page/198202/3.png" width="600" height="500"/>


#### 먼저 잠겨있는 tab 객체를 click 하고 designer 상단 탭바에 있는 ‘레이아웃 풀기’ 아이콘을 click합니다.
#### 그렇게 되면 ‘tabWidget’ 상부에 있는 ‘centralWidget’의 grid 속성이 잠기게 되는데 ‘centralWidget’을 click 후 마찬가지로 ‘레이아웃 풀기’를 click 해 해제합니다.
#### 그런 뒤 ‘tabWidget’을 click하여 ‘레이아웃 풀기’ 아이콘 앞에 위치하는 layout 중 원하는 아이콘을 클릭해 주면 tab 잠김이 풀리고 tabWiget 안의 layout이 login page 처럼 위치합니다.( tab2도 동일하게 진행 )
<img src="https://wikidocs.net/images/page/198202/4.png" width="900" height="600"/>



#### 그 뒤 login page와 마찬가지로 margin을 제거해 mainwindow에 일치시킵니다.( 단, 여기선 ‘centralWidget’, ‘ tab ‘ 두 객체의 margin을 모두 제거 )
#### 그 다음 각각의 layout과 widget을 추가해 화면을 4분할 하여 화면을 완성합니다. ( 해외선물 tab도 동일 )
<img src="https://wikidocs.net/images/page/198202/5.png" width="900" height="600"/>



#### tabBar name과 객체명도 변경해줍니다. ( tabBar name은 tab 속성에서 ‘currentTabText’ 변경 )
<img src="https://wikidocs.net/images/page/198202/6.png" width="600" height="500"/>


#### 각각의 section을 구성하는 방법을 간략히 설명하면 다음과 같습니다.
  1. 종목 추가 table section
  <img src="https://wikidocs.net/images/page/198202/7.png" width="600" height="500"/>

##### 국내외 선물 종목을 보여주는 곳으로 ‘Vertica Layout’ 안에 ‘Horizontal Layout’과 ‘Grid Layout’ 을 위 아래로 drag하여 배치하고 ‘ComboBox’와 ‘Push Button’ , ’Table Widget’ 을 drag하여 종목을 추가,삭제할 수 있습니다. ‘ComboBox’의 item name과 ’TableWidget’ 의 column name 은 해당 widget을 더블 click해서 변경할 수 있습니다.

  2. 상태창 section
 <img src="https://wikidocs.net/images/page/198202/10.png" width="600" height="300"/>

##### ‘Grid Layout’ 안에 ‘TextEdit’를 을 drag하여 page에서 이루어지는 event 내용을 update 할 수 있습니다.

  3. 계좌 정보 table section
  <img src="https://wikidocs.net/images/page/198202/8.png" width="600" height="500"/>

##### 내 계좌정보를 불러와서 실시간으로 보여주는 곳으로 다음과 같이 만듭니다.
##### ‘Grid Layout’ 안에 ‘Label’과 ‘Horizontal Layout’ , ‘Tab Widget’ 을 차래대로 배치합니다.
##### ‘Horizontal Layout’ 안에는 ‘ComboBox’와 ‘LineEdit’ , ‘Push Button’ 을 배치합니다.

##### 💡 이 때 계좌비밀번호 입력 “LineEdit” 속성에서 “placeholerText” 이름을 바꿔주면 inputbox 안에 내용이 생성됩니다.
##### Tab Widget’은 tabBar부분에서 우 click 하여 ‘쪽 삽입’ 을 선택해 tabBar를 하나 더 추가한 뒤 tab 속성에서 각 tabBar name을 변경하고

  4. 매수,매도 및 link Button section
  <img src="https://wikidocs.net/images/page/198202/9.png" width="1400" height="500"/>


##### 선물 종목을 구매하고 여러 정보들을 볼 수 있는 page로 이동하는 link button을 모아논 곳으로 다음과 같이 만듭니다.
##### ‘Vertica Layout’ 안에 ‘Horizontal Layout’ 6줄을 배치하고 첫 줄에 ‘Label’ 3개를 배치하고
##### 두번째 줄에 ‘ComboBox’, ‘SpinBox’ , ‘LinEdit’를 배치해 종목, 수량, 금액을 입력할 input 부분을 만듭니다.


##### 세번째 줄에 다시 ‘Label’ 1개를 배치하고 네번째 줄에 ‘ComboBox’ 2개, ‘PushButton’ 2개를 배치한 다음
##### 다섯번째 줄에 ‘Widget’ 또는 ‘Horizontal Spacer’ ( 개인적으론 ‘Widget’ 배치함 ), ‘PushButton’ 2개를 추가로 배치합니다.
##### (둘 중 택 1)

##### 마지막 줄에는 ‘GroupBox’를 매치하고 그 안에 ‘PushButton’ 4개를 배치합니다.
##### 모두 배치를 마쳤으면 margin 과 widget name 들을 수정합니다.

##### 모든 작업이 끝났다면 "메뉴바"에서 "파일" 을 선택하여 "저장" 을 click하거나 “ctrl + s” key를 눌러 .ui 파일을 저장합니다. ( 파일명 : main_View.ui )
##### 완성 후 미리보기를 실행, window 실행화면을 확인합니다. ( login page 만들기 참고 )
