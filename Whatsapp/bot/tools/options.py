from selenium import webdriver

opts = webdriver.ChromeOptions()
opts.add_argument('lang=pt-br')
opts.add_argument('--no-sandbox')
#opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('headless')
opts.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36")