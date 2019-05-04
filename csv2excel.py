#!/usr/bin/python

import os
import glob
import csv
import xlwt # from http://www.python-excel.org/
import datetime

csvfile=datetime.date.today().strftime("%Y%m%d") + "/Connected-" + datetime.date.today().strftime("%Y%m%d")

wb = xlwt.Workbook()
ws = wb.add_sheet('data')
with open(csvfile + ".csv", 'rb') as f:
    reader = csv.reader(f)
    for r, row in enumerate(reader):
        for c, val in enumerate(row):
            ws.write(r, c, val)
wb.save(csvfile + '.xls')
