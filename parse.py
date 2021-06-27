import string, random, os, sys, _thread, httplib2, time

if len(sys.argv) < 2:
    sys.exit("\033[1;34mUsage: python3 " + sys.argv[0] + " (Number of threads)")

THREAD_AMOUNT = int(sys.argv[1])
INVALID_SIZE = [0, 503]
INVALID_EXT = ["text/html"]
MIME = {"image/png": "png", "image/jpeg": "jpg", "image/jpg": "jpg", "image/gif": "gif"}

def scrape_pictures(thread):
    dirName = 'thread' + thread
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    while True:
        length = random.choice((5, 6))
        if (length == 5):
            tmpName = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
        else:
            tmpName = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))
            tmpName += ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))

            url = 'https://i.imgur.com/'
            url += tmpName
            url += '.jpg'

            h = httplib2.Http()
            response, content = h.request(url)

            if ((response['content-type'] in INVALID_EXT) or (int(response['content-length']) in INVALID_SIZE)):
                # print("Skip: " + tmpName)
                continue

            print("Thread: %s Saving: %s %s %s" % (thread, tmpName, response['content-type'], int(response['content-length'])))
            ext = MIME[response['content-type']]
            fileName = dirName + '/' + tmpName + '.' + ext
            out = open(fileName, 'wb')
            out.write(content)
            out.close()
            time.sleep(2)

for thread in range(1, THREAD_AMOUNT + 1):
    thread = str(thread)
    try:
        _thread.start_new_thread(scrape_pictures, (thread,))
    except:
        print('Error starting thread ' + thread)

print('Succesfully started ' + thread + ' threads.')

while True:
    time.sleep(1)