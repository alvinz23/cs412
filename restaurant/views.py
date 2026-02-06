# restaurant/views.py
from django.shortcuts import render
import random
from datetime import datetime, timedelta

# East Asian menu (simple prices, strings only)
MENU = [
    {"key": "ramen", "name": "Tonkotsu Ramen", "price": 14.50},
    {"key": "bibimbap", "name": "Bibimbap", "price": 13.25},
    {"key": "katsu", "name": "Chicken Katsu Curry", "price": 15.00},
    {"key": "sushi", "name": "Salmon Avocado Roll", "price": 9.75},
]

# One item with options: ramen add-ons
RAMEN_ADDONS = [
    {"key": "egg", "name": "Ajitama Egg", "price": 1.50},
    {"key": "chashu", "name": "Extra Chashu", "price": 3.00},
    {"key": "nori", "name": "Nori", "price": 1.00},
    {"key": "spice", "name": "Extra Spice", "price": 0.50},
]

DAILY_SPECIALS = [
    {"name": "Korean Fried Chicken Bowl", "price": 15.75, "desc": "Gochujang glaze, rice, pickled radish"},
    {"name": "Spicy Miso Ramen Set", "price": 16.25, "desc": "Ramen + gyoza (3)"},
    {"name": "Salmon Teriyaki Plate", "price": 16.50, "desc": "Glazed salmon, rice, broccoli"},
]


def main(request):
    return render(request, "restaurant/main.html")


def order(request):
    special = random.choice(DAILY_SPECIALS)
    context = {
        "menu": MENU,
        "ramen_addons": RAMEN_ADDONS,
        "daily_special": special,
    }
    return render(request, "restaurant/order.html", context)


def confirmation(request):
    if request.method != "POST":
        return render(request, "restaurant/confirmation.html", {
            "error": "Please place an order using the order form."
        })

    special_name = request.POST.get("daily_special_name", "Daily Special")
    special_price = float(request.POST.get("daily_special_price", "0"))

    ordered_items = []
    total = 0.0

    selected_keys = set(request.POST.getlist("items"))
    for item in MENU:
        if item["key"] in selected_keys:
            ordered_items.append({"name": item["name"], "price": item["price"]})
            total += item["price"]

    addons_selected = request.POST.getlist("ramen_addons")
    if "ramen" in selected_keys:
        for ad in RAMEN_ADDONS:
            if ad["key"] in addons_selected:
                ordered_items.append({"name": f"Ramen add-on: {ad['name']}", "price": ad["price"]})
                total += ad["price"]

    if request.POST.get("daily_special") == "on":
        ordered_items.append({"name": special_name, "price": special_price})
        total += special_price

    customer = {
        "name": request.POST.get("customer_name", "").strip(),
        "phone": request.POST.get("customer_phone", "").strip(),
        "email": request.POST.get("customer_email", "").strip(),
        "instructions": request.POST.get("instructions", "").strip(),
    }

    minutes = random.randint(30, 60)
    ready_time = (datetime.now() + timedelta(minutes=minutes)).strftime("%I:%M %p").lstrip("0")

    context = {
        "ordered_items": ordered_items,
        "total": f"{total:.2f}",
        "customer": customer,
        "ready_time": ready_time,
    }
    return render(request, "restaurant/confirmation.html", context)
