from flask import Flask, render_template, request, redirect, url_for
#from data import Articles
import os
from werkzeug.utils import secure_filename
from PIL import Image
# import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import *
from keras.models import load_model
import os.path

app = Flask(__name__)

#Articles = Articles()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


# @app.route('/articles')
# def articles():
#     return render_template('articles.html', articles=Articles)


# @app.route('/article/<string:id>')
# def article(id):
#     return render_template('article.html', articles=Articles, id=id)


@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'static/test_images/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)	

    newDes = os.path.join('static/test_images/'+filename)
    
    train_categories = ['Apple', 'Banana', 'Beetroot', 'Cauliflower', 'Coconut', 'Corn', 'Eggplant',
                        'Guava', 'Kiwi', 'Lemon', 'Litchi', 'Onion', 'Orange', 'Pineapple', 'Pomegranate', 
                        'Potato', 'Starfruit', 'Strawberry', 'Tomato', 'Watermelon']
    # train_samples = []
  
    # model.load_weights("finalmodel.hdf5")
    img = Image.open(newDes)
    original_img = np.array(img, dtype=np.uint8)
    # plt.imshow(original_img)

    if img.size[0] > img.size[1]:
        scale = 100 / img.size[1]
        new_h = int(img.size[1]*scale)
        new_w = int(img.size[0]*scale)
        new_size = (new_w, new_h)
    else:
        scale = 100 / img.size[0]
        new_h = int(img.size[1]*scale)
        new_w = int(img.size[0]*scale)
        new_size = (new_w, new_h)

    resized = img.resize(new_size)
    resized_img = np.array(resized, dtype=np.uint8)
    # plt.imshow(resized_img)

    left = 0
    right = left + 100
    up = 0
    down = up + 100
    model = load_model('model.h5')
    cropped = resized.crop((left, up, right, down))
    cropped_img = np.array(cropped, dtype=np.uint8)
    # plt.imshow(cropped_img)

    cropped_img = cropped_img / 255
    X = np.reshape(cropped_img, newshape=(1, cropped_img.shape[0], cropped_img.shape[1], cropped_img.shape[2]))
    prediction_multi = model.predict(x=X)
    # print(np.argmax(prediction_multi))
    print("Fruit is : ", train_categories[np.argmax(prediction_multi)])
    fruit_name = train_categories[np.argmax(prediction_multi)]

    acc_sort_index = np.argsort(prediction_multi)
    top_pred = acc_sort_index[:, -6:]
    results =[train_categories[top_pred[0][-1]]]
    result = results[0]
    if(result == 'Apple'):
        fruit=['Apple Pie','https://www.youtube.com/watch?v=oL84s7OL8WU',
               'Apple Halwa','https://www.youtube.com/watch?v=BuuPb_I3XWI',
               'Apple Milkshake','https://www.youtube.com/watch?v=K7os6NFPgck',
               '95','0','1','25','3']
    elif(result == 'Banana'):
        fruit=['Banana Chips','https://www.youtube.com/watch?v=IdACN848-oQ',
               'Banana Pancake','https://www.youtube.com/watch?v=kY-d4rRPcUk',
               'Banana Ice Cream','https://www.youtube.com/watch?v=g5swlU5ZdJ4',
               '110','0','1','28','3' ]
    elif(result == 'Beetroot'):
        fruit=['Beetroot Tikki','https://www.youtube.com/watch?v=YZT7a3Jo28E',
               'Beetroot Curry','https://www.youtube.com/watch?v=NFoXcolYMqo',
               'Beetroot fry with coconut','https://www.youtube.com/watch?v=QXQGwv3l02U',
               '58','0.2','2.2','13','3.8']
    elif(result == 'Cauliflower'):
        fruit=['Cauliflower Fry','https://www.youtube.com/watch?v=fh1ElyB5uds',
                'Gobi Masala','https://www.youtube.com/watch?v=bl5lDQC1Fno',
                'Aloo Gobi','https://www.youtube.com/watch?v=sSC8tC738DY',
                '25','0','2','5','2']
    elif(result == 'Coconut'):
        fruit=['Fresh Coconut Burfi','https://www.youtube.com/watch?v=i2dwhWC6nak',
                'Instant Coconut Rava Ladoo','https://www.youtube.com/watch?v=FgoS2cGBr_A',
                'Coconut Sheera','https://www.youtube.com/watch?v=Bp7ycUnmKa8',
                '354','33','3','15','9']
    elif(result == 'Corn'):
        fruit=['Crispy Corn Kebabs','https://www.youtube.com/watch?v=fJi8b7_XuH0',
               'Masala Corn Sabzi','https://www.youtube.com/watch?v=wAWGREdQAq8',
               'Indian Style Masala Street Corn','https://www.youtube.com/watch?v=06kwABpkb2Y',
               "96","1.5","3.4","21","2.4"]
    elif(result == 'Eggplant'):
        fruit=['Baingan Masala Recipe','https://www.youtube.com/watch?v=tQfQ1Eonmyg',
               'Brinjal Fry Recipe','https://www.youtube.com/watch?v=RHXNrUYTITY',
               'Eggplant with Spicy Tomato Dry','https://www.youtube.com/watch?v=V6sI1ShmnNs',
               "20.5","0.1","0.8","4.8","2.4"]
    elif(result == 'Guava'):
        fruit=['Sweet and Sour Guava Curry','https://www.youtube.com/watch?v=XN571uRFUP8',
               'Guava Halwa','https://www.youtube.com/watch?v=PjeJpNiVT-0',
               'Guava Chutney','https://www.youtube.com/watch?v=uwiC5z1EiBo',
               "112","1.6","4.2","23.6","8.9"]
    elif(result == 'Kiwi'):
        fruit=['Kiwi Raita','https://www.youtube.com/watch?v=SYCbEJIIth0',
               'Masala Kiwi Juice','https://www.youtube.com/watch?v=YhvsZtgLYBk',
               'Tangy Delicious Kiwi Mint Chutney','https://www.youtube.com/watch?v=9KN_Oma21qY',
               "42","0.4","0.8","10.1","2.1"]
    elif(result == "Lemon"):
        fruit=['Lemon rice recipe','https://www.youtube.com/watch?v=AmSNobM6ebM',
               'Lemon pickle recipe','https://www.youtube.com/watch?v=eOtb5ayI778',
               'Lemon Dal','https://www.youtube.com/watch?v=Y3I1vfvlYVI',
               "29","0.3","1.1","9.3","2.8"]
    elif(result == "Litchi"):
        fruit = ["Litchi IceCream", "https://www.youtube.com/watch?v=ActpQLsBm5U", 
                 "Litchi Pudding", "https://www.youtube.com/watch?v=3H-SxHit8lw", 
                 "Litchi Juice", "https://www.youtube.com/watch?v=imQhkDtz0tU",
                 "66","0.4","0.8","16.5","1.3"]
    elif(result == "Onion"):
        fruit = ["Cream and Onion", "https://www.youtube.com/watch?v=yCP4S5FNPAI", 
                 "Onion Rings", "https://www.youtube.com/watch?v=_gWreCzu_g4", 
                 "Onion Sabzi", "https://www.youtube.com/watch?v=I843M9m8XKo",
                 "40","0.1","1.1","9.3","1.7"]
    elif(result == "Orange"):
        fruit = ["Orange Halwa", "https://www.youtube.com/watch?v=iTYixf80Dj8",
                 "Orange Delight", "https://www.youtube.com/watch?v=G2pWnoJXIDE",
                 "Orange Jelly","https://www.youtube.com/watch?v=gMt0W3iMqlE",
                 "47","0.1","0.9","11.8","2.4"]
    elif(result == "Pineapple"):
        fruit = ["Sweet Pineapple", "https://www.youtube.com/watch?v=rUmPOcG9K_c",
                 "Pineapple Curry","https://www.youtube.com/watch?v=rUmPOcG9K_c",
                 "Pineapple Halwa","https://www.youtube.com/watch?v=aMUie-1UNHA",
                 "82.5","0.2","0.9","22.0","2.3"]
    elif(result == "Pomegranate"):
        fruit = ["Pomegranate Pudding","https://www.youtube.com/watch?v=ugWrnFdJQRM",
                 "Pomegranate Salad","https://www.youtube.com/watch?v=s8UJllsnX4k",
                 "Pomegranate Burfi","https://www.youtube.com/watch?v=gW_yR2ExRT0",
                 "128","2.0","3.0","29.0","6.0"]
    elif(result == "Potato"):
        fruit = ["Potato Bites","https://www.youtube.com/watch?v=oXN-fI2L2YI",
                 "Roasted Garlic Potatoes","https://www.youtube.com/watch?v=3IhKjd9SVoU",
                 "French Fries", "https://www.youtube.com/watch?v=0OAGLoB0SYk",
                 "87","0.1","1.9","20.1","1.8"]
    elif(result == "Starfruit"):
        fruit = ["Starfruit Sabzi","https://www.youtube.com/watch?v=AdQknYqvXbg",
                 "Starfruit Chutney","https://www.youtube.com/watch?v=HzoRhwplAc8",
                 "Starfruit Salad","https://www.youtube.com/watch?v=T5JSh-i93Eo",
                 "41","0.4","1.4","8.9","3.7"]
    elif(result == "Strawberry"):
        fruit = ["Strawberry Jelly","https://www.youtube.com/watch?v=SRtpdvzGNqQ",
                 "Strawberry Cake","https://www.youtube.com/watch?v=Ro8F9jJZ_DA",
                 "Strawberry Peda","https://www.youtube.com/watch?v=bqlFzG4_Q9A",
                 "32","0.3","0.7","7.7","2.0"]
    elif(result == "Tomato"):
        fruit = ["Tomato Sabzi","https://www.youtube.com/watch?v=2qV40NfC8Bs",
                 "Tomato Curry","https://www.youtube.com/watch?v=IiYbxhxe1r4",
                 "Tomato Ketchup","https://www.youtube.com/watch?v=3mJUF8s7c40",
                 "16","0.2","0.8","3.5","1.1"]
    else:
        fruit = ["Watermelon Halwa","https://www.youtube.com/watch?v=9AaO9eC2nso",
                 "Watermelon Popsicles","https://www.youtube.com/watch?v=F31JYfEz0DQ",
                 "Watermelon Juice","https://www.youtube.com/watch?v=x3R68g7QHqk",
                 "30","0.2","0.6","7.6","0.4"]


    return render_template('about.html',results = results,y1 = fruit[1],y2 = fruit[3], y3 = fruit[5],
                            n1 = fruit[0],n2 = fruit[2], n3 = fruit[4] ,calorie = fruit[6],fat = fruit[7],
                            protein = fruit[8],carb = fruit[9],fibre = fruit[10])
    #return (results, destination)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run( debug=True)
