from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    states = get_state_options()
    #print(states)
    return render_template('home.html', state_options=states)
    
@app.route('/countyoptions')
def counties():
    state = request.args.get('state')
    counties = get_county_options(state)
    under18 = county_most_under_18(state)
    tworaces = county_most_2_or_more_races(state)
    fact1 = "In " + state + ", there is "+ str(under18) + "% of people who are under 18 years old "
    fact2 = "In " + state + ", there is "+ str(tworaces) + "% of people who are two or more races "
    return render_template('county.html', Fact1=fact1, Fact2=fact2, county_options=counties)

@app.route('/showFact')
def render_fact():
    states = get_state_options()
    county = request.args.get('county')
    county3 = data_for_county(county)
    fact2 = "In " + county + ", there is "+ str(county3) + "% of people who are two or more races "
    return render_template('home.html', state_options=states, Fact2=fact2)
    
def get_state_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    states=[]
    for c in counties:
        if c["State"] not in states:
            states.append(c["State"])
    options=""
    for s in states:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
def get_county_options(state):

    with open('demographics.json') as demographics_data:
        counties_data = json.load(demographics_data)
    counties=[]
    for c in counties_data:
        if c["State"] == state:
            counties.append(c["County"])
    options=""
    for c in counties:
        options += Markup("<option value=\"" + c + "\">" + c + "</option>")
    return options

def county_most_under_18(state):
    """Return the name of a county in the given state with the highest percent of under 18 year olds."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    highest=0
    county1 = ""
    for c in counties:
        if c["State"] == state:
            if c["Age"]["Percent Under 18 Years"] > highest:
                highest = c["Age"]["Percent Under 18 Years"]
                county1 = c["County"]
    return county1
    
def county_most_2_or_more_races(state):
    """Return the name of a county in the given state with the highest percent of under 18 year old."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    highest=0
    county2 = ""
    for c in counties:
        if c["State"] == state:
            if c["Ethnicities"]["Two or More Races"] > highest:
                highest = c["Ethnicities"]["Two or More Races"]
                county2 = c["County"]
    return county2
    
def data_for_county(county):
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    county3 = ""
    for c in counties:
        if c["County"] == county:
            county3 = c["Ethnicities"]["Two or More Races"]
    return county3
def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url


if __name__ == '__main__':
    app.run(debug=False) # change to False when running in production
