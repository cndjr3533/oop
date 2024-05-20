import json
import requests
from myutil import clear_screen, where


class NewsConfig: 
    def __init__(self, config_file:str):      
      try:
        with open(config_file, 'r') as f:
          config = json.load(f)
          self.__base_url = config['base_url']
          self.__api_key = config['api_key']
          self.__category = config['category']
          self.__language = config['language']
          result = True        
      except Exception as e:
        print(f'Error: {e}')
        raise Exception(f'Error: {e}')      
    
    def __repr__(self) -> str:
       return f'NewsView({self.__base_url}, {self.__api_key}, {self.__category}, {self.__language})'
     
    def get_language(self) -> iter:
        return self.__language
      
    def get_lang_code(self, i:int) -> str:
        return self.__language[i]['code'].lower()
      
    def get_categories(self) -> iter:
        return self.__category
    
    def get_category(self, i:int) -> str:
        return self.__category[i]
      
    def get_api_key(self) -> str:
        return self.__api_key
      
    def get_base_url(self) -> str:
        return self.__base_url
      

class NewsLoader:  
  def __init__(self) -> None:
    self.status = 'not yet'    
    self.total_results = 0
    self.articles = []
    self.pages = 0
    self.vpp = 20
    
  def load_news_from_url(self, url:str):
    try:
      response = requests.get(url)
      news_json = response.json()
      
      if news_json['status'] != 'ok':
        raise Exception('Error: Unable to load news')
      
      self.articles += news_json['articles']      
      self.status = news_json['status']
      self.total_results = int(news_json['totalResults'])            
      self.remove_quotes()
    except Exception as e:
      print(f'Error: {e}')
      raise Exception(f'Error: {e}')
  
  def remove_quotes(self) -> str:
    chk = lambda x: x is not None #is not none 해서 끝났으니까 x ,들어온값이 non 이면 false, none이 아니면 true
    for article in self.articles:
      article['title'] = where(chk(article['title']), article['title'], '').replace('"', '')
      article['description'] = where(chk(article['description']), article['description'], '').replace('"', '')
      article['author'] = where(chk(article['author']), article['author'], '').replace('"', '')
      article['source']['name'] = where(chk(article['source']['name']), article['source']['name'], '').replace('"', '')
  
  def load_news(self, base_url:str, api_key:str, lang:str, category:str, vpp:int=20):
    try:
      url = f'{base_url}?country={lang}'
      if category.lower() != 'topic':
        url += f'&category={category}'
        
      url += f'&apiKey={api_key}'
          
      self.load_news_from_url(url)     #최종적으로 호출하는 url
      
      self.vpp = vpp      
      self.__calculate_total_pages()
      
      for i in range(2, self.pages+1):
        page_url = url + f'&page={i}' 
        self.load_news_from_url(page_url)
        
    except Exception as e:
      print(f'Error: {e}')
      raise Exception(f'Error: {e}')    
  
  def get_total_results(self) -> int:
    return self.total_results
  
  def __calculate_total_pages(self):
    if self.vpp == 0:
      return
    
    self.pages = self.total_results // self.vpp + 1
    
  def get_page(self, page:int) -> iter:
    start = (page-1) * self.vpp
    end = start + self.vpp
    return self.articles[start:end] if end < self.total_results else self.articles[start:]
  
  
   
   





if __name__ == "__main__":
    news_conf = NewsConfig('config.json')    
    # print(news)
    clear_screen()
    for i, lang in enumerate(news_conf.get_language()) :
        print(f'{i+1} : {lang["code"]}, {lang["name"]}')    
    
    sel = int(input('Select language: '))
    lang_code = news_conf.get_lang_code(sel-1)
    clear_screen()
        
    for i, cat in enumerate(news_conf.get_categories()) :
        print(f'{i+1} : {cat}')
        
    sel = int(input('Select category: '))
    category = news_conf.get_category(sel-1)
    
    clear_screen()
    print(f'You selected: {lang_code}')
    print(f'You selected: {category}')    
    
    news_loader = NewsLoader()
    news_loader.load_news(news_conf.get_base_url(), 
                          news_conf.get_api_key(), 
                          lang_code, 
                          category)
    
    print(f'Total results: {news_loader.get_total_results()}')
    print()
    print(f'Number of articles: {len(news_loader.articles)}')
    print()
    
    for i, article in enumerate(news_loader.articles):
      print('-----------------------------------')
      print(f'Article {i+1}')
      print(f'Title: {article["title"]}')
      print(f'Description: {article["description"]}')
      print(f'URL: {article["url"]}')
      print(f'UrlToImage: {article["urlToImage"]}')
      print(f'Published at: {article["publishedAt"]}')
      print(f'Author: {article["author"]}')
      print(f'Source: {article["source"]["name"]}')
        
    
    
