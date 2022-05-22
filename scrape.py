from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By


class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
      self.visited.clear()
      self.dfs_visit(node)
        # 2. start recursive search by calling dfs_visit

    def dfs_visit(self, node):
      if node in self.visited :
        return
      self.visited.add(node)
      self.order.append(node)
      for x in self.go(node):
        self.dfs_visit(x)

    def bfs_search(self,node) :
      self.visited.clear()
      self.bfs_visit(node)

    def bfs_visit(self,node) :
        queue = []
        queue.append(node)
        while len(queue) > 0:
            print(queue)
            curr = queue.pop(0)
            if curr in self.visited :
              continue
            self.order.append(curr)
            self.visited.add(curr)
            for child in self.go(node):
                if not child in self.visited:
                  queue.append(child)
          

class WebSearcher(GraphSearcher) :
    def __init__(self,driver) :
        self.driver = driver
        self.tab =pd.DataFrame({})
        super().__init__()

    def go(self,node) :
        self.driver.get(url=node)
        links = self.driver.find_elements(by=By.TAG_NAME, value="a")
        link=[]
        for l in links :
            link.append(l.get_property("href"))
        return link
    def table(self) :
      ord = self.order
      # print(ord)
      for x in ord :
        try :
          self.driver.get(url=x)
          # print(x)
          tab = self.driver.find_element(by=By.TAG_NAME,value="table")
          tab=tab.get_attribute('outerHTML')
          table =pd.read_html(tab,index_col=None)
          table=pd.DataFrame(table[0],index=None)
          # print(table)
          # self.table = pd.concat([self.table,pd.read_html(tab)])
        except NoSuchElementException :
            pass

      return self.tab


options = Options()
options.headless = True
service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(options=options, service=service)

ws = WebSearcher(driver)
print(ws.go("http://192.168.1.153:5000/Node_1.html")) 
ws.bfs_search("http://192.168.1.153:5000/Node_1.html")
print(ws.table())
driver.close()