from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer


def _random_joke():
    return Joke.objects.order_by("?").first()


def _random_picture():
    return Picture.objects.order_by("?").first()


def home(request):
    context = {
        "joke": _random_joke(),
        "picture": _random_picture(),
    }
    return render(request, "dadjokes/random.html", context)


def random_item(request):
    context = {
        "joke": _random_joke(),
        "picture": _random_picture(),
    }
    return render(request, "dadjokes/random.html", context)


def jokes_list(request):
    jokes = Joke.objects.all().order_by("-created_at")
    return render(request, "dadjokes/jokes.html", {"jokes": jokes})


def joke_detail(request, pk):
    joke = get_object_or_404(Joke, pk=pk)
    return render(request, "dadjokes/joke_detail.html", {"joke": joke})


def pictures_list(request):
    pictures = Picture.objects.all().order_by("-created_at")
    return render(request, "dadjokes/pictures.html", {"pictures": pictures})


def picture_detail(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    return render(request, "dadjokes/picture_detail.html", {"picture": picture})


@api_view(["GET"])
def api_root(request):
    joke = _random_joke()
    if not joke:
        return Response({"detail": "No jokes found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(JokeSerializer(joke).data)


@api_view(["GET"])
def api_random(request):
    joke = _random_joke()
    if not joke:
        return Response({"detail": "No jokes found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(JokeSerializer(joke).data)


@api_view(["GET", "POST"])
def api_jokes(request):
    if request.method == "GET":
        jokes = Joke.objects.all().order_by("-created_at")
        return Response(JokeSerializer(jokes, many=True).data)

    serializer = JokeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def api_joke(request, pk):
    joke = get_object_or_404(Joke, pk=pk)
    return Response(JokeSerializer(joke).data)


@api_view(["GET"])
def api_pictures(request):
    pictures = Picture.objects.all().order_by("-created_at")
    return Response(PictureSerializer(pictures, many=True).data)


@api_view(["GET"])
def api_picture(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    return Response(PictureSerializer(picture).data)


@api_view(["GET"])
def api_random_picture(request):
    picture = _random_picture()
    if not picture:
        return Response({"detail": "No pictures found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(PictureSerializer(picture).data)
