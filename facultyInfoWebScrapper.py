import urllib
from bs4 import BeautifulSoup
import csv
import sys
import cStringIO
import codecs
import re

# from http://docs.python.org/2/library/csv.html#csv.writer
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
            
#Parser function to find school ID
def parseSchool(uni):
    csvfile = codecs.open('schools.csv', 'rU')
    reader = csv.DictReader(csvfile)
    for row in reader:
        if (row['name'] == uni ):
            #print(row['name'], row['id'])
            return row['id']
    return -1

#Parser to get grad degree,school and year info
def parseGradInfo(text):
    
    if len(text) == 0:
        return []
      
    degree = re.findall(r"\bPh.D.\b | \bPhD\b | \bPh.D\b",text)
    gradyear = re.findall(r'\d+', text)
    
    #split text
    lst = text.split(',')
    if len(lst) > 3:
        uni = lst[-2].strip()
        gradschool = parseSchool(uni)
    else:
        gradschool = -1
        
    ret = []
    graddegree = 'Ph.D'
    
    if not degree:
        ret.append('')
    else:
        ret.append(unicode(graddegree))        
        
    if gradschool == -1:
        ret.append('')
    else:
        ret.append(unicode(gradschool))
        
    if not gradyear:
        ret.append('')
    else:
        ret.append(unicode(gradyear[0]))
    
    return ret


# all depts: http://www.ucsb.edu/academics/depts/
# URL of differnt faculty dept
cs_url = "http://www.cs.ucsb.edu/people"
mc_url = "https://www.mcdb.ucsb.edu/people/faculty"
ee_url = "http://www.ece.ucsb.edu/directory/faculty/"
me_url = "https://me.ucsb.edu/people/faculty"
sociology_url = "http://www.soc.ucsb.edu/faculty"

#### global vars
# header values for the csv file
columns = ['id','firstname', 'lastname','facultytitle', 'facultyschool','facultydept', 
           'graddegree', 'gradschool', 'gradyear']
# master list to add values from various webpages
facultyMain = []; 
counter = 1
school = u'14' # UC santa barbara


####################
# CS dept

dept = u"Computer Science"
html = urllib.urlopen(cs_url).read()
html = "".join(line.strip() for line in html.split("\n"))
soup = BeautifulSoup(html)

# to see how soup is formatted
#print(soup.prettify())
#print soup('table')[0].prettify() 

#iterate through the table to get relevant data
for row in soup('table')[0].find('tbody').findAll('tr'):
    data = row.findAll('td');
    #create list for each faculty member
    fac = [];
    fac.append(unicode(counter))
    counter += 1
    fullname = data[0].a.string.split()
    fac.append(fullname[0]);
    fac.append(fullname[-1]);
    fac.append(data[1].string.strip());
    fac.append(school)
    fac.append(dept)
    
    # get data from the link
    link = data[0].a["href"].split('/');
    fac_url = cs_url + '/' + link[2] + '/' + link[3]
    h = urllib.urlopen(fac_url).read()
    s = BeautifulSoup(h)
    edu = s.find(id = 'block-system-main')
    #grad = edu.findNext('ul').find('li').text.split(',')
    grad = edu.findNext('ul').find('li').text
    print edu.findNext('ul').find('li').text
    grad = parseGradInfo(grad)
    for item in grad:
        fac.append(item)
    
    # finally add faculty member to the master list as row
    facultyMain.append(fac);

##########################

##########################
# electrical engg dept

dept = u"Electrical and Computer Engineering"
html = urllib.urlopen(ee_url).read()
html = "".join(line.strip() for line in html.split("\n"))
soup = BeautifulSoup(html)

## loop thru the faculty table to gather info
for row in soup('table')[0].findAll('tr'):
    data = row.findAll('td');
    if len(data) == 0:
        continue
        
    fac = [];
    fac.append(unicode(counter))
    counter += 1
    fullname = data[1].a.string.split()
    fac.append(fullname[0]);
    fac.append(fullname[-1]);
    if data[2].string is None:
        fac.append('')
    else:
        fac.append(data[2].string);
    
    fac.append(school)
    fac.append(dept)
    
    ##TODO: graddegree,school and year
    # get data from the link
    link = data[1].a["href"]
    h = urllib.urlopen(link).read()
    s = BeautifulSoup(h)
    #edu = s.body.findAll(text = 'Ph.D')
    #edu = s.find(text=re.compile('Ph.D.'))
    #print type(edu)
    
    #edu = soup.find(text=re.compile('Biography'))
    #for edu in s.find(id='maincontent').findAll('tr'):
        #ele = edu.findAll('td')
     #   print ele
#     grad = edu.findNext('ul').find('li').text.split(',')
#     for item in grad:
#         fac.append(item)

    facultyMain.append(fac);

##########################

##########################
## molecular cellular

dept = u"Molecular, Cellular, and Developmental Biology"
html = urllib.urlopen(mc_url).read()
html = "".join(line.strip() for line in html.split("\n"))
soup = BeautifulSoup(html)

## loop thru the faculty table to gather info

for row in soup('table')[0].findAll('tr'):
    data = row.findAll('td');
    if len(data) == 0:
        continue
        
    fac = [];
    fac.append(unicode(counter))
    counter += 1
    
    name = data[1].a.string.split()
    fac.append(name[0]);
    fac.append(name[1]);
    title = data[1].text.replace(data[1].a.string,'').strip()
    fac.append(title);
    fac.append(school)
    fac.append(dept)
    
#     print fac;
    facultyMain.append(fac);
    #print data
    #print data[1].a.string
    #print data[1].text.replace(data[1].a.string,'')
    #print data[3].string
    
##########################


##########################
# dept of sociology

dept = u"Sociology"
html = urllib.urlopen(sociology_url).read()
html = "".join(line.strip() for line in html.split("\n"))
soup = BeautifulSoup(html)

## loop thru the faculty table to gather info

for row in soup('table')[0].findAll('tr'):
    data = row.findAll('td');
    if len(data) == 0:
        continue
    else:
        for col in data:
            fac = []
            fac.append(unicode(counter))
            counter += 1
            if len(col) == 0:
                continue
            else:
                name = col.a.string.split()
                fac.append(name[0]);
                fac.append(name[1]);
                
                link = col.a["href"].split('/')
                link = sociology_url + '/' + link[2]
                #print link
                h = urllib.urlopen(link).read()
                s = BeautifulSoup(h)
                mydiv = s.find("div", { "class" : "job_title" })
                #print mydiv.text
                fac.append(mydiv.text)
                fac.append(school)
                fac.append(dept)
                
                mydiv = s.find("div", { "class" : "education_level" })
                #print mydiv.text
                edu = mydiv.text.split(',')
                if len(edu) >= 2:
                    #print edu[0]
                    #print edu[1].strip()
                    if 'Ph' in edu[0]:
                        fac.append(edu[0])
                    else:
                        fac.append('')
                    
                    gradCode = parseSchool(edu[1].strip())
                    if gradCode == -1:
                        fac.append('')
                    else:
                        fac.append(gradCode)
                elif len(edu) == 1:
                    #edu = edu[0].split()
                    #print edu
                    if 'Ph' in edu[0]:
                        fac.append(edu[0])
                    else:
                        fac.append('')
                        
                    fac.append('')#university
                    
            fac.append('')                

            facultyMain.append(fac)
    
##########################

##########################
# mechanical engg dept

dept = u"Mechanical Engineering"
html = urllib.urlopen(me_url).read()
html = "".join(line.strip() for line in html.split("\n"))
soup = BeautifulSoup(html)

## loop thru the faculty table to gather info

facultySection = soup.find(id = 'content-column')
section = facultySection.findNext('ul').findAll('li')

for row in section:
    fac = [];
    fac.append(unicode(counter))
    counter += 1
    #print row.text
    values = row.text.split()
    fac.append(values[0])
    fac.append(values[1])
    titleFac = values[2]
    #print 't' + '----->  ' + titleFac
    if 'Professor' in titleFac:
        #print values[2]
        fac.append(values[2])
    else:
        fac.append('')
        
    fac.append(school)
    fac.append(dept)
    facultyMain.append(fac)

##########################

######### Finally create and write into csv file
fp = codecs.open('kirtikaFaculty.csv', 'w')
writer = UnicodeWriter(fp)
writer.writerow(columns)
for faculty in facultyMain:
    writer.writerow(faculty)
fp.close()

