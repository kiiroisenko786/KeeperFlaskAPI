from flask import Flask, request

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
# Returns all brands as well as their items
@app.get("/brand")
def get_brands():
    return {"brands" : brands}

# Creates new brand
@app.post("/brand")
def create_brand():
    request_data = request.get_json()
    new_brand = {"name": request_data["name"], "items": []}
    brands.append(new_brand)
    return new_brand, 201

# Creates a new item for a specific brand
@app.post("/brand/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for brand in brands:
        if brand["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            brand["items"].append(new_item)
            return new_item, 201
    return {"message": "Brand not found"}, 404

# Retuns a specific brand
@app.get("/brand/<string:name>")
def get_brand(name):
    for brand in brands:
        if brand["name"] == name:
            return brand
    return {"message": "Brad not found"}, 404

# Returns a specific item from a specific brand
@app.get("/brand/<string:name>/item")
def get_item_in_brand(name):
    for brand in brands:
        if brand["name"] == name:
            return {"items": brand["items"]}
    return {"message": "Brand not found"}, 404