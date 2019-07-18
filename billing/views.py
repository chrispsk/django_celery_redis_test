from django.shortcuts import render
from .tasks import abcsum, mul
from django.http import HttpResponse
import time

def home(request):
    total = abcsum.delay([2,9])
    # time.sleep(1)
    return HttpResponse(total.get()) # get() to return from task when finishes

def heavy(request):
    hey = mul.delay(32131,54353245)
    return HttpResponse("base... Check Database")
