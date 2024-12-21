# from django.shortcuts import redirect
# from django.contrib.auth.models import Group
# from django.contrib.auth.decorators import login_required
#
# from NewsPaper.news.models import Author
#
#
# @login_required
# def upgrade_me(request):
#     user = request.user
#     authors = Group.objects.get(name='authors')
#     if not request.user.groups.filter(name='authors').exists():
#         authors.user_set.add(user)
#     if not Author.objects.filter(author=user).exists():
#         Author.objects.create(author=user)
#     return redirect('/')