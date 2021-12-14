# SPOT Web App
**By:** Samantha Gleich\
**Last Updated:** December 13, 2021\
\
**This web app allows the user to specify a taxonomic group of interest and a depth. Then, the web app summarizes and visualizes 18S tag-sequencing data that were collected at the San Pedro Ocean Time-Series (SPOT) site based on the user input.**
\
\
**Here is what the web app looks like when properly executed:** http://sgleich.pythonanywhere.com/home
\
\
**To run this app, there must be two subdirectories within the main directory.**\
/SPOTWebApp/static/{image.png}   - To store image being displayed on the html pages\
/SPOTWebApp/templates/{home.html}  - To store all html templates being used in the web app (i.e. home.html, plot.html, Chlorophyte.html, etc...)\
\
**You also must have the dataset(s) and the main python script in the main directory.**\
/SPOTWebApp/{SPOT_ASVs_CLR.csv}\
/SPOTWebApp/{flask_app.py}

## Required packages
This web app requires the use of functions in pandas, os, matplotlib, flask, io, and base64 and was created in python 3.7 using the PyCharm IDE. 
```
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template,request,session
from io import BytesIO
import base64
app = Flask(__name__)
```

## Home
The home function will render the home html template (home screen of web app). On the home screen, the user is asked to select a specific taxnomic group of interest.
```
@app.route('/')
@app.route('/home', methods = ['GET'])
def home():
    return render_template('home.html')
```

## Category
The category function will render the html template based on the taxonomic category that was selected on the home page. The options in this example are: Chlorophyte, Ciliate, Diatom, Dinoflagellate, Haptophyte, MAST, and Rhizaria
```
@app.route('/taxa', methods = ['POST','GET'])
def category():
    selectValue = request.form.get('tax')
    if selectValue=="Dinoflagellate":
        return render_template('dinoflagellate.html')
    if selectValue=="Diatom":
        return render_template('diatom.html')
    if selectValue=="Ciliate":
        return render_template('ciliate.html')
    if selectValue=="MAST":
        return render_template('mast.html')
    if selectValue=="Chlorophyte":
        return render_template('chlorophyte.html')
    if selectValue=="Haptophyte":
        return render_template('haptophyte.html')
    if selectValue=="Rhizaria":
        return render_template('rhizaria.html')
```
## Taxonomic Group
```
Separate functions will be needed for each taxonomic group of interest (i.e. one for each of the 7 groups listed above). Here is an example of one of the the functions (i.e. chlorophyte). This function will take a specific chlorophyte genus as input and render the plot html template to show the abundance of the genus over time.  
@app.route('/chlorophyte',methods=['POST','GET'])
def chlorophyte():
    session["category"] = "Chlorophyte"
    selectValue = request.form.get('tax2')
    session["tax"] = selectValue
    d = request.form.get('Depth')
    p = viz("Chlorophyte", selectValue,d)
    img = BytesIO()
    p.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('plot.html', plot_url=plot_url,depth=d)
```
## Visualize
The visualize function will subset the data according the genus and depth user inputs. The data will then be summarized and plotted for visualization. The chlorophyte example is continued below. The full form of this function will contain all of the genra in each of the broad taxonomic categories (see full script).
```
@app.route("/viz")
def viz(category, tax,depth):
    
    df = pd.read_csv("SPOT_ASVs.csv")
    
    # Subset by genus
    chloro = ["Halosphaera","Pterosperma","Chloroparvula","Ostreococcus","Mantoniella","Pyramimonas","Micromonas",
              "Nephroselmis","Prasino-Clade-9_XXX","Dolichomastigaceae-A",
              "Pyramimonadales_XXX","Bathycoccus","Prasinopapilla","Chlorodendrales_XX","Mamiella","Dolichomastix",
              "Crustomastigaceae-AB","Chloropicon","Crustomastix","Prasinococcales-Clade-B_X Prasinoderma"]
    if category == "Chlorophyte":
        if tax in chloro:
            dfSub = df[df["genus"] == tax]
        elif tax == "Unknown":
            dfSub = df[df["genus"] == tax]
            tax = "Unknown Chlorophyte"
        else:
            dfSub = df[df["phylum"] == "Chlorophyta" and df["genus"] not in chloro]
            tax = "Other Chlorophytes"
            
    # Subset by depth 
    if depth =="Surface":
        dfSurf = dfSub[dfSub["depth"] == "5m"]
        # Group the data by depth and month of year; calculate the mean and sd
        dfAvg = (dfSurf.groupby(['month'])['value'].agg(['mean', 'std']).reset_index())
        # Group the data by depth and year; calculate the mean and sd
        dfAvg2 = (dfSurf.groupby(['year'])['value'].agg(['mean', 'std']).reset_index())

    if depth=="DCM":
        dfDCM = dfSub[dfSub["depth"] == "DCM"]
        dfAvg = (dfDCM.groupby(['month'])['value'].agg(['mean', 'std']).reset_index())
        dfAvg2 = (dfDCM.groupby(['year'])['value'].agg(['mean', 'std']).reset_index())

    # Plot the data
    fig = plt.figure()
    ax1 = plt.subplot(1,2,1)
    ax2 = plt.subplot(1,2,2)
    ax1.errorbar("month","mean","std", linestyle='solid', marker='o',data=dfAvg,color="black")
    ax2.errorbar("year", "mean", "std", linestyle='solid', marker='o', data=dfAvg2, color="black")
    ax1.set(xlabel="Month of Year",ylabel="Mean CLR-Transformed Abundance (+/- SD)",title="Abundance vs. Month",xticks=[1,2,3,4,5,6,7,8,9,10,11,12])
    ax2.set(xlabel="Year", ylabel="Mean CLR-Transformed Abundance (+/- SD)", title="Abundance vs. Year",xticks=[3, 4, 5, 6, 7, 8, 9, 10, 11,  
    12,13,14,15,16,17,18],xticklabels=["2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018"])
    ax2.tick_params(labelrotation=45)
    fig.suptitle(tax)
    fig.set_size_inches(13.5, 7.25)
    return fig
```   
## Main
This code will run the web app. 
```
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,port=5009)
```
