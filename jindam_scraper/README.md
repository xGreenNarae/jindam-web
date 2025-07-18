1.
python 이 깔려있어야 한다.

2.
jindam_scraper 디렉토리에서 아래를 실행한다.
원하는 기사링크를 입력으로 준다.
python ./main.py https://www.jindam.news/news/articleView.html\?idxno\=179

3.
output 디렉토리 안에 index.md 가 생성되고 이것을 그대로 article 디렉토리 생성해서 넣으면된다.

4.
사진은 반드시 순서대로 1.jpg, 2.jpg .. 로 article 디렉토리에 다운받아넣어준다.

5.
index.md 에서 figure 태그(사진) 있는곳에 figure caption 영역의 텍스트가 꼭
바로 이전에 중복해서 한번씩 입력되어있으므로 이건 수동으로 제거해줘야 한다.

6. 
이외에도 원본 내용중 누락된거나 틀린거 있는지 눈으로 확인하도록 한다.

