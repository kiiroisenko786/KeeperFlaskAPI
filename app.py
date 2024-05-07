import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, retailers

app = Flask(__name__)

# Flask Route
# First part is endpoint

# Returns all retailers
@app.get("/retailer")
def get_retailers():
    return {"retailers" : list(retailers.values())}

# Returns all items
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}

# Creates new retailer
@app.post("/retailer")
def create_retailer():
    retailers_data = request.get_json()
    if "name" not in retailers_data:
        abort(
            400,
            message="Bad request"
        )
    for retailer in retailers.values():
        if retailers_data["name"] == retailer["name"]:
            abort(400, message=f"retailer already exists")
    retailer_id = uuid.uuid4().hex
    new_retailer = {**retailers_data, "id": retailer_id}
    retailers[retailer_id] = new_retailer
    return new_retailer, 201

# Creates a new item for a specific retailer
@app.post("/item")
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "retailer_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message = "Bad request; Ensure 'price', 'retailer_id' and 'name' are included in the JSON payload"
        )
    
    for item in items.values():
        if(
            item_data["name"] == item["name"]
            and item_data["retailer_id"] == item["retailer_id"]
        ):
            abort(400, message=f"Item already exists")

    if item_data["retailer_id"] not in retailers:
        abort(404, "retailer not found")
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201

# Retuns a specific retailer
@app.get("/retailer/<string:retailer_id>")
def get_retailer(retailer_id):
    try:
        return retailers[retailer_id]
    except KeyError:
        abort(404, "retailer not found")


# Update specific item
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, message="Bad request; Ensure 'price', 'retailer_id' and 'name' are included in the JSON payload")
    try:
        item = items[item_id]
        # pipe equals is the (new?) dictionary update operator
        item |= item_data

        return item
    except KeyError:
        abort(404, message="Item not found")

# Returns a specific item
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, "Item not found")

# Deletes item
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message="Item not found")

# Deletes retailer
@app.delete("/item/<string:retailer_id>")
def delete_retailer(retailer_id):
    try:
        del retailers[retailer_id]
        return {"message": "Retailer deleted"}
    except KeyError:
        abort(404, message="Retailer not found")
