#########################################################################
# Deployment Instructions:
#########################################################################
# 1. Activate Virtual Environment by going to cmd prompt in Windows. 
# >> cd C:\Projects\Science Project\.venv\Scripts\
# >> activate.bat
# 2 Go back 2 directories to C:\Projects\Science Project
# >> cd ..\..\ 
# 3. Type: python app.py
# 4. Open web browser and go to: http://127.0.0.1:5000/
########################################################################
# Quick Delpoyment Instructions
######################################################################
# cd C:\Projects\Science Project\.venv\Scripts\
# activate.bat
# cd ..\..\ 
# python app.py
###################################################################
#How to deploy to Public Server (not for carter)
##################################################################
#1. https://www.youtube.com/watch?v=H2Hxu7fDUOc

#########################################################################
# Git Instructions:
#https://github.com/merskis/image-processor.git
#########################################################################
# 1. Go to cmd prompt in Windows.
# 2. cd C:\Projects\Science Project
# 3. git add .
# 4. git commit -m "your message"

#5. git remote add origin https://github.com/merskis/image-processor.git
#git branch -M main
#git push -u origin main

#6. Create Requirements.txt
# pip freeze > requirements.txt
# git add requirements.txt
# git commit -m "Add requirements.txt"
# git push

############################################################################
# URL Path to Public Server
############################################################################
# https://www.pythonanywhere.com/user/peepdroid/files/home/peepdroid


############################################################################
# Update code from github
#############################################################
# 1. Go to console in pythonanywhere
# 2. cd /home/peepdroid/image-processor (main)
# 3. git pull origin main
# 4. pip install -r requirements.txt 
# 5. Go to Python Anywhere and go to Web tab and reload the web app


from flask import Flask, render_template, request
from PIL import Image, ImageDraw
import os
import uuid
import random

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

@app.route("/")


def home():
    return render_template('index.html')


def index():
    return render_template("index.html")

@app.after_request
def set_cache_headers(response):
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.max_age = 0
    return response

@app.route("/upload", methods=["POST"])
def upload():
    
    #Check if image was selected and uploaded
    if "image" not in request.files:
        return "No image upoaded", 400

    file = request.files["image"]
    filename = f"{uuid.uuid4()}.png"

    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    result_path = os.path.join(RESULT_FOLDER, filename)

    #save uploaded image
    file.save(upload_path)

    baseImage = Image.open(upload_path).convert("RGBA")
    
    width, height = baseImage.size

    overlay = Image.new("RGBA", baseImage.size, (0,0,0,0))
    
    draw = ImageDraw.Draw(overlay)
    
    transparency = int(request.form.get("intensity", 100))
    
    num_lines = 10000
    for _ in range(num_lines):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        tranperency = transparency
        fractal_randomness = random.randint(0,5)    
        # Generate random start and end coordinates within image dimensions
        x1 = random.randint(0, width+(fractal_randomness**2))
        y1 = random.randint(0, height+100)
        x2 = random.randint(0, width+100)
        y2 = random.randint(0, height+100)

        # Choose a random color and width
        # line_color = random.choice(colors)
        line_width = 1

        # Draw the line
        draw.line([(x1, y1), (x2, y2)], fill=(red, green, blue, tranperency), width=line_width)


    img = Image.alpha_composite(baseImage, overlay)
    #save
    img.save(result_path)

    return render_template("index.html", result_image=result_path)

if __name__ == "__main__":
    app.run(debug=True)
