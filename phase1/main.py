import os
import urlllib

import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        
class Image(webapp2.RequestHandler):
    def get(self):
        greeting = db.get(self.request.get('img_id'))
        if greeting.avatar:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(greeting.avatar)
        else:
            self.response.out.write('No image')

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/img/.*', Image)
    ],debug=True)    
