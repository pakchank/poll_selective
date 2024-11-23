# <여론M>에서 추출한 테이블의 링크를 이용해 중앙선거여론조사심의위원회 사이트로부터 각 조사의 수행기관, 조사의뢰자 등 메타데이터를 스크래이핑하는 코드입니다.

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

df = pd.read_csv("from_mbc.csv")
ids = 'ID' #'뉴스식별자'
link = '조사기관' #'URL'

headers = {'accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53',
           'Accept-Language': 'en-US,en;q=0.9,it;q=0.8,es;q=0.7',
           'referer': 'https://www.google.com/'}

def main():
    global df
    
    df = df.reindex(columns=[*df.columns.tolist(), '등록번호', '선거여론조사기관', '조사의뢰자', '조사방법new', '표본추출틀',
                        '표본크기', '응답률new', '접촉률', '표본오차','공표일시'], fill_value=0)

    df['조사방법new'] = df['조사방법new'].astype('object')
    df['표본추출틀'] = df['표본추출틀'].astype('object')

    for index, row in df.iterrows():
        ID = row[ids]
        url = row[link]
    
        res = requests.get(url, headers=headers)     
        
        if res.status_code == 200:
            print("ID " + str(index) + " request succeeded!")

        html_text = res.text
        soup = BeautifulSoup(html_text, 'html.parser')            
                    
        reg_id = soup.find(text=re.compile('등록 글번호')).parent.parent.find("td").text
        reg_org = soup.find(text=re.compile('조사기관명')).parent.parent.find("td").text
        reg_org_co = soup.find(text=re.compile('공동조사기관명')).parent.parent.find("td").text
        
        org_list = re.sub('\s+', '', reg_org) + ',' + re.sub('\s+', '', reg_org_co)
        print(org_list)

        reg_req = soup.find(text=re.compile('조사의뢰자')).parent.parent.find("td").text
        reg_methods = soup.find_all('th', {"class": "number"}) 

        reg_methods_list = []
        for reg_method in reg_methods:
            reg_method_parent = reg_method.parent
            if reg_method_parent.find('td').text != '':
                reg_method_name = reg_method_parent.find('td').text
                reg_method_prop = reg_method_parent.parent.find_all('tr')[1].text
                reg_methods_list.append([reg_method_name, re.sub('\s+', '', reg_method_prop)])
            else:
                pass

        sample_frame_list = []
        for i in range(len(reg_methods_list)):
            div_set = soup.find('div', {"class":"set"+str(i+1)})
            frame = div_set.find_all('table')[3].find('tbody').find_all('tr')[0].find('td').text
            sample_frame_list.append(re.sub('\s+', '', frame))

        reg_num = soup.find(text=re.compile('접촉 후 응답완료 사례수 \(I\) 합계')).parent.parent.find("td").text  
        reg_res = soup.find('th', text=re.compile('전체 응답률')).parent.find("td").text
        reg_con = soup.find('th', text=re.compile('전체 접촉률')).parent.find("td").text
        reg_se = soup.find('th', text=re.compile('표본오차')).parent.find("td").text
        date_announced = soup.find('th', text=re.compile('최초 공표·보도 지정일시')).parent.find("td").text

        tag_list = [reg_id, 
                    reg_req, 
                    reg_num, 
                    re.sub('\s+', '', reg_res), re.sub('\s+', '', reg_con), re.sub('\s+', '', reg_se), date_announced]

        df.loc[index, ['등록번호', 
                   '조사의뢰자', 
                        '표본크기', '응답률new', '접촉률', '표본오차','공표일시']] = tag_list  
        
        df.at[index, '선거여론조사기관'] = org_list
        df.at[index, '조사방법new'] = reg_methods_list
        df.at[index, '표본추출틀'] = sample_frame_list    
        

    df.to_csv("nesdc_scraped.csv")

if __name__ == '__main__':
    main()
