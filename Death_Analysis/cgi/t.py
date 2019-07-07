#!/usr/bin/python3

import cgi,cgitb
cgitb.enable()
form = cgi.FieldStorage()
if form.getvalue('dropdown'):
   subject = form.getvalue('dropdown')
else:
   subject = "Not entered"



print("Content-Type: text/html;charset=utf-8")

print("Content-type:text/html\r\n\r\n")
print('<html>')
print('<head>')
print('<title>Prediction</title>')
print('</head>')
print('<body>')
print('<h2>Predicted sex will be</h2>')
print("<h2> features are %s</h2>" % subject)
print('</body>')
print('</html>')


state={'RAJASTHAN':1}
district = {'JHUNJHUNUN':1, 'SIROHI':2, 'ALWAR':3, 'DHAULPUR':4, 'BIKANER':5, 'JHALAWAR':6,
       'JODHPUR':7, 'JAIPUR':8, 'JAISALMER':9, 'KOTA':10, 'SIKAR':11, 'TONK':12,
       'UDAIPUR':13}
deceased_sex = {'Female':1,'Male':2}
treatment_source={'Private Hospital':1,'Government Hospital':2,
                  'No Medical attention':3,'Private Dispensary/Clinic':4,
                  'Government PHC':5,'At Home':6,'Others':7,
                  'Private AYUSH Hospital/Clinic':8,'NGO or Trust Hosp/Clinic':9,
                  'Government CHC':10,'Government UHC/UHP/UFWC':11,
                  'Government Sub Center':12,'Government Dispensary/Clinic':13
                 ,'Government AYUSH Hospital/Clinic':14,'null':0,'19':7,'45':7,'14':7,'55':7}
marital_status = {'Married and Gauna performed':1, 'Widow/Widower':2, 'Never married':3, 'Separated':4, 
                  'Married but Gauna not performed':5, 'Remarried':6,
       'Not stated':7, 'Divorced':8,'null':0}
highest_qualification={'Literate With formal education-Post Grad/ M.Tech/M.B.A/ MD/Equivalent or higher':1,
                       'Literate with formal education-Graduate/B.Tech/B.B.A/MBBS/Equivalent':2,
                       'Literate With formal education-Middle':3,
                       'Literate With formal education-Secondary/Matric (Class-X)':4,
                       'Literate With formal education-Below primary':5,
                       'Literate Without formal education':6,'Literate With formal education-Primary':7,
                       'null':0,'Literate With formal education-Hr. Secondary/Sr. Secondary/Pre-university (Class XII)':8
                       ,'Illiterate':9,
                       'Literate With formal education-Non-technical/Technical diploma or certificate not equivalent to a degree':10}
drinking_water_source={'Piped water into dwelling/yard/plot':1,'Public tap/standpipe':2,'Tube well or Borehole':3, 
                       'Hand pump':4, 'Unprotected dug well':5,
       'Tanker /truck/Cart with Surface watersmall tank':6, 'Surface water':7,
       'other sources':8, 'Protected dug well':9,'null':0}
toilet_used={'Flush/Pour flush latrine connected:-To piped sewer system':1,
       'open defecation(field, brush,jungle etc.)':2, 'To septic tank':3,
       'Pit latrine with slab':4, 'To pit latrine':5, 'To somewhere else':6,
       'community toilet':7,
       'Pit latrine(without flush/ pour flush):-Ventilated Improved Pit(VIP)':8,
       'Open pit /Pit latrine without slab':9,'service latrine':10,'null':0}
death_symptoms ={'Hypothermia':1, 'Fever with Jaundice':2, 'Others':3, 'Infections':4,
       'Preterm birth/ Low birth weight baby not thriving':5,
       'Bleeding from umbilicus & elsewhere':6,
       'Convulsions soon after birth':7, 'Diarrhoea / Dysentery':8,
       'Asphyxia':9, 'Fever with rash':10, 'Birth injuries':11,
       'Respiratory Infection':12, 'Fever with convulsions':13, 'Jaundice':14,
       'Congenital/birth defects':15,'null':0}
is_death_associated_with_preg = {'No':2, 'null':0, '0':0, 'Yes':1}

features=[]
x=state[subject[0]]
features.append(x)	
x=district[subject[1]]
features.append(x)

x=subject[2]
features.append(x)

x=treatment_source[subject[3]]
features.append(x)

x=subject[4]
features.append(x)

x=subject[5]
features.append(x)

x=death_symptoms[subject[6]]
features.append(x)

x=is_death_associated_with_preg[subject[7]]
features.append(x)

x=marital_status[subject[8]]
features.append(x)

x=highest_qualification[subject[9]]
features.append(x)

x=drinking_water_source[subject[10]]
features.append(x)

x=toilet_used[subject[11]]
features.append(x)


print(features)

import pandas as pd 
df = pd.read('data.csv')
df["marital_status"].fillna("null", inplace = True)
df["treatment_source"].fillna("null", inplace = True)
df["highest_qualification"].fillna("null", inplace = True)
df["drinking_water_source"].fillna("null", inplace = True)
df["toilet_used"].fillna("null", inplace = True)
df["death_symptoms"].fillna("null", inplace = True)
df["is_death_associated_with_preg"].fillna("null", inplace = True)
df["age"].fillna(value=0, inplace = True)

df.state = [state[item] for item in df.state]
df