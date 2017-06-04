#coding:utf-8
import requests
import time
import re
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

job_url = [] #create a list for jobs URL


def get_job(url):
    html = requests.get(url)
    res = re.findall('"url":"(.*?)"}', html.text)
    for i in res:
        if len(i) < 50:
            job_url.append(i)


def get_info(url):
    html = requests.get(url)
    jobtitle = re.findall('"title":"(.*?)",', html.text,re.S)[0]
    copname = re.findall('"name":"(.*?)"}', html.text)[0]
    salary = re.findall('"salary":"(.*?)"', html.text)
    if len(salary) == 0:
        salary = ''
    else:
        salary=salary[0]
    worktype = re.findall('"workType":"(.*?)"', html.text)
    if len(worktype) == 0:
        worktype = ''
    else:
        worktype=worktype[0]
    eee = re.findall('<div class="templatetext">(.*?)</div>', html.text, re.S)
    if len(eee)==0:
        eee = re.findall('<div style="text-align:left">(.*?)</div>', html.text, re.S)
    txt = re.sub('<[^>]*>', '', eee[0]).replace("\n", "")
    csvwriter.writerow((jobtitle.encode(),copname.encode(),salary.encode(),worktype.encode(),txt.encode()))


if __name__ == '__main__':
    for page in range(1, 245):
        url = url = 'https://www.seek.com.au/IT-jobs/in-All-Brisbane-QLD?page={}'.format(page)
        get_job(url)
        print(url)
    datacsv = open('result.csv','wb')
    csvwriter = csv.writer(datacsv)
    csvwriter.writerow(('jobtitle','company name','salary','worktype','txt'))
    for url in job_url:
        print(url)
        try:
            get_info(url)
        except:
            pass
        time.sleep(1)
    datacsv.close()
