import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service as ChromeService

BASE_URL = 'https://realpython.com'
PATH_TO_LINKS = './posts/links.txt'

#отримання ссилок і мепінг в массив
with open(PATH_TO_LINKS, 'r') as f:
  links = f.read().split("\n")
  if(len(links)):

    def getUnique(array): 
      def filter_func(item):
        if len(item): return True;
        else: return False;
      return filter(filter_func, array)
    
    uniqueLinks = list(getUnique(links));

    print(uniqueLinks)
    print(f'Successfully parsed links from ' + PATH_TO_LINKS + '... Please wait...');
  elif not len(f) :
    print('Theres no links')
  else:
    print('Some error occured')