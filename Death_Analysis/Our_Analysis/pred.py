import findspark
findspark.init('/usr/local/spark')


import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
df1 = pd.read_csv('ahs-mort-rajasthan-jhunjhunun.csv')
df2 = pd.read_csv('ahs-mort-rajasthan-sirohi.csv')
df3 = pd.read_csv('ahs-mort-rajasthan-alwar.csv')
df4 = pd.read_csv('ahs-mort-rajasthan-dhaulpur.csv')
df5 = pd.read_csv('ahs-mort-rajasthan-bikaner.csv')
df6 = pd.read_csv('ahs-mort-rajasthan-jhalawar.csv')
df7 = pd.read_csv('ahs-mort-rajasthan-jodhpur.csv')
df8 = pd.read_csv('ahs-mort-rajasthan-jaipur.csv')
df9 = pd.read_csv('ahs-mort-rajasthan-jaisalmer.csv')
df10 = pd.read_csv('ahs-mort-rajasthan-kota.csv')
df11 = pd.read_csv('ahs-mort-rajasthan-sikar.csv')
df12 = pd.read_csv('ahs-mort-rajasthan-tonk.csv')
df13 = pd.read_csv('ahs-mort-rajasthan-udaipur.csv') 

frames = [df1, df2 ,df3, df4 ,df5, df6 ,df7, df8,df9,df10,df11,df12,df13]
df = pd.concat(frames)

df = df [['state','district','deceased_sex','age','treatment_source','month_of_death','year_of_death','death_symptoms','is_death_associated_with_preg'
            ,'marital_status','highest_qualification','drinking_water_source','toilet_used']]

df["marital_status"].fillna("null", inplace = True)
df["treatment_source"].fillna("null", inplace = True)
df["highest_qualification"].fillna("null", inplace = True)
df["drinking_water_source"].fillna("null", inplace = True)
df["toilet_used"].fillna("null", inplace = True)
df["death_symptoms"].fillna("null", inplace = True)
df["is_death_associated_with_preg"].fillna("null", inplace = True)
df["age"].fillna(value=0, inplace = True)

from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.feature import VectorIndexer,VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.ml import Pipeline

ff=[
    'state', 'district', 'age', 'treatment_source',
       'month_of_death', 'year_of_death', 'death_symptoms',
       'is_death_associated_with_preg', 'marital_status',
               'highest_qualification', 'drinking_water_source', 'toilet_used'
]

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



df.state = [state[item] for item in df.state]
df.district = [district[item] for item in df.district]
df.deceased_sex = [deceased_sex[item] for item in df.deceased_sex]
df.treatment_source = [treatment_source[item] for item in df.treatment_source]
df.marital_status = [marital_status[item] for item in df.marital_status]
df.drinking_water_source = [drinking_water_source[item] for item in df.drinking_water_source]
df.toilet_used = [toilet_used[item] for item in df.toilet_used]
df.highest_qualification = [highest_qualification[item] for item in df.highest_qualification]
df.death_symptoms = [death_symptoms[item] for item in df.death_symptoms]
df.is_death_associated_with_preg = [is_death_associated_with_preg[item] for item in df.is_death_associated_with_preg]
df.head()
df.dropna(inplace=True)
tc = df.corr()
sns.heatmap(tc,annot=True) 
df.to_csv('numdata.csv') 	
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('proj').getOrCreate()
data = spark.read.format('csv').load('numdata.csv',header=True,inferSchema=True)	
train_data,test_data =data.randomSplit([0.7,0.3])

subject ={'RAJASTHAN':1,'JHUNJHUNUN':1, 'age':1,'Government Hospital':2,'2008':2008,'Congenital/birth defects':15,'Yes':1,'Separated':4,'Illiterate':9,'Piped water into dwelling/yard/plot':1,'To septic tank':3}

subject = ['Rajasthan', 'JHUNJHUNUN', '1', 'Government Hospital', '1', '2008', 'Congenital/birth defects', 'Yes', 'Separated', 'Illiterate', 'Piped water into dwelling/yard/plot', 'To septic tank']


assembler = VectorAssembler(inputCols=ff,outputCol="features")
assembled = assembler.transform(data)
(trainingData,testData) = assembled.randomSplit([0.8,0.2],seed = 13234)
dt = DecisionTreeClassifier(labelCol="deceased_sex",featuresCol="features",maxDepth=5,minInstancesPerNode=25)
pipeline = Pipeline(stages=[dt])
model = pipeline.fit(trainingData)
predictions = model.transform(testData)	
predictions.select("deceased_sex","prediction").head(25)