from flask import Flask, render_template, request, redirect, url_for
import csv
from pathlib import Path

path = Path(__file__).resolve().parent

app = Flask(__name__)

# ---------------------------- FLASK ROUTES ------------------------------- #
@app.route("/")
def home():
    with open(f"{path}/cafes-with-longlat.csv", newline="", encoding="utf-8") as csv_file:
        cafes = list(csv.DictReader(csv_file))
    return render_template("index.html", cafes=cafes)

@app.route("/addcafe", methods=["POST"])
def add_cafe():
    new_cafe = {
        "name": request.form["name"],
        "location": request.form["location"],
        "img_url": request.form["img_url"],
        "has_wifi": request.form.get("has_wifi", "0"),
        "has_sockets": request.form.get("has_sockets", "0"),
        "has_toilet": request.form.get("has_toilet", "0"),
        "can_take_calls": request.form.get("can_take_calls", "0"),
        "seats": request.form["seats"],
        "coffee_price": request.form["coffee_price"],
        "map_url": request.form["map_url"],
        "latitude": request.form["latitude"],
        "longitude": request.form["longitude"],
    }

    with open(f"{path}/cafes-with-longlat.csv", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames

    with open(f"{path}/cafes-with-longlat.csv", "a", newline="", encoding="utf-8") as csv_file:
        if fieldnames is not None:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames,
                extrasaction="ignore"
            )
            writer.writerow(new_cafe)

    return redirect(url_for("home"))

@app.route("/delete/<int:row_index>", methods=["POST"])
def delete_cafe(row_index):
    with open(f"{path}/cafes-with-longlat.csv", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        cafes = list(reader)
        fieldnames = reader.fieldnames

    cafes.pop(row_index)

    with open(f"{path}/cafes-with-longlat.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cafes)

    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)

