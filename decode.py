#!/usr/bin/python3

import base64
import sys
from datetime import datetime, timedelta

with open(sys.argv[1]) as f:
	for url in f:
		data = url.split("=")[1]
		segments = data.split("-")
		segments = base64.b64decode(data,"-?")
		print("Start")
		print(f"{segments[0]:02x}")
		astr = segments[1:20].decode('ascii')
		dt = datetime.strptime(astr[:12],"%Y%m%d%H%M")
		dt = dt.replace(month = dt.month+1)
		print(dt)
		serial = astr[12:]
		print(serial)
		for b in segments[20:227]:
			print(f"{b:02x}", end="")

		segments = segments[227:]
		print("\nYear")
		total = 0
		date = dt
		for i in range(13):
			hours = segments[2*i]+segments[2*i+1]*256
			print(f"{date.strftime('%b')}: {hours}")
			date = date.replace(month=(date.month+1)%12+1)
			total += hours
		print(f"Total: {total}")
		print("\nWeek")
		date = dt  - timedelta(days=7)
		for i,b in enumerate(segments[26:34]):
			print(f"{date.strftime('%a')}: {b}", end="; ")
			date = date + timedelta(days=1)
		print("\nMonth")
		date = dt - timedelta(days=31)
		for i,b in enumerate(segments[34:-4]):
			print(f"{date.day}.{date.month}.	{b}")
			date = date + timedelta(days=1)
		print("Rest")
		for b in segments[-4:]:
			print(f"{b:02x}")

		#print(segments)
