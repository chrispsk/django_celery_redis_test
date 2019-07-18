from __future__ import absolute_import, unicode_literals
import random
from celery.decorators import task
from .models import Billing
import time

@task(name="sum_two_numbers")
def add(x, y):
    return x + y


@task(name="multiply_two_numbers")
def mul(x, y):
    number_1 = x
    number_2 = y * random.randint(3, 100)
    total = number_1 * number_2
    Billing.objects.create(number_1=number_1, number_2=number_2, total=total)
    return total

@task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)

@task # merge si fara paranteze (afiseaza alt nume gen: billing.tasks.abcsum)
def abcsum(numbers):
    tot = sum(numbers)
    time.sleep(5)
    return tot
