from newsview import NewsConfig, NewsLoader
from myutil import clear_screen
import datetime


class NewsToHtml:
    def __init__(self, country_name:str='Korea', category:str='topic') -> None: #1번 생성자, 2,3번 매개변수
        self.html_top = f'''
        <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">      
  <link rel="stylesheet" href="style.css">
  <title>Document</title>
</head>
<body>
  <div class="country">
    <div>
      <img src="resources/kr.svg" alt="">
    </div>
    <div class="country_name">
      <h1>South Korea</h1>
      <h3>Category</h3>
    </div>
  </div>
  <div class="articles">

        self.html_bottom = f'''
        </div>  <!-- articles -->
  
        </body>
        </html>'''
        
        self.html_mid = ''

    def add_article(self, image_url, url, title, desc, author, date): 
        self.html_mid += f'''    
        <div class="article">
                        
      <div class="news_image">
        <img src="{image_url}" alt="">
      </div> <!-- news_image -->
      
      <div class="news_block"> #css에 news_block이라는 이름이 있는것을 이 위치에 박아넣는다
        <div class="news_title"><a href="{url}">{title}</a></div>
        <div class="news_desc">{desc}</div>
        <div class="news_author">{author}</div>
        <div class="news_date">{date}</div>    
      </div>  <!-- news_block --> #<!-- html 에서 주석

    </div>  <!-- article -->
    '''
    
    def save(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f: #파일오픈은 항상 with open , w는저장
                f.write(self.html_top)
                f.write(self.html_mid)
                f.write(self.html_bottom)
        except Exception as e: 
            print(f'Error: {e}')
            raise Exception(f'Error: {e}') #에러를 발생시켜위로 올려버리는것
        

if __name__ == '__main__':
    conf = NewsConfig('config.json') #api 내껄로 변경해야함
    news_loader = NewsLoader()

    clear_screen()
    for i, lang in enumerate(conf.get_language()): #소괄호 해놔야 ㅎ함수 호출
        print(f'{i+1} : {lang["code"]},{lang["name"]}')

    sel = int(input('Select Language : '))
    lang_code = conf.get_lang_code(sel-1)
    lang_name = conf.get_language()[sel-1]["name"] #얘가 반환해주는게 리스트 거기서 인덱싱해오니까 딕셔너리, 거기서 키값 "name"을가져오는뜻


    clear_screen()
    for i, cate in enumerate(conf.get_categories()):  #enumerate 리스트로 나열 그렇기에 앞에 변수를 여러개 작성가능
        print(f'{i+1}: {cate}')

    sel = int(input('Select Category : '))
    category = conf.get_category(sel-1)
    

    news_loader.load_news(conf.get_base_url(),
                          conf.get_api_key(),
                          lang_code,
                          category)
    
    news_html = NewsToHtml(lang_name, category)
    for article in news_loader.articles:
        news_html.add_article(article['urlToImage'],
                              article['url'],
                              article['title'],
                              article['description'],
                              article['author'],
                              article['publishedAt'])
    now = datetime.datetime.now()
    current_datetime = now.strftime("%Y%m%d_%H%M%S") #문자열로 만들어진것
    html_filename = f'{lang_code}_{category}_{current_datetime}.himl'
    news_html.save(html_filename)

    print(f'HTML file saved as {html_filename}')