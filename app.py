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
@app.get("/brands")
def get_brands():
    return {"brands" : brands}