import csv
from .models import Orders

import os

def scheduled_job():
    sql = 'SELECT * FROM products_orders group by product_id'
    

    writer = csv.writer('total.csv')
    for obj in Orders.objects.raw(sql):
        row = ''
        for field in obj.fields:
            row += getattr(obj, field.name) + ','
        writer.writerow(row)

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")
    scheduled_job()
    