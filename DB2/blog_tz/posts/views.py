from django.shortcuts import render




def MainTestView(request):
	return render(request, 'posts/main.html', {'info':'New redirect info is here'})