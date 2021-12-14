"""
San Pedro Ocean Time-Series (SPOT) Microbial Eukaryote Data
University of Southern California
Web App By: Samantha Gleich
Last Updated: December 13, 2021
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Load in modules that will be used in web app
"""
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask,render_template,request,session
from io import BytesIO
import base64
app = Flask(__name__)

"""
home = renders the home.html template
"""
@app.route('/')
@app.route('/home', methods = ['GET'])
def home():
    return render_template('home.html')

"""
category = Renders the html template of a specific taxonomic group depending on user input
"""
@app.route('/taxa', methods = ['POST','GET'])
def category():
    selectValue = request.form.get('tax')
    if selectValue=="Dinoflagellate":
        return render_template('Dinoflagellate.html')
    if selectValue=="Diatom":
        return render_template('Diatom.html')
    if selectValue=="Ciliate":
        return render_template('Ciliate.html')
    if selectValue=="MAST":
        return render_template('Mast.html')
    if selectValue=="Chlorophyte":
        return render_template('Chlorophyte.html')
    if selectValue=="Haptophyte":
        return render_template('Haptophyte.html')
    if selectValue=="Rhizaria":
        return render_template('Rhizaria.html')

"""
dinoflagellate = prompts user to select specific taxonomic group within the dinoflagellate category
"""
@app.route('/dinoflagellate',methods=['POST','GET'])
def dinoflagellate():
    session["category"]="Dinoflagellate"
    selectValue = request.form.get('tax2')
    session["tax"] = selectValue
    d = request.form.get('Depth')
    m = request.form.get('Normalization')
    p=viz("Dinoflagellate",selectValue,d,m)
    img = BytesIO()
    p.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('plot.html', plot_url=plot_url,depth=d)

"""
diatom = prompts user to select specific taxonomic group within the diatom category
"""
@app.route('/diatom',methods=['POST','GET'])
def diatom():
    session["category"] = "Diatom"
    selectValue = request.form.get('tax2')
    session["tax"] = selectValue
    d = request.form.get('Depth')
    m = request.form.get('Normalization')
    p = viz("Diatom", selectValue,d,m)
    img = BytesIO()
    p.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('plot.html', plot_url=plot_url,depth=d)

"""
chlorophyte = prompts user to select specific taxonomic group within the chlorophyte category
"""
@app.route('/chlorophyte',methods=['POST','GET'])
def chlorophyte():
    session["category"] = "Chlorophyte"
    selectValue = request.form.get('tax2')
    session["tax"] = selectValue
    d = request.form.get('Depth')
    m = request.form.get('Normalization')
    p = viz("Chlorophyte", selectValue,d,m)
    img = BytesIO()
    p.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('plot.html', plot_url=plot_url,depth=d)

"""
haptophyte = prompts user to select specific taxonomic group within the haptophyte category
"""
@app.route('/haptophyte',methods=['POST','GET'])
def haptophyte():
    session["category"] = "Haptophyte"
    selectValue = request.form.get('tax2')
    session["tax"] = selectValue
    d = request.form.get('Depth')
    m = request.form.get('Normalization')
    p = viz("Haptophyte", selectValue,d,m)
    img = BytesIO()
    p.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('plot.html', plot_url=plot_url,depth=d)

"""
rhizaria = prompts user to select specific taxonomic group within the rhizaria category
"""
@app.route('/rhizaria',methods=['POST','GET'])
def rhizaria():
    session["category"] = "Rhizaria"
    selectValue = request.form.get('tax2')
    session["tax"] = selectValue
    d = request.form.get('Depth')
    m = request.form.get('Normalization')
    p = viz("Rhizaria", selectValue,d,m)
    img = BytesIO()
    p.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('plot.html', plot_url=plot_url,depth=d)

"""
mast = prompts user to select specific taxonomic group within the mast category
"""
@app.route('/mast',methods=['POST','GET'])
def mast():
    session["category"] = "MAST"
    selectValue = request.form.get('tax2')
    session["tax"] = selectValue
    d = request.form.get('Depth')
    m = request.form.get('Normalization')
    p = viz("MAST", selectValue,d,m)
    img = BytesIO()
    p.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('plot.html', plot_url=plot_url,depth=d)

"""
ciliate = prompts user to select specific taxonomic group within the ciliate category
"""
@app.route('/ciliate',methods=['POST','GET'])
def ciliate():
    session["category"] = "Ciliate"
    selectValue = request.form.get('tax2')
    session["tax"] = selectValue
    d = request.form.get('Depth')
    m = request.form.get('Normalization')
    p = viz("Ciliate", selectValue,d,m)
    img = BytesIO()
    p.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('plot.html', plot_url=plot_url,depth=d)

"""
viz = visualizes data using matplotlib
input = category, tax
return = plot of the mean +/- sd CLR-transformed abundance of the selected taxonomic group over month and year. 
"""
@app.route("/viz")
def viz(category, tax,depth,method):
    if method=="CLR":
        # Load in dataframe
        df = pd.read_csv("SPOT_ASVs_CLR.csv")

    if method=="TSS":
        # Load in dataframe
        df = pd.read_csv("SPOT_ASVs_TSS.csv")

    # Subset dataframe
    # Dinoflagellates
    dino = ["Blastodinium","Hematodinium","Paragymnodinium","Pelagodinium","Proterythropsis","Protoperidinium","Tripos",
            "Prorocentrum","Phalachroma","Gyrodinium","Karlodinium","Warnowia","Lepidodinium","Margalefidinium",
            "Heterocapsa","Alexandrium","Gymnodinium","Akashiwo","Noctiluca","Gonyaulax","Dinophysis","Kofoidinium",
            "Syndinium","Chytriodinium","Azadinium","Balechina","Goniodoma","Torodinium","Ceratoperidinium","Protoceratium",
            "Lingulodinium","Euduboscquella","Zooxanthella","Ellobiopsis","Thoracosphaeraceae_X","Syndiniales_XXX",
            "Ichthyodinium"]

    if category == "Dinoflagellate":
        if tax in dino:
            dfSub = df[df["genus"] == tax]
        elif tax == "Unknown":
            dfSub = df[df["order"] == tax]
            tax = "Unknown Dinoflagellate"
        elif "Dino-Group-I" in tax:
            dfSub = df[df['genus'].str.contains("Dino-Group-I")]
        elif "Dino-Group-II" in tax:
            dfSub = df[df['genus'].str.contains("Dino-Group-II")]
        elif "Dino-Group-III" in tax:
            dfSub = df[df['genus'].str.contains("Dino-Group-III")]
        else:
            dfSub = df[df["phylum"] == "Dinoflagellata" and df["genus"] not in dino]
            tax = "Other Dinoflagellates"

    # Chlorophytes
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

    # Haptophytes

    hapto = ["Chrysochromulina","Phaeocystis","Braarudosphaera","Haptolina","Pavlova",
             "Algirosphaera","Prymnesium","Helicosphaera","Dicrateria","Prymnesiaceae_X","Chrysocampanula",
             "Calcidiscus"]
    if category == "Haptophyte":
        if tax in hapto:
            dfSub = df[df["genus"] == tax]
        elif tax == "Unknown":
            dfSub = df[df["genus"] == tax]
            tax = "Unknown Haptophyte"
        else:
            dfSub = df[df["phylum"] == "Haptophyta" and df["genus"] not in hapto]
            tax = "Other Haptophytes"

    # Diatoms
    diatom = ["Pseudo-nitzschia","Bacteriastrum","Polar-centric-Mediophyceae_X","Guinardia","Chaetoceros",
              "Leptocylindrus","Thalassiosira","Eucampia","Asteromphalus","Rhizosolenia","Minidiscus","Cylindrotheca",
              "Navicula","Actinocyclus","Skeletonema","Cerataulina","Coscinodiscus","Hemiaulus","Corethron","Nitzschia",
              "Proboscia","Lauderia","Cyclotella","Pleurosigma"]
    if category == "Diatom":
        if tax in diatom:
            dfSub = df[df["genus"] == tax]
        elif tax == "Unknown":
            dfSub = df[df["genus"] == tax]
            tax = "Unknown Diatom"
        else:
            dfSub = df[df["class"] == "Bacillariophyta" and df["genus"] not in diatom]
            tax = "Other Diatoms"

    # MAST
    if category == "MAST":
        dfSub = df[df["class"] == tax]

    # Rhizaria
    rhiz = ["Cercozoa_XXXX","Partenskyella","Discomonas","Minorisa","Marimonadida_XX",
            "Cryothecomonas","Filosa-Thecofilosea_XXX","Hexaconus","Arthracanthida-Symphyacanthida_XX",
            "Ventrifissuridae_X","Filosa-Imbricatea_XXX","Nassellaria_XX","Chaunacanthida_XX","Lithomelissa",
            "Lychnaspis","Bigelowiella","Sticholonche","Pseudopirsonia","Chlorarachnida_XX","Symphyacanthida"]
    if category == "Rhizaria":
        if tax in rhiz:
            dfSub = df[df["genus"] == tax]
        elif tax == "Unknown":
            dfSub = df[df["class"] == tax]
            tax = "Unknown Rhizaria"
        elif "Acantharia" in tax:
                dfSub = df[df['genus'].str.contains("Acantharia")]
        elif "RAD-A" in tax:
                dfSub = df[df['genus'].str.contains("RAD-A")]
        elif "RAD-B" in tax:
                dfSub = df[df['genus'].str.contains("RAD-B")]
        elif "RAD-C" in tax:
                dfSub = df[df['genus'].str.contains("RAD-C")]
        else:
            dfSub = df[df["kingdom"] == "Rhizaria" and df["genus"] not in rhiz and "Acantharia" not in tax
            and "RAD-A" not in tax and "RAD-B" not in tax and "RAD-C" not in tax]
            tax = "Other Rhizaria"

    # Ciliates
    cil = ["Leegaardiella","Lynnella","Urotricha","Askenasia","Pseudotontonia","Eutintinnus","Pelagostrobilidium",
           "Apostomatia_XX","Spirotontonia","Tontoniidae_A_X","Strombidinopsis","Rimostrombidium_A" ,"Tintinnidae_X",
           "Litostomatea_XXX","Amphorides" ,"Tontoniidae_B_X","Peritromus","Didiniidae_X","Steenstrupiella",
           "Tintinnidium","Leegaardiellidae_A_X","Bergeriella"]
    if category == "Ciliate":
        if tax in cil:
            dfSub = df[df["genus"] == tax]
        elif "Strombidiidae" in tax:
                dfSub = df[df['genus'].str.contains("Strombidiidae")]
        elif "Strombidium" in tax:
                dfSub = df[df['genus'].str.contains("Strombidium")]
        elif "Strombidiida" in tax:
                dfSub = df[df['genus'].str.contains("Strombidiida")]
        elif tax == "Unknown":
            dfSub = df[df["genus"] == tax]
            tax = "Unknown Ciliate"
        else:
            dfSub = df[df["phylum"] == "Ciliophora" and df["genus"] not in cil and "Strombidiidae" not in tax and
                       "Strombidium" not in tax and "Strombidiida" not in tax]
            tax = "Other Ciliates"

    # Subset the data by depth
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

    # Plot it up!
    fig = plt.figure()
    ax1 = plt.subplot(1,2,1)
    ax2 = plt.subplot(1,2,2)
    ax1.errorbar("month","mean","std", linestyle='solid', marker='o',data=dfAvg,color="black")
    ax2.errorbar("year", "mean", "std", linestyle='solid', marker='o', data=dfAvg2, color="black")
    if method=="CLR":
        ax1.set(xlabel="Month of Year",ylabel="Mean CLR-Transformed Abundance (+/- SD)",title="Abundance vs. Month",xticks=[1,2,3,4,5,6,7,8,9,10,11,12])
        ax2.set(xlabel="Year", ylabel="Mean CLR-Transformed Abundance (+/- SD)", title="Abundance vs. Year",xticks=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13,14,15,16,17,18],xticklabels=["2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018"])
    if method=="TSS":
        ax1.set(xlabel="Month of Year", ylabel="Mean TSS-Transformed Abundance (+/- SD)", title="Abundance vs. Month",
                xticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        ax2.set(xlabel="Year", ylabel="Mean TSS-Transformed Abundance (+/- SD)", title="Abundance vs. Year",
                xticks=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                xticklabels=["2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013",
                             "2014", "2015", "2016", "2017", "2018"])
    ax2.tick_params(labelrotation=45)
    fig.suptitle(tax)
    fig.set_size_inches(13.5, 7.25)
    return fig



"""
Run web app
"""
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,port=5009)



