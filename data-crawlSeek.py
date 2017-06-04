#coding:utf-8
import requests
import time
import re
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

job_url = []


def get_job(url):
    html = requests.get(url)
    res = re.findall('"url":"(.*?)"}', html.text)
    for i in res:
        if len(i) < 50:
            job_url.append(i)
#line 13 to line 18 open hyperlink in provided URL

def get_info(url):
    html = requests.get(url)
    jobtitle = re.findall('"title":"(.*?)",', html.text,re.S)[0]#crawl job title
    copname = re.findall('"name":"(.*?)"}', html.text)[0]#crawl company name
    salary = re.findall('"salary":"(.*?)"', html.text)#crawl salary
    if len(salary) == 0:
        salary = ''#if the posted advertise do not mention about salary, leave blank
    else:
        salary=salary[0]
    worktype = re.findall('"workType":"(.*?)"', html.text)#crawl work type (full time/part time)
    if len(worktype) == 0:
        worktype = ''#if the posted advertise do not mention about work type, leave blank
    else:
        worktype=worktype[0]
    eee = re.findall('<div class="templatetext">(.*?)</div>', html.text, re.S)
    if len(eee)==0:
        eee = re.findall('<div style="text-align:left">(.*?)</div>', html.text, re.S)
    txt = re.sub('<[^>]*>', '', eee[0]).replace("\n", "")#crawl all the detail information about the job provided by the advertiser
    csvwriter.writerow((jobtitle.encode(),copname.encode(),salary.encode(),worktype.encode(),txt.encode()))#write onto csv file


if __name__ == '__main__':
    for page in range(1, 245):
        url = url = 'https://www.seek.com.au/IT-jobs/in-All-Brisbane-QLD?page={}'.format(page)#search result of Brisbane IT related jobs
        get_job(url)
        print(url)
    datacsv = open('result.csv','wb')
    csvwriter = csv.writer(datacsv)
    csvwriter.writerow(('jobtitle','company name','salary','worktype','txt'))#first lane of the csv file, explain rows
    for url in job_url:
        print(url)
        try:
            get_info(url)
        except:
            pass
        time.sleep(1)
    datacsv.close()
