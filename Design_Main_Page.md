## main page 디자인하기

#### login page 만들기를 참고하여 각각의 widget StyleSheet 를 변경해서 main page 디자인을 해봅니다.

  1. Tab 디자인 변경
#### 디자인을 적용할 TabWidget 을 선택 후 마우스 우 click 으로 ‘styleSheet 바꾸기’ 를 선택하여 stylSheet 창을 열어줍니다.
<img src="https://wikidocs.net/images/page/198214/1.png" width="600" height="300"/>

#### 원하는 스타일 코드를 입력합니다. hover 와 select 속성을 이용해 마우스 on,off 시, 그리고 click 여부에 따라 디자인이 바뀌도록 설정 후 ‘적용’, ‘확인’ 버튼을 눌러서 디자인을 적용합니다.
<img src="https://wikidocs.net/images/page/198214/2.png" width="400" height="600"/>

#### 참고로 부모 클래스에 적용된 디자인은 동일한 widget 형식의 자식 클래스에도 함께 적용됩니다. ( 디자인을 다르게 적용하려면 자식 클래스의 styleSheet 를 변경 해주면 됨 )

  2. ComboBox 디자인 변경
#### designer에서 만든 ComboBox는 특별히 바꿀 스타일이 없으므로 기본 스타일을 유지합니다. 대신python code 에서 따로 만든 ComboBox 는 designer의 기본 ComboBox 와 스타일이 다르기 때문에 수정을 해 줘야 하는데 designer stylSheet 에서 스타일을 적용할 수 없어 code 내에서 ‘setStyleSheet’ 함수를 이용해 스타일을 따로 적용시켜 줍니다. 이 때 기존의 ComboBox는 ‘hide’ 함수를 써 숨깁니다.
<img src="https://wikidocs.net/images/page/198214/3.png" width="1000" height="100"/>

#### 이 때 dropdown 버튼의 모양을 바꾸려면 이미지를 다운받아 아래처럼 setStyleSheet 함수 안에 클래스 명과 이미지 url 경로를 입력 후 크기를 조정해줍니다.

<img src="https://wikidocs.net/images/page/198214/4.png" width="1100" height="100"/>
<img src="https://wikidocs.net/images/page/198214/5.png" width="1100" height="100"/>

  3. SpinBox 디자인 변경
#### 디자인을 적용할 TabWidget 을 선택 후 마우스 우 click 으로 ‘styleSheet 바꾸기’ 를 선택하여 stylSheet 창을 연 뒤 원하는 스타일 코드를 입력합니다. up down 버튼의 모양을 바꾸려면 원하는 이미지를 다운받아 리소스 탐색기에 등록하고 ‘image’ 리소스로 적용시키면 됩니다. ( login page 디자인하기 참고 )

#### 전체 코드는 다음과 같습니다.
<img src="https://wikidocs.net/images/page/198214/6.png" width="900" height="400"/>

  4. PushButton 디자인 변경
#### 디자인을 적용할 PushButton 를 선택 후 마우스 우 click 으로 ‘styleSheet 바꾸기’ 를 선택하여 stylSheet 창을 열어줍니다.
<img src="https://wikidocs.net/images/page/198214/7.png" width="500" height="600"/>

#### 각각의 Button에 적용할 스타일 코드를 입력 후 ‘적용’, ‘확인’ 버튼을 눌러서 디자인을 적용합니다. hover 나 active 속성을 이용해 마우스 on,off 또는 버튼 활성화에 따라 디자인이 바뀌도록 설정합니다.
<img src="https://wikidocs.net/images/page/198214/8.png" width="500" height="600"/>

  5. tableWidget 디자인 변경
#### 디자인을 적용할 tableWidget 를 더블 click 하여 표 위젯 편집창을 엽니다. 행,열,항목의 ‘속성‘ Boutton을 click 해 textAlignment 와 background color 등을 변경할 수 있습니다. 또한 속성편집기에 있는 ‘Header’ 속성에서 HeaderVisible 을 true 또는 false 로 변경해 Header 를 보이거나 숨길 수 있고python code 에서 ‘setColumnWidth’ 함수를 사용해 각 column header 의 넓이를 조정할 수 있습니다.
#### 테이블 Header 를 디자인하려면 ‘QHeaderView::section’ 이란 속성을 수정해주면 됩니다.
#### 디자인을 적용할 tableWidget 를 선택 후 마우스 우 click 으로 ‘styleSheet 바꾸기’ 를 선택하여 stylSheet 창을 열고 QHeaderView::section 에 스타일 코드를 입력해 줍니다. ( coumn header 만 적용하려면 : horizontal 추가 )
#### 또한 행과 열 Header 가 교차하는 코너 디자인을 수정하려면 ‘QTableWidget QTableCornerButton::section’ 속성을 변경해 줍니다. 적용 예는 다음과 같습니다.

<img src="https://wikidocs.net/images/page/198214/9.png" width="1000" height="500"/>
<img src="https://wikidocs.net/images/page/198214/10.png" width="1000" height="500"/>

#### tableWidget을 반응형으로 만들고 싶다면 python code 에서 setSectionResizeMode 함수를 사용해 QHeaderView 속성을 Stretch 로 적용시키면 됩니다. ( 단, Stretch 속성은 모든 cell 을 같은 크기로 적용시키기 때문에 크기를 다르게 적용하려면 if 문을 써 다른 크기로 적용시킬 cell 을 제외시켜줘야 함 )
<img src="https://wikidocs.net/images/page/198214/11.png" width="1200" height="600"/>

  6. 실시간 데이터 color 적용 및 정렬
#### 추후 NHApi를 통해 table에 실시간으로 추가되는 데이터 item 들에 color 를 적용하려면 ‘QColor’ 모듈을 import 해서 적용시키면 됩니다. 먼저 ‘QColor’ 모듈을 import 해서 불러온 뒤 적용할 item 에 디자인할 색을 입력합니다.
#### 그리고 ‘QTableWidgetItem’ 모듈로 item을 table 에 setting 한 다음 ‘setForeground’ 함수를 이용해 원하는 color 를 item 에 적용시킵니다. ( 미리 setting 된 item 은 row 와 column 번호만 가져옴 )
#### item 들을 정렬하려면 item 을 text 로 변환해 ‘setTextAlignment’ 함수를 사용해서 ‘Qt’ 모듈에 있는 ‘Align’ 함수를 적용시켜 정렬합니다. ‘Align’ 은 좌우정렬 ( ‘AlignLeft’ 는 좌측정렬, ‘AlignRight’ 는 우측정렬 ), ‘AlignV’ 는 상하정렬 ( 중앙정렬해주는 ‘AlignVCenter’ 를 많이 사용 ) 을 할 수 있습니다. 이 때 데이터에 불필요한 공백이 있어 정렬이 제대로 안 될 때가 있는데 ‘strip’ 함수를 써 공백을 제거해 줍니다.( ‘strip’ 은 전체공백 제거, ‘rstrip’ 은 우측공백 제거, ‘lstrip’ 은 좌측공백 제거 시 사용 ) 아래는 반복문으로 table에 들어가는 모든 item에 공백을 제거하고 우측정렬하는 코드 예시입니다.

<img src="https://wikidocs.net/images/page/198214/12.png" width="1500" height="400"/>
<img src="https://wikidocs.net/images/page/198214/13.png" width="1200" height="300"/>
<img src="https://wikidocs.net/images/page/198214/14.png" width="400" height="600"/>

#### 디자인을 모두 적용한 뒤 ui 와 python code 를 저장하고 실행시켜서 error 없이 실행된다면 성공입니다.
