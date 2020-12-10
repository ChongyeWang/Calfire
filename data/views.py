from django.shortcuts import render, redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from app import settings
import os
import pandas as pd 
from django.views.decorators.csrf import csrf_protect
import mongoengine as db
import pymongo
from datetime import datetime
import numpy as np
from sklearn.neighbors import NearestNeighbors
import json
from django.core.serializers.json import DjangoJSONEncoder
from sklearn.cluster import KMeans

db.connect(
	host='mongodb+srv://test:fa7f8e8h22fr@data.fff0r.mongodb.net/Calfire?retryWrites=true&w=majority'
)


class FireEntity(db.Document):
	AcresBurned = db.StringField()
	ArchiveYear = db.StringField()
	Counties = db.StringField()
	Extinguished = db.StringField()
	Injuries = db.StringField()
	Latitude = db.StringField()
	Longitude = db.StringField()
	MajorIncident = db.StringField()
	Name = db.StringField()
	PersonnelInvolved = db.StringField()
	SearchDescription = db.StringField()
	Started = db.StringField()

	def to_json(self):
		return {
			"AcresBurned": self.AcresBurned,
			"ArchiveYear": self.ArchiveYear,
			"Counties": self.Counties,
			"Extinguished": self.Extinguished,
			"Injuries": self.Injuries,
			"Latitude": self.Latitude,
			"Longitude": self.Longitude,
			"MajorIncident": self.MajorIncident,
			"Name": self.Name,
			"PersonnelInvolved": self.PersonnelInvolved,
			"SearchDescription": self.SearchDescription,
			"Started": self.Started,
		}

def home(request):
	return render(request, 'data/home.html', 
		
	)

def result(request):
	danger = request.session['danger']
	date = request.session['date']
	lat = request.session['lat']
	lon = request.session['lon']
	return render(request, 'data/result.html', 
		{
			'danger': danger,
			'date': date,
			'lat': lat,
			'lon': lon,
		}
	)

def about(request):
	return render(request, 'data/about.html', 
		
	)

def stat(request):
	all_data = FireEntity.objects.all().order_by('Name')
	return render(request, 'data/stat.html',{'all_data': all_data})

def chart(request):
	data_2020_true = len(FireEntity.objects.filter(Started__contains='2020').filter(MajorIncident='True'))
	data_2020_false = len(FireEntity.objects.filter(Started__contains='2020').filter(MajorIncident='False'))

	data_2019_true = len(FireEntity.objects.filter(Started__contains='2019').filter(MajorIncident='True'))
	data_2019_false = len(FireEntity.objects.filter(Started__contains='2019').filter(MajorIncident='False'))

	data_2018_true = len(FireEntity.objects.filter(Started__contains='2018').filter(MajorIncident='True'))
	data_2018_false = len(FireEntity.objects.filter(Started__contains='2018').filter(MajorIncident='False'))

	data_2017_true = len(FireEntity.objects.filter(Started__contains='2017').filter(MajorIncident='True'))
	data_2017_false = len(FireEntity.objects.filter(Started__contains='2017').filter(MajorIncident='False'))

	data_2016_true = len(FireEntity.objects.filter(Started__contains='2016').filter(MajorIncident='True'))
	data_2016_false = len(FireEntity.objects.filter(Started__contains='2016').filter(MajorIncident='False'))


	date_01 = len(FireEntity.objects.filter(Started__contains='-01'))
	date_02 = len(FireEntity.objects.filter(Started__contains='-02'))
	date_03 = len(FireEntity.objects.filter(Started__contains='-03'))
	date_04 = len(FireEntity.objects.filter(Started__contains='-04'))
	date_05 = len(FireEntity.objects.filter(Started__contains='-05'))
	date_06 = len(FireEntity.objects.filter(Started__contains='-06'))
	date_07 = len(FireEntity.objects.filter(Started__contains='-07'))
	date_08 = len(FireEntity.objects.filter(Started__contains='-08'))
	date_09 = len(FireEntity.objects.filter(Started__contains='-09'))
	date_10 = len(FireEntity.objects.filter(Started__contains='-10'))
	date_11 = len(FireEntity.objects.filter(Started__contains='-11'))
	date_12 = len(FireEntity.objects.filter(Started__contains='-12'))

	context = {
		'2020_true':data_2020_true,
		'2020_false':data_2020_false,
		'2019_true':data_2019_true,
		'2019_false':data_2019_false,
		'2018_true':data_2018_true,
		'2018_false':data_2018_false,
		'2017_true':data_2017_true,
		'2017_false':data_2017_false,
		'2016_true':data_2016_true,
		'2016_false':data_2016_false,
		'date_01': date_01,
		'date_02': date_02,
		'date_03': date_03,
		'date_04': date_04,
		'date_05': date_05,
		'date_06': date_06,
		'date_07': date_07,
		'date_08': date_08,
		'date_09': date_09,
		'date_10': date_10,
		'date_11': date_11,
		'date_12': date_12,
	}
	
	return render(request, 'data/chart.html', context)

def marker(request):
	all_data = FireEntity.objects.all().values_list('Latitude', 'Longitude', 'Name', 'SearchDescription')
	print(all_data)
	all_data = json.dumps(list(all_data), cls=DjangoJSONEncoder)
	return render(request, 'data/marker.html',{'all_data': all_data})

def kMeans(request):
	all_data = FireEntity.objects.filter(Started__contains='2019')
	train_data = []
	data = []
	for index in range(0, len(all_data)):
		# 32 - 42
		# -115 - -125
		lat = float(all_data[index].Latitude)
		lon = float(all_data[index].Longitude)
		if (lat < 32.0 or lat > 42.0):
			continue
		if (lon < -125.0 or lon > -115.0):
			continue
		train_data.append([lat, lon])
		data.append((lat, lon))

	X = np.array(train_data)
	kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
	center = kmeans.cluster_centers_
	result = kmeans.predict(train_data)
	result = [int(i) for i in result]
	print(len(result))

	# all_data = FireEntity.objects.all().values_list('Latitude', 'Longitude')
	# all_data = json.dumps(list(all_data), cls=DjangoJSONEncoder)

	print(len(all_data))

	equipment = []
	equipment.append((38.8, -120.8))
	equipment.append((39.52, -121.56896))
	equipment.append((36.77, -119.7))
	equipment.append((40.59, -124.146))
	equipment.append((40.31, -120.969))
	equipment.append((37.5, -119.988))
	equipment.append((39.35, -123.32))
	equipment.append((39.22, -121.0006))
	equipment.append((36.2, -121.130476))


	data = json.dumps(list(data), cls=DjangoJSONEncoder)
	result = json.dumps(result, cls=DjangoJSONEncoder)

	equipment = json.dumps(equipment, cls=DjangoJSONEncoder)



	# data = []
	# result = []
	# equipment = []

	return render(request, 'data/kMeans.html',{'all_data': data, 'result': result, 'equipment': equipment})

def get_map(request):

	if request.method == 'POST':

		data = request.body
		data = data.decode(encoding='UTF-8')
		data_list = data.split('&')
		target_lat = float(data_list[0].split('=')[1])
		target_lon = float(data_list[1].split('=')[1])

		today = datetime.today()
		year = today.year
		filter_date = '-'
		month = today.month
		if (month < 10):
			filter_date += '0' + str(month)
		else:
			filter_date += str(month)

		request.session['date'] = str(today)
		request.session['lat'] = str(target_lat)
		request.session['lon'] = str(target_lon)

		all_data = FireEntity.objects.filter(Started__contains=filter_date)
		print(all_data)

		# all_data = FireEntity.objects.all()

		# 32 - 42
		# -115 - -125
		train_data = []
		for index in range(0, len(all_data)):
			lat = int(float(all_data[index].Latitude))
			lon = int(float(all_data[index].Longitude))
			train_data.append([lat, lon])

		print(train_data)

		neigh = NearestNeighbors(n_neighbors=10, radius=1)
		neigh.fit(train_data)


		result = neigh.kneighbors([[target_lat, target_lon]], 10, return_distance=False)
		
		print(result)
		major_true = 0
		major_false = 0
		for index in result[0]:
			if all_data[int(index)].MajorIncident == 'True':
				major_true += 1
			else:
				major_false += 1
		print(major_true)
		print(major_false)

		
		if major_true > major_false:
			request.session['danger'] = 'High'
		else:
			request.session['danger'] = 'Low'
		return render(request, 'data/map.html')

	return render(request, 'data/map.html')

# Create your views here.
def create_database(request):

	# file = os.path.join(settings.STATIC_ROOT, 'calfire_data.csv')
	# data = pd.read_csv(file) 
	# for index, row in data.iterrows():
	# 	fire = FireEntity(
	# 		AcresBurned = str(row['AcresBurned']),
	# 		ArchiveYear = str(row['ArchiveYear']),
	# 		Counties = str(row['Counties']),
	# 		Extinguished = str(row['Extinguished']),
	# 		Injuries = str(row['Injuries']),
	# 		Latitude = str(row['Latitude']),
	# 		Longitude = str(row['Longitude']),
	# 		MajorIncident = str(row['MajorIncident']),
	# 		Name = str(row['Name']),
	# 		PersonnelInvolved = str(row['PersonnelInvolved']),
	# 		SearchDescription = str(row['SearchDescription']),
	# 		Started = str(row['Started']),
	# 	)
	# 	fire.save()
	print(FireEntity.objects.all()[0].Counties)

	return render(request, 'data/index.html')



