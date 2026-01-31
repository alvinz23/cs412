from django.shortcuts import render
import random

QUOTES = [
    "I wasn’t willing to sacrifice my game, but I also wasn’t willing to sacrifice my family time. So I decided to sacrifice sleep, and that was that.",
    "Good coaches tell you where the fish are, great coaches teach you how to find them.",
    "Rest at the end, not in the middle.",
]

IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/9/92/Kobe_Bryant_at_Pirates_3_premiere.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/4/46/Kobe_B_Bryant.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/5/5f/Kobe_Bryant_Drives2.jpg",
]


def quote(request):
    context = {
        "quote": random.choice(QUOTES),
        "image": random.choice(IMAGES),
    }
    return render(request, "quotes/quote.html", context)

def show_all(request):
    context = {
        "quotes": QUOTES,
        "images": IMAGES,
    }
    return render(request, "quotes/show_all.html", context)

def about(request):
    return render(request, "quotes/about.html")
