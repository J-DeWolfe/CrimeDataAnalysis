import json
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

#OPEN JSON FILE & RETURN CRIME DATA
def getCrimeData():
    try:
        dataFile = open("FederalCrimeData.json", 'r')
        crime_data = json.loads(dataFile.read())
        dataFile.close()
        return crime_data
    except FileNotFoundError:
        return []

#DATA FUNCTIONS-------------------------------------------------------------------------------------
#Return crime totals for a given level of government
def getCrimeTotals(crime_data, gov, violent = True, larceny = True):
    
    #Returns all crimes (default)
    #Returns only violent crime if larceny = False
    #Returns only larceny if violent = False
    #Returns zeroes if both are False
    #Nonviolent crimes = all crimes minus violent crimes

    crimes = {} 
    for city in crime_data:
        if (violent | larceny):
            if city[gov] in crimes.keys():
                 crimes[city[gov]] += int(city["Robbery"])
            else:
                 crimes[city[gov]] = int(city["Robbery"])
            if (violent):
                crimes[city[gov]] += int(city["Assault"])
                crimes[city[gov]] += int(city["Murder"])
                crimes[city[gov]] += int(city["Rape"])
            if (larceny):
                crimes[city[gov]] += int(city["Burglary"])
                crimes[city[gov]] += int(city["Theft"])
                crimes[city[gov]] += int(city["Vehicle_Theft"])
        else:
            crimes[city[gov]] = 0
    return crimes

#Return specific crime data for a given level of government
def getSpecificCrime(crime_data, gov, crime):
    specific_crime = {}
    for city in crime_data:
        if city[gov] in specific_crime.keys():
            specific_crime[city[gov]] += int(city[crime])
        else:
            specific_crime[city[gov]] = int(city[crime])
    return specific_crime

#Return the crime_data for a specifically named government
def getSpecificGov(crime_data, gov, govName):
    gov_data = []
    for city in crime_data:
        if (city[gov].upper() == govName.upper()):
            gov_data.append(city)
    return gov_data
 
#Calculate mean average
def calculateMean(dict):
    qty = len(dict)
    total = 0
    for key in dict.keys():
        total += dict[key]
    return total/qty
                                                    
#Return population for a given level of government
def getPopulation(crime_data, gov):
    area_pop = {}
    for city in crime_data:
        if len(city['Population']) > 0:
            temp = ''                                                
            for c in city['Population']:
                if c != ',': #Remove commas from number format
                    temp += c
            if city[gov] in area_pop.keys():
                area_pop[city[gov]] += int(temp)
            else:
                area_pop[city[gov]] = int(temp)
        else:
            pass #Do not count if population data is missing
    return area_pop

#DISPLAY FUNCTIONS----------------------------------------------------------------------------------
#Calculate and display murder rate by state
def displayMurderRate():
    pop = getPopulation(crime_data, "State")
    murder = getSpecificCrime(crime_data, "State", "Murder")
    tally = 0;
    print("\nMURDER RATES BY STATE (Murders per 100k residents)")
    print("{:<22}{:>8}{:>14}{:>14}".format("STATE", "MURDERS", "POPULATION", "MURDER RATE"))
    for state in murder:
        murder_rate = (murder[state]/pop[state])*100000
        tally += murder_rate;
        print("{:<22}{:>8}{:>14}{:>14.2f}".format(state.title(), murder[state], pop[state], murder_rate))
    pop_avg = int(calculateMean(pop))
    murder_avg  = int(calculateMean(murder))
    murderRate_avg = tally/len(murder)
    print("{:<22}{:>8}{:>14}{:>14.2f}".format("AVERAGES", murder_avg, pop_avg, murderRate_avg))

#Plot pie chart                                                  
def plotPieChart(title, gov, crimeDict, colormap = 'viridis'):
    framable = {}
    for key in crimeDict.keys():
        framable[len(framable)] = [crimeDict[key], key.title()]
    
    dFrame = pd.DataFrame.from_dict(framable, orient ='index', columns = ['Incidents', gov])  
    
    dFrame.plot.pie(x = gov, y = 'Incidents', explode = (0,0,0,0.1), legend = None, cmap = colormap,
                    labels = crimeDict.keys(), autopct='%1.0f%%', shadow=True)
    plt.gca().get_xaxis().set_label_text('')
    plt.gca().get_yaxis().set_label_text('')
    plt.show()

#Plot bar chart                                                  
def plotBarChart(title, gov, crimeDict, wide = True, colormap = 'viridis'):
    framable = {}
    width = 10 if wide else 5
    palette = matplotlib.cm.get_cmap(colormap)
    
    for key in crimeDict.keys():
        framable[len(framable)] = [crimeDict[key], key.title()]
    
    colors = (palette(0), palette(.33), palette(.66), palette(.99))
    dFrame = pd.DataFrame.from_dict(framable, orient ='index', columns = ['Incidents', gov]) 
    dFrame.plot.bar(x = gov, legend = None, color = colors, figsize = (width, 5))
    plt.gca().get_xaxis().set_label_text('')
    plt.title(title)
    plt.show()
    
#Plot simple histogram                                                  
def plotSimpleHistogram(title, crimeDict, wide = True, colormap = 'viridis'):
    framable = {}
    width = 10 if wide else 5
    
    for key in crimeDict.keys():
        framable[len(framable)] = [crimeDict[key], key.title()]
        
    dFrame = pd.DataFrame.from_dict(framable, orient ='index') 
    dFrame.plot.hist(legend = None, cmap = colormap, figsize = (width, 5), bins = len(framable))
    plt.gca().get_xaxis().set_label_text('')
    plt.title(title)
    plt.show()
    
#Plot multi-Dimensional histogram from a list of dictionaries
def plotMultiDimensionalHistogram(crimeDictList, title = "TEST", wide = True, colormap = 'viridis'):
    framable = {}
    width = 10 if wide else 5
    
    for key in crimeDictList[0].keys():
        framable[key.title()] = [crimeDictList[0][key], crimeDictList[1][key]]
        
    #dFrame = pd.DataFrame({ 'A':[1, 1, 1, 1],  'B':[2, 2, 2, 2],  'C':[3, 3, 3, 3], 'D': [4, 5, 6, 7 ]})
    dFrame = pd.DataFrame(framable)
    dFrame.plot.hist(cmap = colormap, figsize = (width, 5), stacked = True, bins = len(framable))
    plt.gca().get_xaxis().set_label_text('')
    plt.title(title)
    plt.show()
    
#MAIN START-----------------------------------------------------------------------------------------
crime_data = getCrimeData()

#Data Calculations
regional_crime = getCrimeTotals(crime_data, "Region")
state_violence = getCrimeTotals(crime_data, "State", larceny=False)
state_murders = getSpecificCrime(crime_data, "State", "Murder")
midwest_data = getSpecificGov(crime_data, "Region", "Midwest")
midwest_larceny = getCrimeTotals(midwest_data, "State", violent=False)
midwest_violence = getCrimeTotals(midwest_data, "State", larceny=False)

#Print Charts & Tables
displayMurderRate()
print("\nANALYSIS OF FEDERAL CRIME DATA")
plotPieChart("CRIME BY REGION", "Region", regional_crime)
plotBarChart("VIOLENCE BY STATE", "State", state_violence)
plotSimpleHistogram("MURDER FREQUENCY IN THE STATES", state_murders)
plotBarChart("LARCENY IN THE MIDWEST", "State", midwest_larceny)
#plotMultiDimensionalHistogram([midwest_violence, midwest_larceny], "MIDEST (Violence + Larceny)")



