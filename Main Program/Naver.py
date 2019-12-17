import requests, io, datetime, time
import Module
import xml.etree.ElementTree


class Naver(Module.Module):
    module_name = 'Naver'
    data = []
    def __init__(self):
        pass
    def get(self):
        url = "https://datalab.naver.com/keyword/realtimeList.naver?where=main"
        headers = {}

        headers['Content-Type'] = 'text/plain'
        headers['User-Agent'] = 'PostmanRuntime/7.20.1'
        headers['Accept'] = '*/*'
        headers['Cache-Control'] = 'no-cache'
        headers['Host'] = 'datalab.naver.com'
        headers['Accept-Encoding'] = 'gzip, deflate'
        headers['Connection'] = 'keep-alive'
        res = requests.get(url, headers=headers)
        
        
        data = res.content.decode('utf-8')
        common = '<span class="item_title">'
        self.data = []
        for _ in range(20):
            target = '<span class="item_num">%d</span>' % (_ + 1)
            s = data[data.find(target) + len(target):]
            s = s[:s.find('</span>')]
            s = s[s.find(common) + len(common):].strip()
            
            self.data.append(s)
        #print(res.content)
        
    def state(self):
        print('<%s>' % self.module_name)

print('Module, Naver is Loaded')

if __name__ == '__main__':
    n = Naver()
    n.get()
    
