from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.response import TemplateResponse
from dashboards.models import User, Dashboard
from django.core.mail import send_mail
from dashboards.forms import ContactForm, UploadForm, Login, Register, Download, Delete, Published, Unpublish
import os
import datetime
import shutil


#the following four functions are called when HTTPResponceRedirect is object is returned
#define a function that produces an HTTPResponse object with 'thank you' message
def thanks(request):
    return HttpResponse('Thank you')
#define a function that produces an HTTPResponse object with error message
def error_message(request):
    return HttpResponse('Something went wrong. You either provided a wrong name or login/password information')
#define a function that produces an HTTPResponse object with 'password doesn't match' message
def error_login(request):
    return HttpResponse('Your passwords don\'t match')
#define a function that produces an HTTPResponse object with 'successfully created profile' message
def success(request):
    return HttpResponse('Your profile has been successfully created! Please<a href=%s> login here</a>:'
                        %request.META.get('HTTP_REFERER')[:-9])

#render user_dashboards.html which will display dashboards, list of dashboards for deletion, publication and 'unpublishing'
def my_dashboards(request):
    #check whether user id is in request.session dictionary-like object; i.e. user's session is running
    if request.session.get('member_id'):
        url_list = []
        url_published_list = []
        delete_list = []
        unpublish = []
        # a QuerySet (user_dashboards) of all the Dashboard objects for current user represented by request.session['member_id'] is returned
        user_dashboards = Dashboard.objects.filter(author = request.session['member_id'])
        user_published_dashboards = Published.objects.filter(id_user_id = request.session['member_id'])
        counter = 0
        #populate array of tuples: counter 1 to N and dashboard title (from the database)
        url= "path to media directory on the server"+request.session['directory']+'/'
        url_published = "path to 'publish' directory on the server"
        url_intranet = "path to 'publish' on Intranet directory on the server"
        for dash in user_dashboards:
            counter=counter + 1
            url_list.append((counter, url , dash.file_name, dash.title, dash.status, dash.type, dash.resource))
            delete_list.append((counter, dash.title + '(' + dash.file_name + ')'))
        #instantiate check_box form with a list of dashboards to be deleted
        check_box = Delete(request.GET, url_list=delete_list)

        counter = 0
        for dash_p in user_published_dashboards:
            counter=counter + 1
            unpublish.append((counter, dash_p.dashboard))
            url_published_list.append((counter, url_published, dash_p.dashboard, dash_p.name, url_intranet, dash_p.resource))

        if check_box.is_valid():
            number_choice = request.GET['check_box']
            #print number_choice
            number_choice_int = int(number_choice)
            title_all = url_list[number_choice_int-1]
            title = title_all[3]
            dashboard_object = Dashboard.objects.filter(title=title)
            dashboard_object.delete()
            return HttpResponseRedirect('full path/my_dashboards/')
        #instantiate unpublish_list form with a list of dashboards to be unpublished (for display only)
        unpublish_list = Unpublish(request.GET, unpublished_list = unpublish)
        return render_to_response('forms/user_dashboards.html', {'url_list':url_list, 'delete':check_box, 'publish': check_box,
                                                                 'unpublish':unpublish_list, 'url_published_list':url_published_list})

    else:
        return TemplateResponse(request, 'redirect_template.html', {'redirect_url':'full path to root/'})

#function to publish a selected dashboard from drop-down list dashboard
def publish(request):
    #check whether user id is in request.session dictionary-like object; i.e. user's session is running
    if request.session.get('member_id'):
        url_list = []
        publish_list = []
        # a QuerySet (user_dashboards) of all the Dashboard objects for current user represented by request.session['member_id'] is returned
        user_dashboards = Dashboard.objects.filter(author = request.session['member_id'])
        counter = 0
        for dash in user_dashboards:
            counter=counter + 1
            url_list.append((counter, dash.file_name, dash.title, dash.status, dash.type, dash.resource))
            publish_list.append((counter, dash.title + '(' + dash.file_name + ')'))
        #instantiate publish form with a list of dashboards to be published: 'publish_list'
        publish = Delete(request.GET, url_list=publish_list)
        #check whether form is valid (data fields/types match)
        if publish.is_valid():
            #get number_choice, i.e. the user's selection
            number_choice = request.GET['check_box']
            number_choice_int = int(number_choice)
            title_all = url_list[number_choice_int-1]
            title = title_all[2]
            #extract a dashboard record based on its title
            dashboard_object = Dashboard.objects.filter(title=title)
            #copy recently created files from publish directory to my_dashboards. From my_dashboards
            #the files are copied into 'root to /publish/' where a cron job
            #is constantly running (my_synker2)
            shutil.copyfile(os.path.join(os.path.dirname(__file__),'../publish/'+dashboard_object[0].file_name),
                            'path on server'+dashboard_object[0].file_name)
            #check the database whether the published dashboard is already there, so user won't publish two dashboards
            #with the same file name and same dashboard name
            if(Published.objects.filter(id_user_id=request.session['member_id'], dashboard = dashboard_object[0].file_name,
                                        name=dashboard_object[0].title)):
                pass
            else:
                #save dashboard in the db if it's not a clone
                published_dash = Published(id_user_id=request.session['member_id'], dashboard = dashboard_object[0].file_name,
                                           name=dashboard_object[0].title, resource=dashboard_object[0].resource)
                published_dash.save()
            return HttpResponse('You successfully published a dashboard! Please click on any link to '
                            'path to root">continue</a>.')
    else:
        return TemplateResponse(request, 'redirect_template.html', {'redirect_url':'path to root'})

#function to unpublish a selected dashboard from drop-down list dashboard
def unpublish(request):
    #check whether user id is in request.session dictionary-like object; i.e. user's session is running
    if request.session.get('member_id'):
        url_list = []
        unpublish_list = []
        # a QuerySet (user_dashboards) of all the Dashboard objects for current user represented by request.session['member_id'] is returned
        user_dashboards = Dashboard.objects.filter(author = request.session['member_id'])
        counter = 0
        for dash in user_dashboards:
            counter=counter + 1
            print dash
            url_list.append((counter, dash.file_name, dash.title, dash.status, dash.type, dash.resource))
            unpublish_list.append((counter, dash.title + '(' + dash.file_name + ')'))
        #instantiate unpublish form with a list of dashboards to be published: 'unpublish_list'
        unpublish = Unpublish(request.GET, unpublished_list=unpublish_list)
        #check whether form is valid (data fields/types match)
        if unpublish.is_valid():
            #get number_choice, i.e. the user's selection
            number_choice = request.GET['unpublished']
            number_choice_int = int(number_choice)
            title_all = url_list[number_choice_int-1]
            title = title_all[2]
            print "the title is : " + title
            #extract a dashboard record based on its title
            dashboard_object = Dashboard.objects.filter(title=title)
            #move the selected dashboard from 'path to /published/'
            #to unpublished
            shutil.move('path to published dashboards dir'+dashboard_object[0].file_name,
                        os.path.join(os.path.dirname(__file__),'../unpublish/'+dashboard_object[0].file_name))
            #then delete the record from the database
            Published.objects.filter(id_user_id = request.session['member_id'], dashboard = dashboard_object[0].file_name).delete()


            return HttpResponse('You unpublished/deleted a dashboard... Please click on any link to '
                                'path to root">continue</a>.')
    else:
        return TemplateResponse(request, 'redirect_template.html', {'path to root'})

#let user to send a contact form
def contact1(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.clean_message()
            cd = form.cleaned_data
            send_mail(cd['subject'],
                      cd['message'],
                      cd.get('email', 'noreply@example.com'),
                      ['my email @gmail.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm(
            initial={'subject': "My dashboards"}
        )
    return render_to_response('forms/contact_form.html', {'form': form }, RequestContext(request))

author = ""; title=""; status=""; type=""; resource=""; file_name=""; upload_date = "";

def upload(request):
    #check whether user id is in request.session dictionary-like object; i.e. user's session is running
    if request.session.get('member_id'):
        lines = list()
        #define state variables as global variables; state variables store the user's form entries and selections
        #to be later retrieved using form = UploadForm(initial={'title': title})
        global author; global title; global status; global type; global resource; global file_name; global upload_date;
        print "before: " + title
        if request.method == "POST":
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                handle_uploaded_file(request.FILES['file'])
                u1 = User.objects.filter(id=request.session['member_id'])
                print u1
                print "and "+ str(len(u1))
                if u1 and len(u1) == 1:
                    dashboard = Dashboard(file_field = request.FILES['file']) #upload file directly into db and wait until
                    #user decides to publish it (see def publish(request) above
                    dashboard.author = User(id = u1[0].id)
                    dashboard.title = cd['title']
                    dashboard.status = cd['status']
                    dashboard.type = cd['type']
                    dashboard.resource = cd['resource']
                    #to keep versioning split name of the file
                    file_split = str(cd['file']).split('.')
                    dashboard.file_name = file_split[0] + version_prefix + '.' + file_split[1]
                    dashboard.upload_date = datetime.datetime.now()
                    #check whether dashboard already exists and alert user
                    if Dashboard.objects.filter(author=request.session['member_id']).filter(title__contains=dashboard.title):
                        author = User(id = u1[0].id)
                        title = cd['title']
                        status = cd['status']
                        type = cd['type']
                        resource = cd['resource']
                        file_name = cd['file']
                        upload_date = datetime.datetime.now()
                        lines.append("Duplicate dashboard title. Please click 'back' or 'Upload dashboard' "
                                    "and select a different name for dashboard")
                        return render_to_response('base_upload.html', {'form':form,
                                                                   'lines':lines}, RequestContext(request))
                    #if there are no duplicates of dashboard - save it in the database
                    dashboard.save()
                    return HttpResponseRedirect('/contact/thanks/')

                else:
                    return HttpResponseRedirect('/contact/error_message/')

        else:
            form = UploadForm(initial={'title': title, 'status':status, 'type':type, 'resource':resource, 'file':file_name})

            return render_to_response('base_upload.html', {'form':form,
                                                        'lines':lines}, RequestContext(request))
    else:
        #redirect template to 'top' frame. Otherwise it will remain in the same frame and each new log in will created '
        #nested cascade of frames
        return TemplateResponse(request, 'redirect_template.html', {'redirect_url':'/'})


#version of dashboard file generator
def ver_generator():
    date_time = datetime.datetime.now()
    return str(date_time.strftime("%Y%m%d_%H%M"))

#function that handles upload of a file
def handle_uploaded_file(f):
    #create a global version prefix to deliniate a uploaded file in the database
    global version_prefix
    #if the file that user tris to upload doesn't exist let user to upload it
    if not os.path.exists(os.path.join(os.path.dirname(__file__),'../media/'+ directory+f.name)):
        version_prefix = ""
        with open(os.path.join(os.path.dirname(__file__),'../media/'+ directory+f.name), 'w+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    #otherwise create a new version of the file using ver_generator function
    else:
        file_array = f.name.split('.')
        version_prefix = ver_generator()
        file_ready = file_array[0] + version_prefix
        with open(os.path.join(os.path.dirname(__file__),'../media/'+ directory+file_ready+'.xml'), 'w+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

#upon login set cookies and session dictionary with 'member_id' and 'directory' keys
def login_form(request):
    if request.COOKIES.get('dashboards_site', ""):
        print "Cookie: " + request.COOKIES.get('dashboards_site', "") + "signed cookie: " + \
              request.get_signed_cookie(key="dashboards_site", salt="addSalt")

    if request.method == 'POST':
        login = Login(request.POST)
        if login.is_valid():
            cd = login.cleaned_data
            try:
                user = User.objects.get(login=cd['login'], password=cd['password'])
            except User.DoesNotExist:
                return HttpResponseRedirect('/contact/error_message/')
            else:
                #here I write down user id into request.session dictionary-like object
                request.session['member_id'] = user.id
                #for link creation purposes, here I create a request.session 'user_login'
                request.session['user_login'] = user.login
                request.session['directory'] = request.session.get('user_login')+'/'
                global directory
                directory = request.session.get('directory')
                print "user id:" + str(request.session.get('member_id')) + "login: " + str(request.session.get('user_login'))
                return HttpResponseRedirect('/logged/')
    else:
        login = Login()
    #to save a cookie associated with login page save an instance of HTTPresponse in a variable 'response'
    response = render_to_response('forms/login_iframe.html', {'login':login}, RequestContext(request))
    #then sign a signed cookie associated with it; add salt for encryption
    response.set_signed_cookie(key="dashboards_site", value="password", salt="addSalt", max_age=10000, httponly=True)
    return response

#logout function
def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse('You logged out. Please<a href=%s> login here</a>:'%'/')

#get dash_name list
def get_dash_name(user_id):
    dash_name = []
    # a QuerySet (user_dashboards) of all the Dashboard objects for current user represented by request.session['member_id'] is returned
    user_dashboards = Dashboard.objects.filter(author = user_id)
    counter = 0
    #populate array of tuples: counter 1 to N and dashboard title (from the database)
    for dash in user_dashboards:
        counter=counter + 1
        dash_name.append((counter, dash.title))
    return dash_name

#register a new user
def register_form(request):
    if request.method == 'POST':
        register = Register(request.POST)
        if register.is_valid():
            cd = register.cleaned_data
            if (cd['login'] == cd['login_r']):
                login_cleaned = cd['login']
                directory = os.path.join(os.path.dirname(__file__), '../media/'+login_cleaned)
            else:
                return HttpResponseRedirect('/contact/error_login/')
            #if passwords match create a new directory (in case it doesn't exist)
            if cd['password'] == cd['password_r']:
                if not os.path.exists(directory):
                    os.makedirs(directory)
                u1 = User(first_name=cd['first'], last_name=cd['last'], email=cd['email'],
                          login=login_cleaned, password=cd['password'])
                u1.save()
                print u1
                #show user a 'success' screen
                return HttpResponseRedirect('/contact/success')
            else:
                #or tell user that that something went wrong
                return HttpResponseRedirect('/contact/error_login/')
    else:
        register = Register()
    return render_to_response('forms/register.html', {'register':register}, RequestContext(request))

#function to download files from server
def download(request):
    #check whether user id is in request.session dictionary-like object; i.e. user's session is running
    if request.session.get('member_id'):
        #get the actual user_id from the session
        user_id = request.session['member_id']
        if request.GET.items():
            DASH_NAME = get_dash_name(user_id)
            #calling function get_dash_name() that generates a list of tuples ((1, value1), (2, value2), ..., (N, valueN))
            # and sending dash_name list variable to form Download constructor
            search = Download(request.GET, dash_name=get_dash_name(user_id))
            if search.is_valid():
                cd = search.cleaned_data
                #make these vars global, so they will be seen by 'respond_as_attachment' function
                global path_to_dash_file
                global dashboard_file_name
                if cd['search_by_name']:
                    dashboard_object = Dashboard.objects.filter(title__icontains=cd['search_by_name'])
                    path_to_dash_file = os.path.join(os.path.dirname(__file__), '../media/'+dashboard_object[0].file_name)
                    dashboard_file_name = dashboard_object[0].file_name
                    return respond_as_attachment(request, path_to_dash_file, dashboard_file_name)
                else:
                    number_choice = cd['select_all']
                    number_choice_int = int(number_choice)
                    print(cd['search_by_name']), "selected dashboard:", number_choice_int
                    print "more testing:", DASH_NAME[number_choice_int-1][1]
                    dashboard_object = Dashboard.objects.filter(title=DASH_NAME[number_choice_int-1][1])
                    path_to_dash_file = os.path.join(os.path.dirname(__file__), '../media/'+directory+dashboard_object[0].file_name)
                    dashboard_file_name = dashboard_object[0].file_name
                    return respond_as_attachment(request, path_to_dash_file, dashboard_file_name)
        else:
            search = Download(dash_name=get_dash_name(user_id))
        return render_to_response('forms/download_form.html', {'search':search})
    else:
        #redirect template to 'top' frame. Otherwise it will remain in the same frame and each new log in will created '
        #nested cascade of frames
        return TemplateResponse(request, 'redirect_template.html', {'redirect_url':'/'})


import mimetypes
import urllib
def respond_as_attachment(request, file_path, original_filename):
    #print "testing... %s, %s:" %(file_path, original_filename)
    fp = open(file_path, 'rb')
    response = HttpResponse(fp.read())
    fp.close()
    #to figure out the type of file, for example xml
    type, encoding = mimetypes.guess_type(original_filename)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % original_filename.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:

        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(original_filename.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response


