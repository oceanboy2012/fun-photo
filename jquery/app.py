#!/home/pi/.viertualenvs/flask/bin/python

# In this example we are going to create a simple HTML
# page with 2 input fields (numbers), and a link.
# Using jQuery we are going to send the content of both
# fields to a route on our application, which will
# sum up both numbers and return the result.
# Again using jQuery we'l show the result on the page


# We'll render HTML templates and access data sent by GET
# using the request object from flask. jsonigy is required
# to send JSON as a response of a request
from flask import Flask, render_template, request, jsonify
import picamera
import time

# Initialize the Flask application
app = Flask(__name__)

#load default configuations then user specified
#app.config.from_object('photobooth.default_settings')
#app.config.from_envvar('USER_SETTINGS')


# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')

# Route that will process the AJAX request, sum up two
# integer numbers (defaulted to zero) and return the
# result as a proper JSON response (Content-Type, etc.)
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/show')
def show():
    return render_template('simple_slideshow.html')

#def take_pictures():
@app.route('/take')
def take():
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        time.sleep(2)
        for x in range(1,5):
            camera.capture('/home/pi/git/flask/jquery/static/test/%s.jpg' % (x))
            time.sleep(1)
    return render_template('simple_slideshow.html')    

#    return 

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("5000"),
        debug=True
    )

