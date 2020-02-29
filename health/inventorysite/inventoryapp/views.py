

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Lender,Borrower
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from inventorysite.forms import LenderForm
from django.template import RequestContext
from django.shortcuts import render_to_response



from textblob import TextBlob

import random
import re
import nexmo




def logout_inventory(request):
    if request.user.is_authenticated():
        logout(request)
        return redirect('/login/')
    else:
        return HttpResponseRedirect('/login')

def index(request):
    current_mood = api_call()
    if(current_mood == "fear"):
        music = "/static/audio/Fight_Song.mp3"
    elif(current_mood == "anger"):
        music = "/static/audio/Let_it_Go.mp3"
    elif(current_mood == "sadness"):
        music = "/static/audio/burn.mp3"
    else:
        music = "static/audio/Hall_Of_Fame.mp3"
    return render(request,'index.html',{'music':music})


def about(request):
    return render(request,'aboutus2.html')

def blog(request):
    return render(request,'blogtwo.html')

def portfolio(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a valid chat')
        
        else:
            resp,link1,link2,link3=reply(q)
            return render(request, 'portfolio-details.html',
                          {'resp':resp,'link1':link1,'link2':link2,'link3':link3})
        
    return render(request, 'portfolio-details.html',
              {'errors': errors})


def shortcodes(request):
    return render(request,'shortcodes.html')

def contact(request):
    return render(request,'contact2.html')

def arrival(request):
    return render(request,'arrival.html')  

def service(request):
    return render(request,'service.html')    
#if request.user.is_authenticated():
#currentuser = request.user

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        username = request.POST.get('sap_id')

        user = User.objects.create(
            first_name = name,
            username = username,
            email=email,
            )
        user.set_password(password)
        user.save()

        user = authenticate(username = username, password = password)
        login(request, user)
        return redirect('/login/')
    else:
        return render(request,'register.html')   

def login_inventory(request):
    if request.method == 'POST':
        username = request.POST.get('sap_id')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user :
            if user.is_active:
                login(request,user)
                return redirect('/index/')
            else:
                return HttpResponse('Disabled Account')
        else:
            return HttpResponse("Invalid Login details.Are you trying to Sign up?")
    else:
        return render(request,'register.html')



def lenderform(request):
    if request.method == 'POST':
        form = LenderForm(request.POST ,request.FILES or None )
        if form.is_valid():
            cd = form.cleaned_data
            Lender.objects.create(lender=cd['lender'],product_name=cd['product_name'],product_description=cd['product_description'],image=request.FILES['image'],department=cd['department'],safety_deposit=cd['safety_deposit'],contact_number=cd['contact_number'])
        form = LenderForm()    
        return render(request,'testlenderform.html',{'form': form})               
    else:
        form = LenderForm()
    return render(request, 'testlenderform.html', {'form': form})    




def inventorylist(request):
    if request.user.is_authenticated():
        currentuser = request.user


    errors = []
    if 'q' in request.GET :
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            items = Lender.objects.filter(product_name__icontains=q)
            equipment=items[0]
            product_name=equipment.product_name
            name=currentuser.first_name
            sap_id=currentuser.username
            email=currentuser.email
            print(currentuser)


            student=Borrower(borrower=name,sap_id=sap_id,email=email,product_name=product_name)
            student.save()






            return render(request, 'inventoryresulttest.html',
                          {'items': items, 'query': q})

    full=Lender.objects.all()        
    return render(request, 'inventorytest.html',
              {'errors': errors,'full':full})







def cart(request):

    if request.user.is_authenticated():
        currentuser = request.user
        name=currentuser.first_name
        items = Borrower.objects.filter(borrower__icontains=name)
        return render(request, 'cart.html',
              {'items':items})

    else:
        return HttpResponse("Please login")


def arrival(request):
    
    items = Lender.objects.all()

    return render(request, 'arrival.html',
              {'items':items})





def check_for_anxiety(sentence):

    resp = "Believe in yourself and all that you are. Know that there is something inside of you that is greater than any obstacle. I think you should try meditation or yoga. Here are some links that could help you"
    link1 ="https://youtu.be/L1QOh-n-eus"
    link2="https://youtu.be/_iGWdUTifIQ"
    link3="https://youtu.be/nKHBIAdBvZ4"
    return resp,link1,link2,link3


def check_for_anger(sentence):
    resp = "Holding on to anger is like grasping a hot coal with the intent of throwing it at someone else; you are the one who gets burned. I think you should first calm down, and talk to me, open your heart out. Also, here are some additional videos you could check out and learn to divert your anger into a positive direction. I am always here for you. Lets get this together."
    link1 ="https://youtu.be/BsVq5R_F6RA"
    link2 ="https://youtu.be/T235jK9xR8Q"
    link3="https://youtu.be/de2TdvDaS5A"
    return resp,link1,link2,link3


def check_for_sad(sentence):
    resp = "Hey, why are you feeling so low. Did you know why you often feel so cold? Because you have a lot of fans. Hahahaha, aint I funny? Let's think about doing some fun things, look at out socialising page or check out these links."
    link1 ="https://youtu.be/qHvUUoSj1oM"
    link2 ="https://youtu.be/yqHH0IpPupg"
    link3="https://youtu.be/UkM-FjfN6Mc"
    return resp,link1,link2,link3



def check_for_fear(sentence):
    resp = "Be the warrior, not the worrier. Fear does not exist anywhere except in the mind."
    link1 ="https://youtu.be/-FyVetL1MEw"
    link2 ="https://youtu.be/1XDpa2HLXV0"
    link3="https://youtu.be/aE0pRMtQeu0"
    return resp,link1,link2,link3


danger_pattern = re.compile("^kill|^die|^suffer|^fail|^quit")
anxiety_pattern = re.compile("^tensed|^worried|^nervous|^panic|^concern|^uneasy|^stressed|^sick")
angry_pattern = re.compile("^angry|^anger|^furious|^hit|^annoyed|^irriated|^fuming|^snap|^fier|^rage|^rant|^storm|^pissed|^red|^boiling|^mad|^swear|^fuck")
sad_pattern = re.compile("^low|^sad|^disappoint|^broken|^fallen|^break|^sorrow|^depressed|^gloomy")
fear_pattern = re.compile("^horror|^scared|^phobia|^terror|^nightmare|^fright|^fear")




def check_for_keywords(sentence):
    link1=None
    link2=None
    link3=None
    resp=None
    for word in sentence.words:

        if danger_pattern.match(word.lower()):
            client = nexmo.Client(key='75d84653', secret='SoDG2ayMGG4huX9O')

            client.send_message({'from': '13092828727', 'to': '16462339846', 'text': 'This is an Emergency, Please Help me!!',})
            resp = "You are strong and have a thousand reasons to be happy :) We are always here for you !"
            
            break
        
        elif anxiety_pattern.match(word.lower()):
            resp,link1,link2,link3 =check_for_anxiety(sentence)
            break
            
        elif angry_pattern.match(word.lower()): 
            
            resp,link1,link2,link3 =check_for_anger(sentence)
            break
          

        elif sad_pattern.match(word.lower()):
            resp,link1,link2,link3=check_for_sad(sentence)
            break
           

        elif fear_pattern.match(word.lower()): 
            resp,link1,link2,link3 =check_for_fear(sentence)
            break

    return resp,link1,link2,link3



greeting_pattern = re.compile("^hello|^hi|^greeting|^sup|^what's up|^hey")

GREETING_RESPONSES = ["Hey, welcome ..", "Oh hi there :p ", "Hey there ! " , "Hey, what's up ?"]



NONE_RESPONSES = [
    "I didn't get what you said...",
    "I didn't understand..",
    "Umm, could you please elaborate ? ",

]


def check_for_greeting(sentence):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    for word in sentence.words:
        if greeting_pattern.match(word.lower()) :
            return random.choice(GREETING_RESPONSES)


def request(sentence):
    #cleaned = preprocess_text(sentence)
    parsed = TextBlob(sentence)

    resp= None
    link1=None
    link2=None
    link3=None

    resp,link1,link2,link3 = check_for_keywords(parsed)


    if not resp:
        resp = check_for_greeting(parsed)

    if not resp:
        resp = random.choice(NONE_RESPONSES)

    return resp,link1,link2,link3



def reply(sentence):
    resp,link1,link2,link3  = request(sentence)
    return resp,link1,link2,link3



    
    
def read_log_string():
    import re
    fp = open('/Users/shreya_naik/logfile.txt', 'r')

    s = ""
    for i,line in enumerate(fp):
        if i == 1 or i == 2:
            continue
        s += line


    # s.replace("[return]", "\n")
    ret = ""
    skip1c = 0
    for i in s:
        if i == '[':
            skip1c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif skip1c == 0:
            ret += i
    return (ret)

def api_call():
    import json
    from ibm_watson import ToneAnalyzerV3
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_watson import ApiException

    authenticator = IAMAuthenticator('OI0G_Rf5fzFMERmUnnbDA6kkyuXM0f_9EYVBUSEJoLSj')
    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        authenticator=authenticator
    )

    tone_analyzer.set_service_url('https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/1d285fb1-002f-4d28-a024-032d169f7cb0')
    text = read_log_string()
    tone_analysis = tone_analyzer.tone({'text': text},content_type='application/json').get_result()
    c = json.dumps(tone_analysis, indent=2)
    #print(c)
    #print(tone_analysis["sentences_tone"][-1]["tones"][0]["tone_id"])
    return tone_analysis["sentences_tone"][-1]["tones"][0]["tone_id"]
    #current_mood = tone_analysis["document_tone"]["tones"][0]["tone_id"]
    #print(current_mood)

























