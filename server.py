import tornado.httpserver
import tornado.ioloop
import tornado.web
import query
import config
import loadengine
import ranker

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    html = """
    <html><body>
    <form method="POST" action="/results">
    Search: <input type="text" name="query" size="100"><br>
    <input type="submit" value="Search">
    </form>
    </body></html>
    """
    self.write(html)

class ResultHandler(tornado.web.RequestHandler):
  def post(self):
    raw_query = self.get_argument('query')
    query_obj = query.Query(raw_query)
    print 'q_obj', query_obj.query
    q = query_obj.parse_query()
    results = self.search_query(q)
    html = '<html><body>%s</body></html>' % results
    self.write(results)

    
  def search_query(self, q):
    results = ranker.rank(q, config.matrix)
    html = '<table cellspacing="7">'
    for i in range(10):
      score = results[i][1]
      if score > 0:
        result = config.doclinks_list[config.indextodoc[results[i][0]]][0]
        html += '<tr><td>%s. <a href="%s" target="_blank">%s</a></td><td>Rank: %s</td></tr>' % (str(i+1), result, result, str(score))	
    html += '</table><br><br><a href="/search">Search Again</a>'
    return html
    	



application = tornado.web.Application([(r'/search', MainHandler),(r'/results', ResultHandler),])

if __name__ == "__main__":
  loadengine.load_engine()
  print 'Engine loaded...'
  print 'Starting web server...'
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
