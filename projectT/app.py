import os
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, jsonify, render_template, send_from_directory
from os.path import join, dirname, realpath
from tensorflow import keras
import numpy as np
import tensorflow as tf
from keras.preprocessing import image


app = Flask(__name__,template_folder=r'projectT\template')
app._static_folder = r'projectT\static'
app.config["IMAGE_UPLOADS"] = r'projectT\static\uploads\image'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF","JFIF"]
model_path = r'projectT'
model = tf.keras.models.load_model(model_path)


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route('/')
def home():
    return render_template('upload.html')


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

                images = request.files["image"]
                
                if images.filename == "":
                    print("No filename")
                if allowed_image(images.filename):
                    filename = secure_filename(images.filename)
                    images.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    print("Image saved")

                else:
                    print("this extension not allowed")

                    
    path =  r'projectT\static\uploads\image\{}'.format(filename)
    
    def finds():
        test_image = image.load_img(path, target_size = (64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = model.predict(test_image)
        return result
    
    val = finds()
    if  val[0][0] == 1:
              prediction = 'DOG'
    else:
              prediction = 'CAT'

    return render_template('upload.html', prediction_text='The image you choosed was of a {}'.format(prediction))

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)