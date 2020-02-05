import googletrans
from googletrans import Translator
from flask import Flask,render_template,request,url_for,redirect

'''------Translator Variables -------'''

translate=Translator()
lang_dict=googletrans.LANGUAGES #dictionary with key value pairs of language

'''--------Flask Variables -----------'''

app=Flask(__name__)

'''----------Regular Variables --------------'''

di=dict()

'''-----------Translator Modules---------------'''

def return_dict(): #returns googletrans dictionary
    return googletrans.LANGUAGES

def return_key(language): #returns the key for a given language
    for i in return_dict().keys():
        if lang_dict[i]==language.lower():
            return i

def list_of_languages(): #returns the values of languages( used for option tag )
    li=[]
    for i in lang_dict.keys():
        li.append(lang_dict[i].capitalize())
    return li

def return_object(src,dest,text): #returns translator object
    src_key=return_key(src)
    dest_key=return_key(dest)
    output=translate.translate(text,src=src_key,dest=dest_key)
    return output

def return_text(out): #returns translated text
    return out.text

def return_confidence(out): #returns confidence percentage of translation
    return (translate.detect(return_text(out)).confidence)*100

def source_equals_text(src,text):
    if translate.detect(text).lang==return_key(src):
        return True
    return False

'''---------------Flask Modules ----------------'''

@app.route('/') #First page
def homepage():
    return render_template('index.html',languages=list_of_languages())

@app.route('/translated') #Return to the next page
def translated():
    return render_template('duplicate.html',di=di) 

try:
    @app.route('/',methods=['GET','POST'])
    def inputs():
        if request.method=='POST':
            di['SourceLang']=request.form['sorc'] #Get the values from form
            di['DestinationLang']=request.form['dest']
            di['Text']=request.form['text']
            Obj=return_object(di['SourceLang'],di['DestinationLang'],di['Text'])
            if source_equals_text(di['SourceLang'],di['Text']): #Check the source language of Text 
                di['TranslatedText']=return_text(Obj)
                di['Confidence']=str(return_confidence(Obj))+'%'
                return redirect(url_for('translated')) #Goes to next page
            else:
                return render_template('index.html',languages=list_of_languages()) #Reloads the same page 
        else:
            return render_template('index.html',languages=list_of_languages()) #Reloads the same page if method is GET

    if __name__=="__main__":
        app.run(debug=True)

finally:
    print("Success!")

