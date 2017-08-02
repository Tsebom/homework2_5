import os
import subprocess
from queue import Queue
from threading import Thread

queue_conveert = Queue() # Очередь FIFO

def directory_file(way = ''):
	"""Абсолютный путь к фаилу, аргумент - (путь от директории с __file__)"""
	file = os.path.join(os.path.dirname(os.path.abspath(__file__)), way)
	return file

def build_direcrory(directory):
	"""Проверяет существование директории и если нет то создает ее, аргумент - (требуемая директория)"""
	if directory not in os.listdir(directory_file()):
		os.mkdir(directory_file(directory))

def subprocess_convert(list_way):
	"""Вызывает программу Image Magick, аргумент - (список путей к исходному и коненчному фаилам)"""
	subprocess.call('convert ' + list_way[0] + ' -resize 200 ' + list_way[1])

def way_files(list_file):
	"""Генерируе данные для subprocess_convert, аргумент - (список исходных фаилов)"""
	for file_jpg in list_file:
		convert_file = directory_file('Source\\' + file_jpg) # Конвертируемый фаил
		result_file = directory_file('Result\\' + file_jpg) # Результат	
		yield [convert_file, result_file]

def convert_process():
	"""Вызывает процесс в потоке"""
	while True:
		list_way = queue_conveert.get()
		subprocess_convert(list_way)
		queue_conveert.task_done()

def main():
	build_direcrory('Result') # Создаем папку Result

	file_source = os.listdir(directory_file('Source')) # Список фаилов в папке Source

	quantity_threads = 4 # Колличество потоков 
	
	# Запускаем потоки
	for flow in range(quantity_threads):
		t = Thread(target = convert_process)
		t.setDaemon(True)
		t.start()
	# Заполняем очередь
	for list_ways in way_files(file_source):
		queue_conveert.put(list_ways)

	queue_conveert.join()

main()