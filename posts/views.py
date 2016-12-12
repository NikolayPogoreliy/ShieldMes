

# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth import get_user, logout as exit
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from posts.models import Posts
from posts.forms import PostForm, ComentForm
from django.core.context_processors import csrf


# Получаем сведения об авторе поста от цоиальных сетей
def get_author_attributes(user):
    args={}
    author = SocialAccount.objects.get(user_id=user.id)
    args['name'] = user.username                    # имя юзера, которое будет отображаться на сайте
    if author.provider == 'google':                 # ДЛЯ GOOGLа
        args['link'] = author.extra_data['link']    # ссылка на страницу юзера в социальной сети
        args['pic'] = author.extra_data['picture']  # ссылка на аватарку
    elif author.provider == 'vk':                                           # ДЛЯ Вконтакта
        args['link'] = 'http://vk.com/id' + str(author.extra_data['uid'])   # ссылка на страницу юзера в социальной сети
        args['pic'] = author.extra_data['photo']                            # ссылка на аватарку
    return args

#Пагинация
def pagination(request, posts_list):
    args={}
    paginator = Paginator(posts_list, 10)  # Show 10 posts per page

    page = request.GET.get('page')
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts_page = paginator.page(paginator.num_pages)
    args['posts'] = posts_page

    if paginator.num_pages > 7:
        if not page or int(page) < 5:
            page_to_view = paginator.page_range[0:7]
        elif int(page) >= int(paginator.num_pages) - 4:
            page_to_view = paginator.page_range[int(paginator.num_pages) - 7:int(paginator.num_pages) + 1]
        else:
            page_to_view = paginator.page_range[int(page) - 3:int(page) + 4]
    else:
        page_to_view = paginator.page_range
    args['pages_to_view'] = page_to_view
    return args


# Данные о юзере, корневые посты, юзер и необходимая форма
def get_post_data(request, action):
    form = PostForm
    args = {}
    args.update(csrf(request))
    args['form'] = form                                             # Форма для добавления/редактирования сообщения
    if action != 'noact':
        args['action'] = action                                     # Добавить или редактировать пост
    args['user'] = get_user(request)                                # Информация о юзере
    args.update(pagination(request, posts_list=Posts.objects.filter(level=0).order_by('-date')))#Посты, разбитые постранично
    return args


#Выводим все посты независимо от того, залогинился юзер или нет
def posts(request):
    return render_to_response('main.html', get_post_data(request, 'noact'))


#Выводим посты если юзер залогинился
def start_view(request):
    args = {}
    if request.user.is_authenticated():
        return render_to_response('main.html', get_post_data(request, '/addpost/'))
    else: #или страницу логина, если юзер еще не вошел на сайт
        return render_to_response('login_page.html',args)


#Добавляем пост
@login_required(login_url='/')
def addpost(request):
    if request.POST:
        form = PostForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.parent_id = 0
            author = get_user(request)
            author_data = get_author_attributes(author) #Получаем сведения об авторе от socialaccounts
            new.author_name = author_data['name']
            new.author_link = author_data['link']
            new.author_pic = author_data['pic']
            form.save()
        return redirect('/')


#Добавляем комент
@login_required(login_url='/')
def addcoment(request, parent_id):
    parent = get_object_or_404(Posts, id=parent_id) #получаем данные поста - родителя
    #Сохраняем данные в базу если форма была просабмичена
    if request.POST:
        form = ComentForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.title = ""
            new.parent_id = parent_id   #ID коментируемого поста
            new.level = parent.level + 1#Уровень вложенности (комент к посту, коммент к комменту и т.д.)

            author = get_user(request)
            author_data = get_author_attributes(author) #Получаем данные об авторе поста
            new.author_name = author_data['name']
            new.author_link = author_data['link']
            new.author_pic = author_data['pic']
            # parrent_id - ID крментируемого поста/коммента
            # mster_id - ID корневого поста - корневого поста всей ветки
            if parent.master_id:  # если комментируем коммент, копируем ID корневого поста
                new.master_id = parent.master_id
            else:                   # иначе устанавливаем ID родительского поста - т.е. корневого сообщения
                new.master_id = parent.id

            parent.coments_count += 1
            parent.save()
            form.save()

        return redirect('/')
    #Или отправляем пустую форму
    else:
        args = {}
        args.update(csrf(request))
        args['form_comment'] = ComentForm
        args.update(pagination(request, posts_list=Posts.objects.filter(level=0).order_by('-date')))#Функция возвращает посты с постраничной разбивкой
        args['post'] = parent
        args['user'] = get_user(request)
        return render_to_response('main.html', args)


def logout(request):
    exit(request)
    return redirect('/')

#Редактируем пост
@login_required(login_url='/')
def editpost(request, post_id):
    args={}
    args.update(csrf(request))
    post =get_object_or_404(Posts, id=post_id)
    if request.user.username == post.author_name:   #если залогинившийся юзер - автор поста, разрешаем редактирование
        if request.POST:
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post.save()
            return redirect('/')
        else: #если форма не была отослана на обработку
            args['form']=PostForm(instance=post)    #Посылаем заполненную форму
            args['action'] = '/editpost/'+str(post_id)+'/' #Действие, которое надо провести над формой - надо указывать, т.к. форма и шаблон для редактирования и добавления поста - один и тот же
            args.update(pagination(request, posts_list=Posts.objects.filter(level=0).order_by('-date')))#Посты для отображения
            args['user'] = get_user(request)
            return render_to_response('main.html', args)
    return redirect('/') #если залогинившийся юзер не автор поста, то редирект на главную.