import requests
import html
import re
import csv

#Packages for statistical analysis
import statistics
import matplotlib
import matplotlib.pyplot as mp 

#Packages for econometrics
import pandas as pd 
import numpy as np 
import statsmodels.api as sm 
import statsmodels.formula.api as smf


Prix=[] #Will contain all the prices collected from both website
Produits=[] #Will contain the name of all the product collected
Moyenne=[] #Means for each category
Mediane=[] #Median for each category
Minimum=[] #Minimum for each category
Maximum=[] #Maximum for each category
Taille_Ech=[] #Size of the sample
Red=[] #0 if the product belongs to CafePress // 1 if belongs to Redbubble
Cat_Femme=[] #0 if it belongs to men's department // 1 if belongs to women's

#The following line presents the goal of this tool : gathering data from two specific website and compare prices for one specific product : tee-shirt 
print('Ce programme permet de comparer les prix pour les teeshirts sur les marketplaces Redbubble.com et Cafepress.com. \nCette comparaison se fait à l\'aide de statistiques descriptives et d\'un modéle économétrique.')

################################## REDBUBBLE ############################################################
########################### Collect #####################################################################
#This section presents to the user the structure of the e-commerce website Redbubble. It tells how many department there are and its links
print("\n POUR LE SITE REDBUBBLE.COM :")
url='https://www.redbubble.com/'
redbubble=requests.get(url)
redbubble=redbubble.text
redbubble=html.unescape(redbubble)
redbubble=redbubble.replace('\n','')
redbubble=redbubble.replace('\t','')
redbubble=redbubble.replace('\r','')

#Gathering name and links for each department
pattern_red='aria-haspopup="true" href="(.+?(?=">))'
lien_cat_red=re.findall(pattern_red, redbubble)

pattern_red_name='<span>(.+?(?=</span>))'
nom_cat_red=re.findall(pattern_red_name, redbubble)
del(nom_cat_red[4]) 
del(nom_cat_red[4])
del(nom_cat_red[8])

#Announcing the permanent structure
print('Le Site RedBubble présente ', len(nom_cat_red),' départements de produits.')
print(nom_cat_red)
#Announcing the choosen departments for the scrapping
print("Dans le cadre de cette analyse, les départements de produits ciblés sont : ", nom_cat_red[0], "et", nom_cat_red[1])

#Gathering the name for each product presented in both department
Gamme_red=[]
Lien_gamme_red=[]
for k in range(0,2):
    url = "https://www.redbubble.com"
    url = requests.compat.urljoin(url,lien_cat_red[k])
    cat=requests.get(url)
    cat=cat.text
    cat=html.unescape(cat)
    cat=cat.replace('\n','-')
    cat=cat.replace('\t','_')
    
    pattern_red_cat='<span class="default__text--3DN1l default__display5--2BVdd" element="span">(.+?(?=</span></div></div>))'
    red_gamme=re.findall(pattern_red_cat,cat)
    print("\n \n Pour le département de produit ", nom_cat_red[k], " la liste des gammes de produits sont :")
    Gamme_red.extend(red_gamme)
    print(red_gamme)
    pattern_lien_red_cat='<a tabindex="0" class="Cards__link--1iiMg" href="(.+?(?="><div class="))'
    red_gamme_lien=re.findall(pattern_lien_red_cat,cat)
    Lien_gamme_red.extend(red_gamme_lien)
    #Announcing the user the product for whose price will be analysed
    print ("Il conviendra de se concentrer sur la première gamme :",red_gamme[0])

# Gathering data (price and name of the products) from Tee-shirt 
T_Red=[] 
T_Red_Lien=[] 
T_Red.append(Gamme_red[0])
T_Red.append(Gamme_red[3])
T_Red_Lien.append(Lien_gamme_red[0])
T_Red_Lien.append(Lien_gamme_red[3])

Red_Prix=[] #Lists of all the price collected from Redbubble

Prix_R_H=[] #Prices of Tee_shirts from Redbubble men's department
Prix_R_F=[] #Prices of Tee_shirts from Redbubble women's department
for i in range(0,2):
    print("\nPour le département ", nom_cat_red[i], ':')
    Prix_Red=[]
    Produit_Red=[]

    for j in range(0,16):
        url = "https://www.redbubble.com"
        page="&page="+str(j)
        url = requests.compat.urljoin(url,T_Red_Lien[i],page)
        gam=requests.get(url)
        gam=gam.text
        gam=html.unescape(gam)
        gam=gam.replace('\n','-')
        gam=gam.replace('\t','_')
        gam=gam.replace('&#39;',' ')
        
        pat_produits='<h2 class="default__text--3DN1l default__caption--3cJd6 default__muted--1ydZD styles__fullTitle--2XH1d" element="h2">(.+?(?=</h2>))'
        produit_red=re.findall(pat_produits, gam)
        Produit_Red.extend(produit_red)
        pat_prix='<span class="default__text--3DN1l default__display6--7oOD8 styles__price--EYMKU" element="span">€(.+?(?=</span>))'
        prix_red=re.findall(pat_prix, gam)
        Prix_Red.extend(prix_red)
 
    taille=len(Prix_Red)
    Taille_Ech.append(taille)
    Prix.extend(Prix_Red)
    Produits.extend(Produit_Red)
    Red_Prix.extend(Prix_Red)
    
    for k in range(len(Prix_Red)):
        Prix_Red[k].replace('.',',')
        Prix_Red[k]=float(Prix_Red[k])
    
    if i==0:
        for j in range(len(Prix_Red)):
            Cat_Femme.append(i)
        Prix_R_H.extend(Prix_Red)
    else:
        for j in range(len(Prix_Red)):
            Cat_Femme.append(i)
        Prix_R_F.extend(Prix_Red)

    #Stats 
    print("Les statistiques descriptives se ferront sur la base de ", taille, " produits présentés sur la premières page.")
    moyenne=statistics.harmonic_mean(Prix_Red)
    print("Le prix moyen d'un produit de cette gamme est de ", moyenne,"€.")
    Moyenne.append(moyenne)
    mediane=statistics.median(Prix_Red)
    print("Le prix médian pour cette gamme de produit est de ", mediane,'€.')
    Mediane.append(mediane)
    maximum=max(Prix_Red)
    f=Prix_Red.index(max(Prix_Red))
    print("Le prix le plus élévé de cette gamme est de ", maximum, '€.')
    print("Ce prix correspond au produit ", Produit_Red[f])
    Maximum.append(maximum)
    minimum=min(Prix_Red)
    f=Prix_Red.index(min(Prix_Red))
    print("Le plus petit prix de cette gamme est de ", minimum,"€.")
    print("Ce prix correspond au produit ", Produit_Red[f])
    Minimum.append(minimum)

#Econometrics
var=Prix_R_H+Prix_R_F
for k in range(len(var)):
    Red.append(0)

###################################### CAFEPRESS.COM #############################################################

print('\n \n \n POUR LE SITE CAFEPRESS :')
url='https://www.cafepress.com/'
main=requests.get(url)
main=main.text
main=html.unescape(main)
main=main.replace('\n','')
main=main.replace('\t','')
main=main.replace('\r','')

# Gathering the name of all the departments of the webstore
caf_cat='<a class="parent-link" reset-ui="" href="//www.cafepress.com/\+(.+?(?=">))'
caf_cat=re.findall(caf_cat, main)

print("Le site Cafe Press présente ", len(caf_cat), " départements de produits.")
print(caf_cat)
print('Dans le cadre de notre analyse, les départements ciblés sont :', caf_cat[0], "et", caf_cat[1])
caf_lien='<a class="parent-link" reset-ui="" href="//www.cafepress.com/(.+?(?=">))'
caf_lien=re.findall(caf_lien, main)

#This part differs from the one used for Redbubble. The website structure is different and doesn't allow
caf_cat=[w.replace('-clothing', '-t-shirts') for w in caf_cat] 
caf_lien=[y.replace('-clothing', '-t-shirts') for y in caf_lien]

Caf=[] #List containing the name of the product
Caf_Prix=[] #List containing the price
Prix_C_H=[] #Price for tee-shirts in the men's department
Prix_C_F=[] #Price for tee-shirst in women's department

for z in range(0,2):
    print('\nPour les T-shirts du département ', caf_cat[z],':')
    Prixc=[]
    Produitc=[]

    for i in range(0,20):
        page="?page="+str(i)
        url = "https://www.cafepress.com/"
        url = requests.compat.urljoin(url,caf_lien[z], page)
        cat=requests.get(url)
        cat=cat.text
        cat=html.unescape(cat)
        cat=cat.replace('\n','-')
        cat=cat.replace('\t','_')
        pattern_caf_produit='title="(.+?(?="> <div class="img-wrap">))'
        caf_produit=re.findall(pattern_caf_produit,cat)
        Produitc.extend(caf_produit)
        pattern_caf_prix='<div class="base-price">\$(.+?(?=</div>))'
        caf_prix=re.findall(pattern_caf_prix, cat)
        Prixc.extend(caf_prix)

    Taille_Ech.append(len(Prixc))
    Prix.extend(Prixc)
    Caf.extend(Produitc)


    for k in range(len(Prixc)):
        Prixc[k].replace('.',',')
        Prixc[k]=float(Prixc[k])

    Caf_Prix.extend(Prixc)

    if z==0:
        for j in range(len(Prixc)):
            Cat_Femme.append(z)
        Prix_C_H.extend(Prixc)
    else:
        for j in range(len(Prixc)):
            Cat_Femme.append(z)
        Prix_C_F.extend(Prixc)
    
    taillec=len(Prixc)
    print("Les statistiques descriptives se ferront sur la base de ", taillec, " produits présentés sur la premières page.")
    moyenne=statistics.harmonic_mean(Prixc)
    print("Le prix moyen d'un produit de cette gamme est de ", moyenne,"€.")
    Moyenne.append(moyenne)
    mediane=statistics.median(Prixc)
    print("Le prix médian pour cette gamme de produit est de ", mediane,'€.')
    Mediane.append(mediane)
    maximum=max(Prixc)
    f=Prixc.index(max(Prixc))
    print("Le prix le plus élévé de cette gamme est de ", maximum, '€.')
    """ print("Ce prix correspond au produit ", Produitc[f])"""
    Maximum.append(maximum)
    minimum=min(Prixc)
    f=Prixc.index(min(Prixc))
    print("Le plus petit prix de cette gamme est de ", minimum,"€.")
    """print("Ce prix correspond au produit ", Produitc[f])"""
    Minimum.append(minimum)

var=Prix_C_H+Prix_C_F
for k in range(len(var)):
    Red.append(1)


#Graphs
#The first graph compares the price for men's tee-shirt for both webstores
x1=Prix_R_H
x2=Prix_C_H
mp.hist([x1,x2], range=(15, 41), bins=5, density=1, color=['red', 'green'], edgecolor='xkcd:black', label=['Redbubble','CafePress'])
mp.title('Répartition des prix des tee-shirts Homme entre les deux sites', fontdict=None, loc='center', pad=None)
mp.xlabel('Prix en euros')
mp.ylabel('Pourcentage de répartition')
mp.legend()
mp.show()

#The second graph compares the price for men's tee-shirt for both webstores
x1=Prix_R_F
x2=Prix_C_F
mp.hist([x1,x2], range=(15, 41), bins=5, density=1, color=['red', 'green'], edgecolor='xkcd:black', label=['Redbubble','CafePress'])
mp.title('Répartition des prix des tee-shirts Femme entre les deux sites', fontdict=None, loc='center', pad=None)
mp.xlabel('Prix en euros')
mp.ylabel('Pourcentage de répartition')
mp.legend()
mp.show()

#The following lines creates a CSV file with all the stats for each department and each store
with open("Statistiques descriptives des deux sites.csv", 'w', encoding='utf-8')as outfile :
    data=csv.writer(outfile, delimiter='\t', lineterminator='\n')
    data.writerow(['Taille Echantillon', 'Prix moyen', 'Prix médian', 'Prix minimal', 'Prix maximal'])
    data.writerows(zip(Taille_Ech, Moyenne, Mediane, Minimum, Maximum))

#Econometrics
print('\n Il conviendra d\'estimer le prix d\'un tee-shirt en fonction de son appartenance à un site, à une catégorie.')
print('La référence est l\'appartenance du produit au site redbubble et au département homme.')
#This allows to create a CSV data base with all the name, price and website
with open("base.csv", 'w', encoding='utf-8')as base:
    data=csv.writer(base, lineterminator='\n')
    data.writerow(['Prix', 'Site', 'Femme'])
    data.writerows(zip(Prix, Red, Cat_Femme))

#This part is to show the user the regression made based on the database
base=pd.read_csv('base.csv')
reg=smf.ols('Prix ~ Site + Femme', data=base)
results=reg.fit()
print(results.summary())
