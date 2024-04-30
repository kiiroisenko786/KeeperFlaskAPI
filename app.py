import uuid
from flask import Flask, request
from flask_smorest import abort
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
    if "name" not in brands_data:
        abort(
            400,
            message="Bad request"
        )
    for brand in brands.values():
        if brands_data["name"] == brand["name"]:
            abort(400, message=f"Brand already exists")
    brand_id = uuid.uuid4().hex
    new_brand = {**brands_data, "id": brand_id}
    brands[brand_id] = new_brand
    return new_brand, 201

# Creates a new item for a specific brand
@app.post("/item")
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "brand_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message = "Bad request; Ensure 'price', 'brand_id' and 'name' are included in the JSON payload"
        )
    
    for item in items.values():
        if(
            item_data["name"] == item["name"]
            and item_data["brand_id"] == item["brand_id"]
        ):
            abort(400, message=f"Item already exists")

    if item_data["brand_id"] not in brands:
        abort(404, "Brand not found")
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201

# Retuns a specific brand
@app.get("/brand/<string:brand_id>")
def get_brand(brand_id):
    try:
        return brands[brand_id]
    except KeyError:
        abort(404, "Brand not found")

# Returns a specific item
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, "Item not found")

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message="Item not found")