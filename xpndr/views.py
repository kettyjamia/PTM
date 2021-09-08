from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .models import Comment,Transponder,Satellite
from .forms import  CommentForm
from .filters import CommentFilter

#TODO PDF generate nginx gunnicorn 
# active filter Truefalse....activeresolver   search button enable with text .....edit existing form......delete in edit button.....
# portal details.html footerflex

@login_required
def new_comment(request):
    form=CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            form=form.save(commit=False)
            # automatically set the user as logged in user .....when a form is created
            form.user=request.user
            print(form.user)
            form.save()
            return comment_list(request) #return to comment_list all comments page
        else:
            print("ERROR FORM INVALID")
    else:
        form = CommentForm(initial={'user':request.user})  # new form to the user
    return render(request,'xpndr/post/form.html',{'form':form}) 

@login_required
def update_post(request,pk):
    comment=Comment.objects.get(id=pk)
    form=CommentForm(instance=comment)
    if request.method == 'POST':
        print("POST method")
        form = CommentForm(request.POST,request.FILES,instance=comment)
        # form = CommentForm(data=request.POST)
        if form.is_valid():
            # Save the comment to the database
            form.save(commit=True)
            return comment_list(request) #return to comment_list all comments page
        else:
            print("ERROR FORM INVALID")
    else:
        print("get method")
        form = CommentForm(instance=comment)  # new form to the user
    return render(request,'xpndr/post/update_post.html',{'form':form})   

# all posts list with search filter
@login_required
def comment_list(request):
    comment = Comment.objects.all()
    myFilter=CommentFilter(request.GET,queryset=comment)
    comment=myFilter.qs
    return render(request,'xpndr/post/list.html',{'comment': comment,'myFilter':myFilter,'heading':'All Complaints'})

# all active posts list with search filter
@login_required
def comment_active(request):
    comment = Comment.objects.all().filter(active=True)
    myFilter=CommentFilter(request.GET,queryset=comment)
    comment=myFilter.qs
    return render(request,'xpndr/post/list.html',{'comment': comment,'myFilter':myFilter,'heading':'Active'})

# all active posts list with search filter
@login_required
def comment_inactive(request):
    comment = Comment.objects.all().filter(active=False)
    myFilter=CommentFilter(request.GET,queryset=comment)
    comment=myFilter.qs
    return render(request,'xpndr/post/list.html',{'comment': comment,'myFilter':myFilter,'heading':'Inactive'})


#full detail of comment post
@login_required
def comment_detail(request,pk):
    comment = get_object_or_404(Comment,id=pk)                           
    return render(request,'xpndr/post/detail.html',{'comment': comment})


@login_required
def comment_delete(request,pk):
    if request.method == 'POST':    
        comment=Comment.objects.get(pk=pk)
        comment.delete()
        # return render(request,'xpndr/post/list.html')
    return redirect('xpndr:comment_list',)

#search based on satellite select
""" @login_required
def sat_detail(request):
    form=SatDetailForm(   )
    query=None
    result=[]
    if request.method == 'POST':
    # if 'query' in request.GET:
        form = SatDetailForm(data=request.POST)
        if form.is_valid():
            # query = form.cleaned_data['form']
            print(query)
            # comment = Comment.objects.all()
            comment = Comment.objects.filter(satellite=request.POST['satellite'])
            # comment = comment.object.filter(Satellite=form['satellite'].value())   .                                
            # Save the comment to the database
            # print(form.cleaned_data.get("satellite"))
            # selected_choice = Comment.choice_set.get(pk=request.POST['satellite'])
            # comment = Comment.objects.get(satellite='4')
            # comment = get_object_or_404(Comment, 'GSAT4')
            # comment = get_object_or_404(Comment, pk=request.POST['satellite'])
            # print(comment)
            # pk=request.POST["satellite"]
            # print(pk)
            # form.save(commit=True)
            return render(request,'xpndr/post/list.html',{'comment': comment})
        else:
            print("ERROR FORM INVALID")
    else:
        form = SatDetailForm()  # new form to the user
    return render(request,'xpndr/post/sat_detail.html',{'form':form})
    # try:
    #     selected_choice = comment.satellite_set.get(pk=request.POST['satellite'])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the question voting form.
    # return render(request,'xpndr/post/list.html',{'comment': comment})
    # else:
    #     return HttpResponseRedirect("error sat_detail view")
        # return HttpResponseRedirect(reverse('polls:results', args=(question.id,))) """


    #     def delete_book(request, pk):
    # if request.method == 'POST':
    #     book = Book.objects.get(pk=pk)
    #     book.delete()
    # return redirect('book_list')




# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'