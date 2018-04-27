from __future__ import absolute_import, unicode_literals
from .celery import app
from random import randint
import random
from pharmacy_app.models import Medicine, MedicineCategory, MedicineUnit, MedicineSale
import datetime


@app.task
def add_to_stock():
    print("Adding items to stock...")
    medicines = sorted(Medicine.objects.all().order_by('id'), key=lambda x: random.random())
    size = len(medicines)
    num_rand_to = randint(0, size)
    iter_list = list(range(0, num_rand_to))
    now = datetime.datetime.now()
    today_date = "{0}-{1}-{2}".format(now.year, now.month, now.day)
    for i in iter_list:
        medicine = medicines[i]
        num_rand_to_add = randint(0, 10)
        iter_list_add = list(range(0, num_rand_to_add))
        for _ in iter_list_add:
            medicine_unit = MedicineUnit(medicine=medicine, status='a', date_added=today_date,
                                         date_updated=today_date)
            medicine_unit.save()


@app.task
def add_medicines():
    print("Adding medicines in progress...")
    lines = []
    with open("pharmacy_app/static/medicines.csv") as f:
        for line in f:
            line_spl = line.split(",")
            lines.append(line_spl)
    size = len(lines)
    num_rand = randint(0, size)
    direct = randint(0, 1)
    if direct == 0:
        iter_list = list(range(0, num_rand))
    else:
        iter_list = list(range(size - 1, num_rand - 1, -1))
    # print("Iter list: ", iter_list)
    for i in iter_list:
        line = lines[i]
        # print("Line: ", line)
        name = line[0]
        producer = line[1]
        url = line[2]
        category_name = line[3]
        price = float(line[4])

        if Medicine.objects.filter(name=name).count() == 0:
            print("Adding medicine to database")
            category = MedicineCategory.objects.filter(name=category_name)[0]
            now = datetime.datetime.now()
            today_date = "{0}-{1}-{2}".format(now.year, now.month, now.day)

            medicine = Medicine(name=name, producer=producer, url=url, category=category,
                                date_added=today_date, date_updated=today_date, price=price,
                                count=0)
            medicine.save()


@app.task
def generate_sales():
    print("Generating sales...")
    medicines = sorted(Medicine.objects.all().order_by('id'), key=lambda x: random.random())
    size = len(medicines)
    num_rand_to = randint(0, size)
    iter_list = list(range(0, num_rand_to))
    now = datetime.datetime.now()
    today_date = "{0}-{1}-{2}".format(now.year, now.month, now.day)
    today_time = "{0}:{1}".format(now.hour, now.minute)
    for i in iter_list:
        medicine = medicines[i]
        med_unit_cnt = MedicineUnit.objects.filter(medicine=medicine, status='a').count()
        num_rand_sale = randint(0, int(med_unit_cnt/2))
        if num_rand_sale == 0:
            continue
        med_units = MedicineUnit.objects.filter(medicine=medicine, status='a')
        counter = 0
        for med_unit in med_units:
            counter += 1
            if counter > num_rand_sale:
                break
            med_unit.status = 's'
            med_unit.save()

        amount = float(num_rand_sale) * medicine.price
        sale = MedicineSale(medicine=medicine, items_count=num_rand_sale, amount=amount,
                            purchase_date=today_date, purchase_time=today_time)
        sale.save()
