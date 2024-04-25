import requests
import random
from datetime import datetime
import time

Articles = {
    "Croissant": 1.5,
    "Chocolate Eclair": 7.5,
    "Fruit Tart": 8.5,
    "Cinnamon Roll": 4.0,
    "Danish Pastry": 6.5,
    "Palmier": 3.0,
    "Cream Puff": 9.0,
    "Apple Turnover": 5.0,
    "Bear Claw": 6.8,
    "Napoleon": 7.9,
    "Cheesecake": 10.5,
    "Strudel": 8.0,
    "Muffin": 3.5,
    "Baguette": 2.0,
    "Scone": 2.8,
    "Cupcake": 4.5,
    "Cherry Pie": 9.5,
    "Blueberry Muffin": 3.8,
    "Pecan Pie": 11.0,
    "Key Lime Tart": 8.2,
    "Red Velvet Cake": 12.0,
    "Lemon Bar": 6.0
}

while True:
    article = random.choice(list(Articles.keys()))
    prix = Articles[article]

    quantity = random.choice(list(range(1, 20)))
    total = quantity * prix

    sale_type = random.choice(["direct", "livraison"])
    payment_mode = "online" if sale_type == "livraison" else random.choice(["cash", "card"])


    payload = {
        "pos_id": 2,
        "pos_name": "Beja Centre",
        "article": article,
        "quantity": quantity,
        "unit_price": prix,
        "total": total,
        "sale_type": sale_type,
        "payment_mode": payment_mode,
        "sale_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

    api_url = "http://localhost:8082/orderitem"

    response = requests.post(api_url, json=payload)

    print(response.json())

    time_to_sleep = random.randint(1, 11)
    time.sleep(time_to_sleep)
