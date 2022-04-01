from store.models import *

def person_data(request):
	try:
		person = Persona.objects.get(user = request.user)
	except:
		person = Persona()
	return person

def my_processor(request):
	context = { 'ctx_persona':person_data(request),
	}
	return context