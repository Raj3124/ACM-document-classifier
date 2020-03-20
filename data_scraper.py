from bs4 import BeautifulSoup
import re

import requests
import time,codecs
list1=[]
abstract_2=''
list_label=['CHI','CIKM', 'WWW', 'KDD', 'SIGIR', 'SIGGRAPH','CSE']
for j in range(5):
    url1='https://dl.acm.org/results.cfm?query=CHI&start='+str(j*20)+'&filtered=&within=recurringEvents%2ErecurringEventID%3DRE151&dte=&bfr=&srt=%5Fscore'
#https://dl.acm.org/results.cfm?query=CHI&start=0&filtered=&within=recurringEvents%2ErecurringEventID%3DRE151&dte=&bfr=&srt=%5Fscore
    print(url1)
    for i in range(5):  # try 5 times
        try:
            # use the browser to access the url
            response = requests.get(url1, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
            html = response.content  # get the html
            break  # we got the file, break the loop
        except Exception as e:  # browser.open() threw an exception, the attempt to get the response failed
            print('failed attempt', i)
            time.sleep(2)  # wait 2 secs


    soup = BeautifulSoup(html.decode('utf-8','ignore'),'html5lib') # parse the html
    reviews = soup.findAll('div', {
                'class':'details'})
    for review in reviews:
        titlechunck = review.find('div', {'class': 'title'})
        idchunck = str(titlechunck)
        idchunck=idchunck.split('id=')[1]
        idchunck=idchunck.split('" target')[0]
        # idchunck = re.sub('[^0-9]', '', idchunck)
        if len(idchunck)>7:
            print(idchunck)
            print(url1)
            print(review)
        list1.append(idchunck)

print(list1)
print(len(list1))
fw=open('reviews.txt','w',encoding='utf-8') # output file
#
for i in range(len(list1)): # for each page

    print ('id',list1[i])
    html=None
    pageLink='https://dl.acm.org/citation.cfm?id='+list1[i]+"&amp;preflayout=flat" # url for page 1

    for i in range(5): # try 5 times
        try:
            #use the browser to access the url
            response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
            html=response.content # get the html
            break # we got the file, break the loop
        except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
            print ('failed attempt',i)
            time.sleep(2) # wait 2 secs


    # if not html:continue # couldnt get the page, ignore

    soup = BeautifulSoup(html.decode('utf-8','ignore'),'html5lib') # parse the html
    soup_1 = soup.findAll('a', {'title': 'Conference Website'})
    if soup_1:
        for soup_2 in soup_1:
            if soup_2: label = soup_2.text.strip()
        label = label.split(' ')[0]
    if not (label in list_label): print('not specified label');continue

    review = soup.find('div', {'id': re.compile('divmain')})  # get all the review divs
    authors = ''
    institutions = ''
    date, title, abstract_1 = 'NA', 'NA', 'NA'  # initialize critic and text

    titlechunck = review.find('h1', {'class': 'mediumb-text'})
    if titlechunck: title = titlechunck.text.strip()  # .encode('ascii','ignore')

    authorchunks = review.findAll('a', {'title': re.compile('Author Profile Page')})
    if authorchunks:
        for author in authorchunks:
            if authorchunks: authors = authors + str(author.text.strip()) + ':'  # .encode('ascii','ignore')
    else:
        authors = "no author"

    institutionchunks = review.findAll('a', {'title': re.compile('Institutional Profile Page')})
    if institutionchunks:
        for institution in institutionchunks:
            if institutionchunks: institutions = institutions + str(
                institution.text.strip()) + ':'  # .encode('ascii','ignore')
    else:
        institutions = 'no institutions'
    # fw.write(title+'\t'+authors+'\t'+institutions+'\n') # write to file
    # start_time=time.clock()
    datechunks = soup.find('meta', {'name': re.compile('citation_date')})
    datechunks_1 = str(datechunks)
    if datechunks:
        datechunks_1 = re.sub('[^0-9]', ' ', datechunks_1)  # .encode('ascii','ignore')
        numbers = datechunks_1.split(" ")
        for number in numbers:
            if number == "": continue
            date = number
    # print(time.clock()-start_time)

    abstractchunks = soup.find('div', {'class': re.compile('layout')})
    if abstractchunks:
        abstract = abstractchunks.find('div', {'class': 'flatbody'})
        # if abstract:
        abstracts = abstract.text.strip()
        # abstract_1 = abstracts.split('\n')
    # for abs_1 in abstract_1:
    #     abstract_2=abstract_2+abs_1
    # abstract_1=str(abstract_1)
    # labelchunks = review.find('a', {'class': 'link-text'})
    # if labelchunks:label=labelchunks.text.strip()
    # label = re.sub('[^A-Z]', ' ', label).strip()
    fw.write(authors + '\t' + str(abstracts) + '\t' + title + '\t' + institutions + '\t' + date + '\t' + str(label)+'\n')  # write to file
#
#
#
#
#
#
#



