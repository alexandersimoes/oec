from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from blog.models import *

# Create your views here.
def blog_index(request):
	posts = Post.objects.current()
	return render_to_response("about/blog_home.html", {"posts": posts}, context_instance=RequestContext(request))

def blog_post_detail(request, **kwargs):

	if "post_pk" in kwargs:
		if request.user.is_authenticated() and request.user.is_staff:
			queryset = Post.objects.all()
			post = get_object_or_404(queryset, pk=kwargs["post_pk"])
		else:
			raise Http404()
	else:
		queryset = Post.objects.current()
		queryset = queryset.filter(
			published__year = int(kwargs["year"]),
			published__month = int(kwargs["month"]),
			published__day = int(kwargs["day"]),
		)
		post = get_object_or_404(queryset, slug=kwargs["slug"])

	return render_to_response("about/blog_post.html", {
		"post": post
	}, context_instance=RequestContext(request))
