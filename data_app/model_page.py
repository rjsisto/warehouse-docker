from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
from joblib import load

import os
# MODEL_FOLDER = os.getenv("MODEL_FOLDER")
# DATA_FOLDER = os.getenv("DATA_FOLDER")

MODEL_FOLDER = "src/models"
DATA_FOLDER = "src/data"
# create a dashboard that shows these graphs by each warehouse

#!! pandas import/data wrangling for presentation stuff

gbr_model_old = load(MODEL_FOLDER + "/gbr_improved.joblib")
master_data = pd.read_csv(DATA_FOLDER + "/master_dataset.csv")
hours = pd.read_csv(DATA_FOLDER + "/random_hours.csv")
gbr_model_old = load(MODEL_FOLDER + "/gbr_improved.joblib")
gbr_model = load(MODEL_FOLDER + "/gbr_improved_3.joblib")
xtratree_model = load(MODEL_FOLDER + "/xtra_tree.joblib")
randfor_model = load(MODEL_FOLDER + "/rfr.joblib")

#!! model stuff
# TODO will probably want to add a standard randomized seed
model_data = master_data[master_data["cases_hrs"] <= 300]
model_data = model_data[model_data["Total_Hours"] >= 10]

# dropping all of the redundant columns
to_drop = ["Total_Hours", "Total_Cases", "B_HrsPct", "B_Cases",
           "Total_Each_Day", "dry_ratio", "clr_ratio", "frz_ratio", "LABEL_TYPE"]
model_data.drop(labels=to_drop, axis=1, inplace=True)
model_data.rename(columns={"BRNCH_CD": "brnch_cd", "A_HrsPct": "a_hrspct",
                  "C_HrsPct": "c_hrspct", "A_Cases": "a_cases", "C_Cases": "c_cases"}, inplace=True)
dates = model_data.pop("Date")
go_live = model_data.pop("GO_LIVE_DATE")

# removing the real values
y = model_data.pop('cases_hrs')
X = model_data


# 1=gbr; 2=xtratree; 3=randfor; 4=old gbr
def model_pred(model):
    # replacing the actual cpmh values with predicted ones from the model
    df_pred = X
    if (model == 1):
        df_pred['cases_hrs_pred'] = gbr_model.predict(X)
    if (model == 2):
        df_pred['cases_hrs_pred'] = xtratree_model.predict(X)
    if (model == 3):
        df_pred['cases_hrs_pred'] = xtratree_model.predict(X)
    if (model == 4):
        df_pred['cases_hrs_pred'] = xtratree_model.predict(X)
    df_pred['cases_hrs_real'] = y
    df_pred['Date'] = dates
    df_pred["GO_LIVE_DATE"] = go_live
    df_pred['Date'] = pd.to_datetime(df_pred['Date'])
    return df_pred


#!! creating a dictionary that will allow the branch names to appear in the dropdown menu
div_nm = hours['FULL_MARKET_NAME'].unique()
brnch = model_data['brnch_cd'].unique()
branches = {}
for b in brnch:
    for d in div_nm:
        if b in d:
            branches[b] = d


# TODO maybe use just one graph and allow the user to pick the model they want to use to predict the data
#!! dash stuff
layout = html.Div([
    html.H1("Warehouse Analytics"),
    html.Div([
        html.H3(
            "Predicted Productivity vs Actual Productivity over time per Branch using GBR"),
        dcc.Dropdown(branches, "2Z", id='dropdown-pred-real_gbr'),
        dcc.Graph(id="pred_real_gbr"),
    ]),
    html.Div([
        html.H3(
            "Predicted Productivity vs Actual Productivity over time per Branch using XtraTrees"),
        dcc.Dropdown(branches, "2Z", id='dropdown-pred-real_xtra'),
        dcc.Graph(id="pred_real_xtra"),
    ]),
    html.Div([
        html.H3(
            "Predicted Productivity vs Actual Productivity over time per Branch using Old GBR"),
        dcc.Dropdown(branches, "2Z", id='dropdown-pred-real_oldgbr'),
        dcc.Graph(id="pred_real_oldgbr"),
    ])
])


app = Dash(__name__)
app.layout = layout

"""Graphing real values over predicted values using GBR"""


@app.callback(
    Output("pred_real_gbr", "figure"),
    Input("dropdown-pred-real_gbr", "value"),
)
def display_gbr(value):
    df = model_pred(1)
    df = df[df['brnch_cd'] == value]
    fig = go.Figure([
        go.Scatter(x=df['Date'], y=df['cases_hrs_pred'],
                   name="Predicted Values"),
        go.Scatter(x=df['Date'], y=df['cases_hrs_real'], name="Real Values")
    ])
    # fig.add_vline(x=df.iloc[0][10], line_width=3)
    # fig.add_vline(x=datetime(2020, 3, 1), line_width=3, line_color="green")
    return fig


"""Graphing real values over predicted values using XtraTrees"""


@app.callback(
    Output("pred_real_xtra", "figure"),
    Input("dropdown-pred-real_xtra", "value"),
)
def display_xtra(value):
    df = model_pred(2)
    df = df[df['brnch_cd'] == value]
    fig = go.Figure([
        go.Scatter(x=df['Date'], y=df['cases_hrs_pred'],
                   name="Predicted Values"),
        go.Scatter(x=df['Date'], y=df['cases_hrs_real'], name="Real Values")
    ])
    # fig.add_vline(x=df.iloc[0][10], line_width=3)
    # fig.add_vline(x=datetime(2020, 3, 1), line_width=3, line_color="green")
    return fig


"""Graphing real values over predicted values using Old GBR"""


@app.callback(
    Output("pred_real_oldgbr", "figure"),
    Input("dropdown-pred-real_oldgbr", "value"),
)
def display_oldgbr(value):
    df = model_pred(4)
    df = df[df['brnch_cd'] == value]
    fig = go.Figure([
        go.Scatter(x=df['Date'], y=df['cases_hrs_pred'],
                   name="Predicted Values"),
        go.Scatter(x=df['Date'], y=df['cases_hrs_real'], name="Real Values")
    ])
    # fig.add_vline(x=df.iloc[0][10], line_width=3)
    # fig.add_vline(x=datetime(2020, 3, 1), line_width=3, line_color="green")
    return fig


app.run_server(debug=True, port=8888, host="0.0.0.0")

# TODO look at rmse for each month
# maybe some months have more error than others - this could help us improve the model
# do the same for weekdays
