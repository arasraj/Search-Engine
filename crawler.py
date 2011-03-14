import urllib2
import hashlib
from urlparse import urljoin
from urlparse import urlparse
from BeautifulSoup import *
import robotparser
import codecs
import time

class Crawler():

  def __init__(self):
    self.frontier = ['http://www.cdm.depaul.edu.com']
    self.visited = []
    self.stopwords = ['jpg', 'jpe', 'png', 'pdf', 'gif', 'css', 'js', 'ppt', 'ps', 'doc']
    self.filetable = {}
    self.previous_host_visit = ''
    self.count = 0

  def crawl(self, depth=7):

    size = len(self.frontier)

    for i in range(depth):
      for j in range(size):

      	url = self.frontier[j-1]
      	if self.previous_host_visit == urlparse(url).netloc:
      		time.sleep(10)
      	if url in self.visited: continue

        try:
          conn = urllib2.Request(url, 'utf-8')
          conn.addheader = [('User-Agent', 'RajBot - Email arasraj@gmail.com if behaving badly.' )]
          page = urllib2.urlopen(conn)
          print 'Opening connection to %s...' % url
        except:
          print 'Error getting page %s' % url
          continue
        
        parsedhtml = BeautifulSoup(page)
        links = parsedhtml('a')
        
        check_list = []
        for link in links:
          if ('href' in dict(link.attrs)):
            tmpurl = urljoin(url, link['href'])
      	    tmpurl = tmpurl.split('#')[0]
            #alloed mailto: for some reason
            if url[:4] != 'http': continue
      	    check_list.append(tmpurl)


        robot_ok = self.robots_ex(url, check_list)
        noise = self.files_excluded(robot_ok)
        frontier_new = self.dup_frontier(noise)
        self.frontier.extend(frontier_new)
        filename = hashlib.md5(url).hexdigest() + '.txt'
        self.filetable[url] = filename

        site_text = self.extract_text(parsedhtml)
        fout = codecs.open('index/' + filename, 'w', 'utf-8')
        fout.write('** %s **' % url)
        fout.write(unicode(site_text))
        fout.flush()
        fout.close()
        if url[-1:] == '/':
          url = url[-1:]
        self.visited.append(url)
        self.count += 1
        if self.count >= 5000:
          print 'count', self.count
          return
        self.previous_host_visit = urlparse(url).netloc

      self.frontier = self.frontier[size:]
      size = len(self.frontier)
      urls = self.frontier

  def extract_text(self, html):

    texts = html.findAll(text=True)
    #text = html.string
    #if text == None:
    #  markups = html.contents
    #  parsedtext = ''
    #  for markup in markups:
    #    tmp = self.extract_text(markup)
    #    parsedtext += tmp + '\n'
    #  return parsedtext
    #else:
    #	return text.strip()
    def gettext(item):
      if item.parent.name in ['style', 'script', '[document]', 'head', 'title']:
      	return False
      return True

    text = filter(gettext, texts)
    parsed_text = ''.join(text)
    return parsed_text.replace('\n', '')
    	

  def robots_ex(self, root, urls):
    try:
      rp = robotparser.RobotFileParser()
      rp.set_url(urljoin(root, '/robots.txt'))
      rp.read()
      print 'Getting robots.txt ...'
    except:
      print 'Error getting page %s' % root
      return 'false'

    allowed = []
    for url in urls:
      try:
        url = unicode(url)
        if rp.can_fetch('*', url):
          allowed.append(url)
      except:
        pass
    return allowed

  def dup_frontier(self, urls):
    allowed = []
    for url in urls:
      try:
        if url[-1:] == '/':
          url = url[-1:]
        if url not in self.visited:
          allowed.append(url)
      except:
        pass
    return allowed

  def files_excluded(self, urls):
    allowed = []
    for url in urls:
      if url[-3:] not in self.stopwords:
      	allowed.append(url)
    return allowed
    
    



if __name__ == '__main__':
  spider = Crawler()
  spider.crawl()
  #c=urllib2.urlopen('http://www.fittidbit.com')
  #soup = BeautifulSoup(c.read())
  #print spider.robots_ex('http://www.fittidbit.com/')    
