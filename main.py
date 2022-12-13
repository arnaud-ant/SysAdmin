# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# pylint: disable-msg=E0401,C0411,W0611,R0915,W0612,W0613,W0602,C0114,C0209,R0912,R0914
from audioop import add
from cgitb import reset
import datetime
import time

import plotly.express as px
import plotly.graph_objects as go
import plotly
import pandas as pd
from dash.dependencies import Input, Output
import paramiko
import json

from Script import *

import dash
from dash import dcc
from dash import html



# On récupère les informations du fichier json
f = open('machine_names.json')
fdata = json.load(f)
machines = []
df = {}
isDown = {}

# On initialise quelques valeurs avec les machines fraichement récupérées
for name in fdata['machines']:
    print(name)
    df[name['value']] = pd.DataFrame({
        "Time": [],
        "RAM": [],
        "CPU": [],
        "Ping": [],
        "404": [],
    })
    isDown[name['value']] = False
    machines.append(name)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# La première machine sur laquelle on se connecte
value = machines[0]['value']
valueTried = value

# INITIALISATION DES VALEURS :
oldLengthLastMinute = 0
oldStatByPage = {}
oldStatByConnection = {}
oldStatBy404 = {}
dataInit = []
lstNb404 = []
firstIteration = True
resetGraphs = False

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)


# On essaye de se connecter une prémière fois, à la première machine de la liste
try:
    client.connect(value, port=22, username="user",
                   password="pass!", timeout=200, banner_timeout=200)
    isDown[value] = False
except paramiko.SSHException as e:
    # Si ça ne fonctionne pas on indique bien qu'elle est down
    isDown[value] = True

# On fait le modèle du layout
app.layout = html.Div(children=[


    dcc.Store(id='store'),

    #html.H1(children="Caractéristiques de " + machineName + " :"),
    html.H1(id='machine-name'),

    #html.Div(id='cpu'),
    dcc.Dropdown(
        id='demo-dropdown',
        options=machines,
        value=value
    ),
    dcc.Graph(id='timeseries'),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # in milliseconds
        n_intervals=0
    ),
])

# Définition de la connection qu'on réutilise plus tard à chaque fois que l'on veut se reconncter
def Connect(value):
    global isDown
    try:
        client.connect(value, port=22, username="user", password="pass",
        timeout=100, banner_timeout=100)
        isDown[value] = False
    except paramiko.SSHException as e:
        isDown[value] = True
        print("La connexion n'a pas abouti :(")
    except paramiko.ssh_exception.NoValidConnectionsError as e:
        print("Pas de réponse")
        isDown[value] = True


# Callback toutes les 5 secondes, ou quand on clique sur une nouvelle machine
# pour mettre à jour l'état de la machine :
@app.callback(
    Output('machine-name', 'children'),
    Input('demo-dropdown', 'value'),
    Input('interval-component', 'n_intervals')
)
def UpdateOutput(value, n):

    # En fcontion de l'état de la machine, on change le titre HTML
    if isDown[value]:
        return '\U0000274C La machine {} ne réponds pas.'.format(value)
    if valueTried!=value:
        return '\U0000274C La machine {} ne réponds pas.'.format(value)
    return '\U00002705 Machine {} opérationelle.'.format(value)



# Callback qui stocke quelques valeurs
# et qui demande la reconnexion quand on clique sur une nouvelle machine
@app.callback(
    Output('store', 'data'),
    Input('demo-dropdown', 'value')
)
def UpdateOutput(value):
    # Quand on change de moniteur, on reset toutes les valeurs.
    global oldLengthLastMinute, lstNb404, firstIteration
    global df, client, oldStatBy404, oldStatByPage, oldStatByConnection
    global resetGraphs, isDown, fig, valueTried

    resetGraphs = True
    valueTried = value
    Connect(value)

    # INITIALISATION DES VALEURS :

    oldLengthLastMinute = 0
    oldStatByPage = {}
    oldStatByConnection = {}
    oldStatBy404 = {}
    lstNb404 = []
    firstIteration = True

    return value


# Callback toutes les 5 secondes, pour mettre à jour les graphes :
@app.callback(Output('timeseries', 'figure'),
              Input('interval-component', 'n_intervals'),
              Input('store', 'data'))
def UpdateOutputDiv(n, mName):
    global df, client, oldStatBy404, oldStatByPage, oldStatByConnection
    global oldLengthLastMinute, lstNb404, firstIteration, statByPage, valueTried
    global resetGraphs

    # Si on a pas pu se Connecter, ou que le serveur est down, on ne renvoie rien.
    if (valueTried!=mName or isDown[mName]):
        Connect(mName)
        return {}

    # Sinon on fait tout nos calculs
    else:
        if resetGraphs:
            resetGraphs = False
            newStatByPage = {}
            statByPage = {}

        dataInit = []
        # DEBUT RECUP DATA
        print(mName)

        currentDate = datetime.datetime.now()

        _, stdout, stderr = client.exec_command("free")
        output = stdout.read().decode("utf-8")

        dataInit.append(output)

        _, stdout, stderr = client.exec_command("cat /proc/stat")
        output = stdout.read().decode("utf-8")
        output.splitlines()

        dataInit.append(output)

        start = time.time()
        client.exec_command("ls")
        end = time.time()
        ping = (end-start)*1000

        dataInit.append(ping)

        # format data : RAM (en %) , CPU (en %) , ping (en ms)
        data = TransformData(dataInit)
        data[1] = data[1]*100
        # Récupere le nombre d'entré dans les logs à executer toute les X minutes

        _, stdout, stderr = client.exec_command(
            "wc -l /var/log/apache2/access.log")
        output = stdout.read().decode("utf-8")

        newLengthLastMinute = GetActivityLastMinute(output)
        nbConnectLastMinute = newLengthLastMinute - oldLengthLastMinute
        oldLengthLastMinute = newLengthLastMinute

        # récupere les N nouvelles entrées du fichier de log

        command = "tail -n" + str(nbConnectLastMinute) + \
            " /var/log/apache2/access.log"
        _, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode("utf-8")
        output.splitlines()
        logs = GetLog(output)
        # On note le nombre d'erreur 404 renvoyé par le serveur les dernieres X minutes

        nb404 = GetNb404(logs)

        lstNb404.append(nb404)

        # Pour ne rien afficher à la première itération.
        if firstIteration:
            nb404 = 0
            nbConnectLastMinute = 0
            firstIteration = False
        # On enlève les logs des x dernières heures
        nbHourDiff = 30000
        tmpLogs = GetLogsByTime(logs, nbHourDiff)
        newStatByPage = GetStatByPage(tmpLogs)

        # On met à jour la variable statByPage qui contient le nom de la page
        # et le nombre d'acces à la page
        statByPage = FusionDico(newStatByPage, statByPage)

        # Initialisation du tableau du nombre de visite par page.
        sites = []
        nb = []
        for key in statByPage:
            if statByPage[key]:
                if len(key) > 30:
                    tempKey = key[0:30]
                    tempKey += "..."
                else:
                    tempKey = key
                sites.append(tempKey)
            if statByPage[key]:
                nb.append(statByPage[key])

        oldStatByPage = newStatByPage

        newStatByConnection = GetStatByConnection(logs)

        # On met à jour la variable statByPage qui contient le nom de la page
        # et le nombre d'acces à la page
        oldStatByConnection = newStatByConnection
        newStatBy404 = GetStatBy404(logs)
        oldStatBy404 = newStatBy404

        # On récupère toutes les données fraichment calculées, pour les mettre sous la forme voulue
        # afin de pouvoir les afficher correctement dans les graphes.
        dfappend = pd.DataFrame({
            "Time": [currentDate],
            "RAM": [data[0]],
            "CPU": [data[1]],
            "Ping": [data[2]],
            "404": [nb404],
            "Connections": [nbConnectLastMinute],
        })


        # On ajoute dfappend au df de la machine.
        # Grace à ceci, quand on passe d'une machine à l'autre,
        # on ne perds pas les données calculées depuis la connexion.
        df[mName] = df[mName].append(dfappend, ignore_index=True)

        # Subplot pour agencer l'affichage des données.
        fig = plotly.subplots.make_subplots(
            rows=5, cols=4,
            specs=[
                [{"type": "indicator"}, {"type": "indicator"},
                    {"rowspan": 5, "colspan": 2}, None],
                [{"rowspan": 2, "colspan": 2}, None, None, None],
                [None, None, None, None],
                [{"rowspan": 2, "colspan": 2}, None, None, None],
                [None, None, None, None]],
            print_grid=False)
        fig['layout']['margin'] = {
            'l': 30, 'r': 10, 'b': 30, 't': 10
        }
        fig['layout']['legend'] = {'x': 1.08, 'y': 1, 'xanchor': 'center'}

        # Pour comparer avec l'ancienne valeur de la RAM
        if len(df[mName]) == 1:
            oldRAM = df[mName]['RAM'][0]
        else:
            oldRAM = df[mName]['RAM'][len(df[mName])-2]
        fig.append_trace(go.Indicator(
            mode="number+delta+gauge",
            value=df[mName]['RAM'][len(df[mName])-1],
            title={'text': "RAM", 'font': {'size': 18}, 'align': "center"},
            delta={'reference': oldRAM, 'increasing': {'color': "red"},
                   'decreasing': {'color': "RebeccaPurple"}, "valueformat": ".2f"},
            number={
                'suffix': " %",
            },
            gauge={
                # 'shape' : 'bullet',
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {
                    'thickness': .8,
                    'color': 'red'

                },
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",

            }), 1, 1)

        if len(df[mName]) == 1:
            oldCPU = df[mName]['CPU'][0]
        else:
            oldCPU = df[mName]['CPU'][len(df[mName])-2]
        fig.append_trace(go.Indicator(
            mode="number+delta+gauge",
            value=df[mName]['CPU'][len(df[mName])-1],
            title={'text': "CPU", 'font': {'size': 18}, 'align': "center"},
            delta={'reference': oldCPU, 'increasing': {'color': "red"},
                   'decreasing': {'color': "RebeccaPurple"}, "valueformat": ".2f"},
            number={
                'suffix': " %",
            },
            gauge={
                # 'shape' : 'bullet',
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {
                    'thickness': .8,
                    'color': 'yellow'
                },
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
            }), 1, 2)

        fig.append_trace({
            'x': df[mName]['Time'],
            'y': df[mName]['Ping'],
            'name': 'Ping',
            'mode': 'lines+markers',
            'type': 'scatter'
        }, 2, 1)

        fig.append_trace(go.Scatter(
            name="Nombre 404",
            x=df[mName]['Time'], y=df[mName]['404']), 4, 1)

        fig.append_trace(go.Scatter(
            name="Nombre Connections",
            x=df[mName]['Time'], y=df[mName]['Connections']), 4, 1)

        fig.add_trace(go.Bar(
            name="Connexion par page",
            x=sites, y=nb),
            1, 3)


        fig.update_layout(barmode='group', bargap=0, bargroupgap=0,
                          height=900,  margin=dict(l=60, r=25, b=40, t=40))

        #fig.update_layout(height=700, yaxis1=dict(range=[0, 100]), yaxis2=dict(range=[0, 100]))
        return fig


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True)
