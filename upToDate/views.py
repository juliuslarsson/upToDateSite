from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import RequestContext
from django.shortcuts import redirect
import json, urllib


def flickr(request):
	page = int(request.GET['page'])
	nrOfTags = page * 4

	context = 	{	'tags' : [],
					'state': 'flickr',
					'nextPage' : str(page+1)
				}

	tagsJson = GetJson({ "method" : "flickr.tags.getHotList", "count" : nrOfTags}, request.session['api_key'])
	for tag in tagsJson['hottags']['tag'][(nrOfTags-4):]:
		context['tags'].append( {'tagName' : tag['_content'], 'images' : []})

	for tag in context['tags']:
		tag['images'] = getFlickrPreviews(tag['tagName'], 4, request.session['api_key'])

	return render(request, 'upToDate/flickr.html', context)

def getFlickrPreviews(tagName, nrOfImages, api_key):
	images = []
	jsonPhotos = GetJson(  {"method" 	: "flickr.photos.search", 
							"tags" 		: tagName, 
							"per_page" 	: nrOfImages
							}, 
						api_key)

	for pic in jsonPhotos['photos']['photo']:
		jsonSizes = GetJson({"method" : "flickr.photos.getSizes", "photo_id" : pic['id']}, api_key)
		image = { 'id' : pic['id'] }
		for size in jsonSizes['sizes']['size']:
			if (size['label'] == "Large Square"):
				image['url'] = size['source']
		images.append(image)

	return images

def GetJson(addParams, api_key):

	paramsDictionary = {"api_key" 		 : api_key, 
						"format" 		 : "json",
						"nojsoncallback" : "1"}

	for key in addParams.keys():
		paramsDictionary[key] = addParams[key]

	params = urllib.urlencode(paramsDictionary)
	result = urllib.urlopen("https://api.flickr.com/services/rest/?%s" % params)
	jsonObj = json.loads(result.read())

	return jsonObj

def local(request):

	response = HttpResponse()

	context = { 'tags' : [], 'state' : 'local'}
	context['tags'].append(getLocalPreviews('kamera', 4))
	context['tags'].append(getLocalPreviews('uppsala', 4))
	context['tags'].append(getLocalPreviews('pyssel', 4))

	return render(request, 'uptodate/local.html', context)

def getLocalPreviews(tagName, nrOfImages):

	match = { 'tagName' : tagName, 'images' : []}
	localJson = json.load(open('uptodate/static/uptodate/'+tagName+'.json'))

	for i in range(0, nrOfImages):
		pic = { 'id' 	: localJson['pics'][i]['id'], 
				'url' 	: localJson['pics'][i]['urls']['smallURL'],
			  }
		match['images'].append(pic)

	return match

def start(request):
	context = {}
	return render(request, 'upToDate/start.html', context, 	context_instance = RequestContext(request))

def set_key(request):
	response = HttpResponse()

	if request.method == 'POST':
		request.session['api_key'] = request.POST['api_key']

	key = request.POST['api_key']

	params = urllib.urlencode({'method': 'flickr.test.echo', 'api_key': key, 'format' : 'json', 'nojsoncallback' : '1'})
	result = urllib.urlopen("https://api.flickr.com/services/rest/?%s" % params)
	jsonObj = json.loads(result.read())

	if jsonObj['stat'] == 'fail':
		context = { 'status' : 'Nyckel ej godkand', 'Flickr-meddelande' : jsonObj['message'] }
		response.content = json.dumps(context)
		return response
	else:
		return redirect('/../uptodate/flickr/?page=1')

def localTag(request):
	response = HttpResponse()
	params = request.GET;

	localJson = json.load(open('uptodate/static/uptodate/'+params['tagName']+'.json'))
	tag =  getLocalPreviews(params['tagName'], len(localJson['pics']))

 	match = { 'tagName' : params['tagName'], 'images' : tag['images']}

	response.content = json.dumps(match)
	response.status_code = 200
	return response

def localImage(request):
	response = HttpResponse()
	params = request.GET;

	localJson = json.load(open('uptodate/static/uptodate/'+params['tagName']+'.json'))
	match = {}
	for pic in localJson['pics']:
		if(pic['id'] == params['id']):
			match = { 	'title' 	: pic['title'], 
						'user' 		: pic['user'], 
						'bigURL' 	: pic['urls']['bigURL'], 
						'bigHeight' : pic['heights']['bigHeight'],
						'bigWidth'	: pic['widths']['bigWidth']
					}


	response.content = json.dumps(match)
	response.status_code = 200
	return response

def flickrTag(request):
	response = HttpResponse()
	params = request.GET

	match = { 	'tagName' : params['tagName'], 
				'images' : getFlickrPreviews(params['tagName'], 12, request.session['api_key']) }

	
	response.content = json.dumps(match)
	response.status_code = 200
	return response

def flickrImage(request):
	response = HttpResponse()
	params = request.GET

	sizes = GetJson({"method" : "flickr.photos.getSizes", "photo_id" : params['id']} , request.session['api_key'])
	info = GetJson({"method" : "flickr.photos.getInfo", "photo_id" : params['id']} , request.session['api_key'])

	for size in sizes['sizes']['size']:
		if (size['label'] == "Medium"):
			bigURL = size['source']
			bigHeight = size['height']
			bigWidth = size['width']

	match = { 	'title' : info['photo']['title']['_content'], 
				'user' : info['photo']['owner']['username'], 
				'bigURL' : bigURL, 
				'bigHeight' : bigHeight,
				'bigWidth' : bigWidth
			}

	response.content = json.dumps(match)
	response.status_code = 200
	return response



