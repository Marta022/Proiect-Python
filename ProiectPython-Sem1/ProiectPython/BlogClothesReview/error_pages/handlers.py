from flask import Blueprint,render_template

error_pages = Blueprint('error_pages', __name__) #am creat un obiect error_pages de tip Blueprint, caruia i-am parsat doua argumente, un nume 'errpr_pages' si variabila speciala __name__ care tine numele modulului curent de Python


@error_pages.app_errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html') , 404 #returnam un tuple, un template html (cu interpretarea noastra a erorii) si codul de eroare in sine 

@error_pages.app_errorhandler(403)
def error_403(error):
    return render_template('error_pages/403.html') , 403


#la fel ca si in cazul Blueprintului din sectiunea core/views, este nevoie sa legam blueprintul creat, adica error_pages, de fisierul _init_.py