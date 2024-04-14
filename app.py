from flask import Flask

app = Flask(__name__)

brands = [
    {
        "name": "Adidas",
        "items": [
            {
                "name": "Adidas Predator Pro PROMO Fingersave",
                "price": 117.00
            }
        ]
    }
]

# Flask Route
# First part is endpoint
@app.get("/brand")
def get_brands():
    return {"brands" : brands}

@app.post("/brand")
def create_brand():
    pass

@app.post("/brand/<string:name>/item")
def create_item(name):
    pass