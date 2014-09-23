from google.appengine.ext import ndb
from google.appengine.ext import images

DEFAULT_STREAM_CONTAINER = "default_streams"
DEFAULT_IMAGE_CONTAINER = "default_images"

def image_key(image_container = DEFAULT_IMAGE_CONTAINER) :
    '''Constructs a Datastore key for the image store'''
    return ndb.Key('Images', image_container)

def stream_key(stream_container=DEFAULT_STREAM_CONTAINER) :
   '''Constructs a Datastore key for a Streams entity with default_streams'''
    return ndb.Key('Streams', stream_container)

class Images(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    image = ndb.BlobProperty()

class Stream(ndb.Model):
    sid = ndb.StringProperty(indexed=True)
    urls = ndb.StringProperty(indexed=False, repeated=True)
    cover = ndb.StringProperty(indexed=False)

# create a stream (which takes a stream definition and returns a status code), 
def create_stream(sid, urls, cover) :
    s = Stream(parent=stream_key())
    s.sid = sid
    s.urls = urls
    s.cover = cover
    s.put()

# view a stream (which takes a stream id and a page range and returns a list of URLs to 
#images, and a page range), 
def view_stream(sid, page_start, page_end) :
    stream = get_stream(sid) 
    return {'urls' : stream.urls}

# image upload (which takes a stream id and a file), 
def upload_image(sid, f) :
    stream = get_stream(sid)
    file_upload = open(f, 'r')
    file_name = os.path.basename(f)
    #file_upload = self.request.POST.get('file', None)
    image = Images(id=file_name, name=file_name, blob=file_upload.read())
    image.put() 
    stream.urls += ['/img/%s' % file_name]

# view all streams (which returns a list of names of streams and their cover images), 
def view_all() :
    result = []
    for s in Stream.all() :
        result += [{'name' : s.sid, 'cover' : s.cover}]
    return result
 
# search streams (which takes a query string and returns a list of streams (titles and 
# cover image urls) that contain matching text, most viewed streams (which returns a 
# list of streams sorted by recent access frequency), and reporting request.
def search_streams(query_str) :
    return ([None], [None], None)

def get_stream(sid) :
    stream_query = Stream.query(
        ancestor = stream_key())
    stream = stream_query.filter('sid =', sid).get()

