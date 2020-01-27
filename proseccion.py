# import the necessary packages
import os
import sys
from utilidades.centroidtracker import CentroidTracker
from utilidades.trackableobject import TrackableObject
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2


import csv
from datetime import datetime
import subprocess

import settings

## 
# ancho de la imagen
IM_WIDTH = 500

## sectores de la tienda
sectors = {	#sector		start(x, y)					end(x, y)
			'pasillo': ((IM_WIDTH // 3,0), 			(IM_WIDTH * 2 // 3, 300)),		#
			'tienda1': ((0,0), 						(IM_WIDTH// 3, 100)),
			'tienda2': ((0,100), 					(IM_WIDTH// 3, 200)),
			'tienda3': ((0,200), 					(IM_WIDTH// 3, 300)),
			'tienda4': ((IM_WIDTH * 2 // 3, 0), 	(IM_WIDTH, 100)),
			'tienda5': ((IM_WIDTH * 2 // 3, 100), 	(IM_WIDTH, 200)),
			'tienda6': ((IM_WIDTH * 2 // 3, 200), 	(IM_WIDTH, 300))
}

## funciones utiles


def in_rect(position, start, end):
	return position[0] >= start[0] and position[0] <= end[0] and position[1] >= start[1] and position[1] <= end[1]

def get_sector(position, sectors):
	for sector, (start, end) in sectors.items():
		if in_rect(position, start, end):
			return sector

def send_file(file):
	print("[INFO] enviando archivo {} a servidor remoto{}".format(file, settings.HOST))
	# command: sshpass -p "password" scp -r user@example.com:/some/remote/path /some/local/path

	p = subprocess.Popen(['sshpass', '-p', '{}'.format(settings.PASS), 
						'scp', '-r', file,
						'{}@{}:{}'.format(settings.USER, settings.HOST, settings.REMOTE_PATH)], stdout=subprocess.PIPE)
	# process = Popen(["ls", "-la", "."], stdout=PIPE)
	# (output, err) = p.communicate()
	while p.poll() is None:
		out = p.stdout.read(1)
		sys.stdout.write(out.decode('utf-8'))
		sys.stdout.flush()

	exit_code = p.wait()
	print("[INFO] error code: {}".format(exit_code))
	# print(output)
	# print('--------------')
	# print(err)
	# sts = os.waitpid(p.pid, 0)



# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-i", "--input", type=str,
	help="path to optional input video file")
ap.add_argument("-c", "--confidence", type=float, default=0.4,
	help="minimum probability to filter weak detections")
ap.add_argument("-s", "--skip-frames", type=int, default=30,
	help="# of skip frames between detections")
ap.add_argument("-o", "--out", type=str, default="data",
	help="path to output positions files")	
args = vars(ap.parse_args())

# clases de la red neuronal
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

# cargar modelo
print("[INFO] Cargando modelo...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# creando archivo de registro
print("[INFO] Creando archivo de registro...")
# crear carpeta si no existe
if not os.path.exists(args['out']):
        os.makedirs(args['out'])

columnas=['timestamp','object_id','position_x', 'position_y']
columnas=['anho','mes','dia','hora','object_id','position_x', 'position_y','sector']


out_filename = datetime.now().strftime('%d%m%Y_%H:%M:%S') + '.csv'
out_file = os.path.join(args['out'], out_filename)

sent = False
with open(out_file, 'a') as f:
    writer = csv.writer(f)
    writer.writerow(columnas)

print("[INFO] archivo creado: " + out_file)

if not args.get("input", False):
	print("[INFO] iniciando camara...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

else:
	print("[INFO] abriendo archivo...")
	vs = cv2.VideoCapture(args["input"])

# dimensiones del frame
W = None
H = None

# iniciar tracker
ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
trackers = []
trackableObjects = {}

# variables para contar personas
totalFrames = 0
totalDown = 0
totalUp = 0

# estimador de fps
fps = FPS().start()


# para cada frame
while True:
	# lectura del frame
	frame = vs.read()
	frame = frame[1] if args.get("input", False) else frame

	# fin del video
	if args["input"] is not None and frame is None:
		break

	
	frame = imutils.resize(frame, width=IM_WIDTH)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# guardar las dimensiones
	if W is None or H is None:
		(H, W) = frame.shape[:2]

	# estado del programa
	status = "Waiting"
	rects = []

	# verificar si debemos correr el detector
	if totalFrames % args["skip_frames"] == 0:
		# inicializacion del detector
		status = "Detecting"
		trackers = []

		# convertir la imagen en un blob para pasar a la red neuronal
		blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
		net.setInput(blob)
		detections = net.forward()

		# para cada deteccion
		for i in np.arange(0, detections.shape[2]):
			# extraer la confianza
			confidence = detections[0, 0, i, 2]

			# filtrar detecciones debiles
			if confidence > args["confidence"]:
				# extraer indice de la clase
				idx = int(detections[0, 0, i, 1])

				# corresponder con la deteccion de personas
				if CLASSES[idx] != "person":
					continue

				# calcular la region de la deteccion
				box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
				(startX, startY, endX, endY) = box.astype("int")

				# contruir una region para el trackeo con dlib
				tracker = dlib.correlation_tracker()
				rect = dlib.rectangle(startX, startY, endX, endY)
				tracker.start_track(rgb, rect)

				# agregar los trackers
				trackers.append(tracker)
				# calcular la hora actual

		csv_data = []	

		# guardar datos de seguimiento
		for (objectID, centroid) in ct.objects.items():
			# object_timestamp = datetime.now().strftime('%d%m%Y_%H:%M:%S')
			year = datetime.now().strftime('%Y')
			month = datetime.now().strftime('%m')
			day = datetime.now().strftime('%d')
			hour = datetime.now().strftime('%H:%M:%S')
			
			# si existe el objeto en la lista
			to = trackableObjects.get(objectID, None)
			# 'timestamp','object_id','position_x', 'position_y'
			for cent in to.centroids:
				sector = get_sector(cent, sectors)
				csv_data.append([year, month, day, hour, objectID, cent[0], cent[1], sector])

		#escribir archivo
		with open(out_file, 'a') as f:
			writer = csv.writer(f)
			for row in csv_data:
				writer.writerow(row)
	# seguir con el tracking
	else:
		# para cada tracker
		for tracker in trackers:
			# estado del programa
			status = "Tracking"

			# actualizar los trackers
			tracker.update(rgb)
			pos = tracker.get_position()

			# recuperar la posicion
			startX = int(pos.left())
			startY = int(pos.top())
			endX = int(pos.right())
			endY = int(pos.bottom())

			# agregar las regiones
			rects.append((startX, startY, endX, endY))

	# usar el tracker de centroide
	objects = ct.update(rects)

	# para cada objeto
	for (objectID, centroid) in objects.items():
		# si existe el objeto en la lista
		to = trackableObjects.get(objectID, None)

		# si no, crear una nueva entrada
		if to is None:
			to = TrackableObject(objectID, centroid)

		else:
			# la diferencia en el eje y nos dice la direccion
			y = [c[1] for c in to.centroids]
			direction = centroid[1] - np.mean(y)
			to.centroids.append(centroid)

			# verificar si ya ha sido contado
			if not to.counted:
				# si la direccion es negativa
				if direction < 0 and centroid[1] < H // 2:
					totalUp += 1
					to.counted = True

				# si la direccion es positiva
				elif direction > 0 and centroid[1] > H // 2:
					totalDown += 1
					to.counted = True

		trackableObjects[objectID] = to

		# plotear el id y el centroide
		text = "PER {}".format(objectID)
		cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

		sector = get_sector(centroid, sectors)

		cv2.putText(frame, sector, (centroid[0] - 10, centroid[1] + 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

		
		N_TRACE = 60	
		plot_centroids = to.centroids if len(to.centroids) < N_TRACE else to.centroids[-N_TRACE:]
		# dibujar las ultimas posiciones
		for i in range(0,len(plot_centroids),4):
			cv2.circle(frame, (plot_centroids[i][0], plot_centroids[i][1]), 4, (0, 255, 0), -1)

		# Guardar las posiciones en un archivo csv

	for sector, (start, end) in sectors.items():
		# print(start)
		cv2.rectangle(frame, start, end, (0,255,255),2)
	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		# enviar archivo
		send_file(out_file)
		# borrar archivo
		if os.path.exists(out_file):
			os.remove(out_file)
		sent = True
		break

	# increment the total number of frames processed thus far and
	# then update the FPS counter
	totalFrames += 1
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


# if we are not using a video file, stop the camera video stream
if not args.get("input", False):
	vs.stop()

# otherwise, release the video file pointer
else:
	vs.release()

# close any open windows
cv2.destroyAllWindows()
# send file

if not sent:
	send_file(out_file)
	if os.path.exists(out_file):
			os.remove(out_file)