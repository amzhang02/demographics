from graphics import *
import json

makeGraphicsWindow(1200,550)     
        

def startWorld(world):
    #Setting background color to light blue
    setBackground("lightskyblue")
    #Open and load the countries.json file (information about the countries)
    countries_file = open('countries.json', 'r')
    world.countries = json.load(countries_file)
    #Open the file with data about crime for each country
    world_crime_data = open("world-crime-data.csv", "r")
    #Create empty colors dictionary
    world.colorsdict = {}
    #Create empty assault data dictionary
    world.datadict={}
    #For loop that assigns each data value for assault rate in the crime data file to a color in the gradient
    for line in world_crime_data:
        line = line.strip()
        (numeric_code, country_name, data_year, data_name, data_value) = line.split(",")
        if data_name == "Assault rate per 100000 population":
            numeric_code = int(numeric_code)
            data_value = float(data_value)
            red = 255
            green = (-0.191*data_value) + 255
            blue = (-0.191*data_value) + 255            
            color = (red, green, blue)
            #Appending values into the empty dictionaries created previously    
            world.colorsdict[numeric_code]=color
            world.datadict[numeric_code]=data_value

def updateWorld(world):
    pass

def drawWorld(world):
    #Get the mouse's coordinates
    (mousex,mousey) = getMousePosition()
    
    #title the map
    drawString("Assault rate per 100000 population", 10, 480)
    
    #Makes a key for the colors
    fillRectangle(10, 10, 20, 20, "gray")
    drawString(" = No data", 30, 10)
    drawRectangle(10, 40, 20, 255)
    for y in range(0,256):
        color = (255, -y + 255, -y + 255)
        drawLine(10, y+40, 30, y+40, color)
    drawString(" = Smallest", 30, 40)
    drawString(" = Largest", 30, 280)
    
    #First For loop assigns variables to elements in the dictionary of countries
    for country in world.countries:
        polygons = country["polygons"]
        numeric_code = country["number"]
        country_name = country["name"]
        #Second For loop fills the country polygons with the color in the gradient that corresponds to the assault rate
        for polygon in polygons:
            if numeric_code in world.colorsdict:
                fillPolygon(polygon, world.colorsdict[numeric_code])
            else:
                #Fills countries with no data with gray
                fillPolygon(polygon, "gray")
            #Draws the outline of the countries in black
            drawPolygon(polygon)
            #Draws strings for country name and its assault rate data value if the mouse is within the country polygon
            if pointInPolygon(mousex, mousey, polygon):
                drawString(country_name, 10, 510)
                if numeric_code in world.datadict:
                    drawString(world.datadict[numeric_code], 200, 510)
                else:
                    #Draws string "no data" for countries that do not have data when mouse is in said country
                    drawString("No data", 200, 510)

runGraphics(startWorld, updateWorld, drawWorld)