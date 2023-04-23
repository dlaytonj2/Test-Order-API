import json

import quart
import quart_cors
from quart import Quart, request, jsonify, send_from_directory, render_template
from datetime import datetime


# In[ ]:


# Note: Setting CORS to allow chat.openapi.com is only required when running a localhost plugin
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")


# In[ ]:


# List of available products
products = [
    {"name": "Base Coffin (pine)", "price": 599.00},
    {"name": "Modest Coffin (laminated)", "price": 1500.00},
    {"name": "Sleek Coffin (Fibreglass)", "price": 4000.00},
    {"name": "Luxury Coffin (walnut & Brass)", "price": 10000.00},
]

@app.route('/order', methods=['POST'])
async def create_order():
    data = await request.json

    try:
        product_id = data['product_id']
        quantity = data['quantity']
    except KeyError:
        return jsonify({"error": "product_id and quantity are required"}), 400

    if product_id < 1 or product_id > len(products):
        return jsonify({"error": "Invalid product_id"}), 400

    selected_product = products[product_id - 1]

    # Generate order
    order_number = datetime.now().strftime("%Y%m%d%H%M%S")
    date_of_order = datetime.now().strftime("%B %d, %Y")
    total_price = selected_product['price'] * quantity

    order = {
        "order_number": order_number,
        "date_of_order": date_of_order,
        "product": selected_product,
        "quantity": quantity,
        "total_price": round(total_price, 2),
    }

    return jsonify(order), 201


# In[ ]:


# sample code from OpenAI documentation starts here 

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    print("plugin_manifest",host)
    with open(".well-known/ai-plugin.json") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the manifest
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        print("plugin_manifest",text)
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    print("openapi_spec",host)
    with open("openapi.yaml") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the OpenAPI spec
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        print('openapi_spec:', text)
        return quart.Response(text, mimetype="text/yaml")


# In[ ]:


def main():
    app.run(debug=True, host="0.0.0.0", port=5001)


if __name__ == "__main__":
    main()    
 

