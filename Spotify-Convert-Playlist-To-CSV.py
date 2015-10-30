import sys
import os
from urllib2 import urlopen
from bs4 import BeautifulSoup
import csv

inputFile = ""
outputFile = ""

def readFile():
	spotify_urls = []
	if os.path.isfile(inputFile):
		with open(inputFile, 'r') as f:
			data = f.read()
		spotify_urls = data.split('\n')
	else:
		print "Input file not found!"
	return spotify_urls

def readArguments(args):
	global inputFile
	global outputFile
	if len(args) < 2:
		return "missing"
	elif len(args) == 2:
		inputFile = args[1]
		return "input"
	elif len(args) == 3:
		inputFile = args[1]
		outputFile = args[2]
		return "both"

def getSongInfo(url):
	print "URL: " + url
	response = urlopen(url).read()
	soup = BeautifulSoup(response, "html.parser")
	artist = soup.find("a", { "class" : "button owner-action"}).text.encode("utf-8")
	track_name = soup.find("h1", {"class" : "h-title"}).text.encode("utf-8")
	print "Artist: " + artist + ", Track Name: " + track_name
	return {'track name' : track_name,
			'artist' : artist}

def printToOutputFile(songs):
	headers = ['track name', 'artist']
	with open(outputFile, 'w') as csvfile:
		for song in songs:
			print "Writing " + song['track name']
			csv_writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=song)
			csv_writer.writerow(song)


def process():
	songs = []
	spotify_urls = readFile()
	for url in spotify_urls:
		songs.append(getSongInfo(url))
	printToOutputFile(songs)

mode = readArguments(sys.argv)
if mode == "missing":
	print "Missing input file name"
	sys.exit("1")
elif mode == "input":
	outputFile = os.path.join(os.path.dirname(inputFile), "spotify_output.csv")
	print outputFile
process()
print "Done."