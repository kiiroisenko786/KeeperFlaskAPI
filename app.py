import uuid
from flask import Flask, request
from db import items, brands

app = Flask(__name__)

# Flask Route
# First part is endpoint

# Returns all brands
@app.get("/brand")
def get_brands():
    return {"brands" : list(brands.values())}

# Returns all items
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}

# Creates new brand
@app.post("/brand")
def create_brand():
    brands_data = request.get_json()
    brand_id = uuid.uuid4().hex
    new_brand = {**brands_data, "id": brand_id}
    brands[brand_id] = new_brand
    return new_brand, 201

# Creates a new item for a specific brand
@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data["brand_id"] not in brands:
        return {"message": "Brand not found"}, 404
    item_id = uuid.uuid4.hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201

# Retuns a specific brand
@app.get("/brand/<string:name>")
def get_brand(brand_id):
    try:
        return brands[brand_id]
    except KeyError:
        return {"message": "Brad not found"}, 404

# Returns a specific item
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Brand not found"}, 404