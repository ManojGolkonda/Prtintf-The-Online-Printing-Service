from printf.models import *
import os,sys
import django
sys.path.append("../App")
os.environ["DJANGO_SETTINGS_MODULE"] = "App.settings"
django.setup()

def display(temp):
    print temp