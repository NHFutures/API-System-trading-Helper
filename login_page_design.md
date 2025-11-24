## login page 만들기

#### Qt Designer를 실행한 다음 "Main Window"를 선택하고 ‘생성’ 버튼을 click 합니다.
<img src="https://wikidocs.net/images/page/198201/1.png" width="600" height="600"/>



#### 위젯 상자에서 "Grid Layout" 을 click 하여 생성된 MainWindow로 drag 해 반응형 page 형식을 만들어 줍니다.
<img src="https://wikidocs.net/images/page/198201/2.png" width="900" height="600"/>



#### 이 때 margin이 있어서 Layout 바깥쪽으로 공백이 보이는데 이 margin을 없애려면 Designer 창 오른쪽 중간에 있는 속성 편집기에 ‘margin’을 검색해 layout 속성에 있는 margin 값을 0으로 만들어줘야 합니다.
<img src="https://wikidocs.net/images/page/198201/3.png" width="600" height="800"/>


#### 0으로 수정하면 page와 layout이 빈틈없이 일치하는 것을 확인할 수 있습니다.
#### "Vertical Layout"을 click 하여 drag 해 추가한 다음 margin 값을 조정해 page가운데로 위치 시킵니다.
<img src="https://wikidocs.net/images/page/198201/4.png" width="1200" height="600"/>



#### "Vertical Layout"을 두 번 drag 하여 가운데 위치한 "Vertical Layout" 안에 위, 아래로 추가하고 layout 속성을 조정해 적당히 배치합니다.
<img src="https://wikidocs.net/images/page/198201/5.png" width="1500" height="600"/>


#### "Label"을 click, drag 하여 상단 layout 에 title 레이블을 만듭니다.
#### "Horizontal Layout" 와 "Vertical Layout" 을 click, drag 하여 하단 layout 안에 각각 위치 시킵니다.
<img src="https://wikidocs.net/images/page/198201/6.png" width="600" height="800"/>


#### "Radio Button" 을 click, drag 하여 "Horizontal Layout" 에 “실전” 과 ”모의” button을 만듭니다.
<img src="https://wikidocs.net/images/page/198201/7.png" width="600" height="50"/>


#### “Line Edit” 을 click, drag 하여 각각 “ID”, ”Password” , ”CERT” 를 입력할 inputbox를 생성하고 "Push Button"을 click, drag 하여 "로그인" 버튼을 추가합니다.
#### 💡 이 때 각각의 “LineEdit” 속성에서 “placeholerText” 이름을 바꿔주면 inputbox 안에 내용이 생성됩니다.
<img src="https://wikidocs.net/images/page/198201/8.png" width="600" height="800"/>


#### 추가로 layout 속성들을 수정해서 최종 완성합니다.
<img src="https://wikidocs.net/images/page/198201/9.png" width="600" height="500"/>


#### 완성 후에는 각 Widget 별로 객체 name을 바꿔줘야 하는데 원하는 naming을 해도 되지만 되도록 중복되는 name이 없어야 추후 유지,보수 작업이 원할하게 이루어질 수 있습니다.
<img src="https://wikidocs.net/images/page/198201/10.png" width="900" height="400"/>


#### 모든 작업이 끝났다면 "메뉴바"에서 "파일" 을 선택하여 "저장" 을 click하거나 “ctrl + s” key를 눌러 .ui 파일을 저장합니다.
#### 저장 후 "메뉴바"에서 “폼” 메뉴에 “미리보기” 를 선택해 window 실행 시의 login page를 미리 확인할 수 있습니다.

