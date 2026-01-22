#########################################################################
# Deployment Instructions:
#########################################################################
# 1. Start Server by opening cmd prompt in Windows. 
# 2. cd C:\Projects\Science Project
# 4.  python app.py 

#########################################################################
# Git Instructions:
#########################################################################
# 1. Go to cmd prompt in Windows.
# 2. cd C:\Projects\Science Project
# 3. git add .


from flask import Flask, render_template, request
from PIL import Image, ImageDraw
import os
import uuid
import random

app = Flask(__name__)

color_determiner = random.randint(2, 5)



if color_determiner == 1:
    color = "red"
if color_determiner == 2:
    color = "orange"
if color_determiner == 3:
    color = "yellow"
if color_determiner == 4:
    color = "green"
if color_determiner == 5:
    color = "blue"
if color_determiner == 6:
    color = "purple"
else:
    color = "white"
    

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

@app.route("/")
def index():
    return render_template("index.html")



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
    
    num_lines = 10000
    for _ in range(num_lines):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        # Generate random start and end coordinates within image dimensions
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        # Choose a random color and width
        # line_color = random.choice(colors)
        line_width = random.randint(1, 5) # Random width between 1 and 5 pixels

        # Draw the line
        draw.line([(x1, y1), (x2, y2)], fill=(red, green, blue, 100), width=line_width)


    img = Image.alpha_composite(baseImage, overlay)
    #save
    img.save(result_path)

    return render_template("index.html", result_image=result_path, color_determiner=color_determiner)


if __name__ == "__main__":
    app.run(debug=True)