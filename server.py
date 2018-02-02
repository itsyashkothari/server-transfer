# USAGE
# Start the server:
#   python run_keras_server.py
# Submit a request via cURL:
#   curl -X POST -F image=@dog.jpg 'http://localhost:5000/predict'
# Submita a request via Python:
#   python simple_request.py

# import the necessary packages
from keras.preprocessing.image import img_to_array
#from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import io
import time
from keras.models import load_model
import binascii
from flask_cors import CORS,cross_origin
import base64
# initialize our Flask application and the Keras model
app = flask.Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

model = None

def load():
    # load the pre-trained Keras model (here we are using a model
    # pre-trained on ImageNet and provided by Keras, but you can
    # substitute in your own networks just as easily)
    global model
    global mapping
    model = load_model('t2.h5')
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    mapping=['2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','K','M','N','P','R','S','T','V','W','X','Y','Z']


@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}
    print("req")
    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read the image in PIL format
            image = flask.request.files["image"].read()

            image = Image.open(io.BytesIO(image))
            image = img_to_array(image)/255
            # preprocess the image and prepare it for classification
            ans =[0,0,0,0,0]
            print(image.shape)
            for i in range(5):
                img =image[1:,i*47:(i*47)+64,:]
                img = np.reshape(img,(1,64,64,3))
                ans[i]=mapping[np.argmax(model.predict(img))]
            ans = ''.join(ans)
            print(ans)
            data = {"success":True,"value":ans}
    # return the data dictionary as a JSON response
    return flask.jsonify(data)
@app.route("/pre", methods=["POST"])
def pre():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        print('hello')
    return flask.jsonify(data)

@app.route("/predict23", methods=["GET","OPTIONS","POST"])
@cross_origin()
def predict23():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}
    jsonData = flask.request.get_json()
    print(jsonData['name'])
    print(jsonData['age'])
    image = Image.open(io.BytesIO(base64.b64decode(jsonData['extra'])))
    image.show()
    image = img_to_array(image)/255
            # preprocess the image and prepare it for classification
    ans =[0,0,0,0,0]
    print(image.shape)
    image=image[:,:,:3]
    for i in range(5):
        img =image[1:,i*47:(i*47)+64,:]
        img = np.reshape(img,(1,64,64,3))
        ans[i]=mapping[np.argmax(model.predict(img))]
    ans = ''.join(ans)
    print(ans)
    data = {"success":True,"value":ans}
    # return the data dictionary as a JSON response
    print("gotcha")
    return flask.jsonify(data)
    # ensure an image was properly uploaded to our endpoint
    

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    load()
    app.run()
#host = "0.0.0.0",port = 80