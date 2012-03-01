from django.shortcuts import render_to_response
from atlas.languages import supported_langs
from blog.models import *

# Create your views here.
def blog_index(request):
	posts = Post.objects.current()
	return render_to_response("about/blog_home.html", {"posts": posts, "supported_langs": supported_langs})
	# return render_to_response("biblion/blog_list.html", {"posts": posts})