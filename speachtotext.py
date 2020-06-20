# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 20:31:20 2020

@author: Soumya Kanti Mandal
"""
from ibm_watson import SpeechToTextV1   

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pandas.io.json import json_normalize
from ibm_watson import LanguageTranslatorV3

url_s2t = "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/6d123dc1-2748-46f9-8683-10414e20410d"   #the url location 
iam_apikey_s2t = "zlNsj9x2dPKn2bkXm2f9N7aGTzmByYJun84Ibf9_0mSa" # api key 

#speachtotext adapter object
authenticator = IAMAuthenticator(iam_apikey_s2t)
s2t = SpeechToTextV1(authenticator=authenticator)
s2t.set_service_url(url_s2t)
s2t

fname="skm.mp3"  #the mp3 file
with open(fname , mode='rb') as wav:
    response=s2t.recognize(audio=wav ,content_type='audio/mp3')  #use recognize to return th erecognize text

#result contain a dictionary that include translation
print('==========The mp3 to text Is Stored as a  Dictionary==========\n')
print(response.result)
print('\n') 
print('==========response of the recognizer==========\n')
print(json_normalize(response.result['results'],"alternatives"))
response

#here we store the text
recognized_text=response.result['results'][0]['alternatives'][0]['transcript']
type(recognized_text)

url_lt="https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/d0d7a537-d734-4586-94cd-22ce040545aa" #the url location
apikey_lt="GAgnAA0HCGDH8lqYfOVMxDPf5ibDnduwUMkqhn4qiIzi" #api key
version_lt='2018-05-01'

#language tranlator  object
authenticator = IAMAuthenticator(apikey_lt)
language_translator =LanguageTranslatorV3(version=version_lt, authenticator=authenticator)
language_translator.set_service_url(url_lt)
language_translator

#list of language that support 
print('\n')
print('==========The Supported Language You Can Choose To Convert==========\n')
print(json_normalize(language_translator.list_identifiable_languages().get_result(), "languages"))




translation_response = language_translator.translate(\
    text=recognized_text,model_id='en-es')    
translation_response

#the result is a dictionary
print('======spanis converted response a very few line ======\n')
translation=translation_response.get_result()
print(translation)


#obtain the actual translation as a string 
spanish_translation=translation['translations'][0]['translation']
print('======Spanish Language very few lines ======\n')
print(spanish_translation)

#translate back to english 
translation_new =language_translator.translate(text=spanish_translation,model_id='es-en').get_result()


#translation as a string
translation_eng=translation_new['translations'][0]['translation']
print('======English Language very few lines ======\n')
print(translation_eng)

#convert into france 
france_translation = language_translator.translate(
    text=translation_eng , model_id='en-fr').get_result()

print('========== France Language very few line  =========\n')    
print(france_translation['translations'][0]['translation'])







    
    



