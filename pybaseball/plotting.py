import altair as alt
import pandas as pd
from pathlib import Path


CUR_PATH = Path(__file__).resolve().parent
STADIUM_COORDS = pd.read_csv(
    Path(CUR_PATH, 'mlbstadiums.csv'), index_col=0
)
# transform over x axis
STADIUM_COORDS['y'] *= -1


def plot_stadium(team):
    """
    Plot the outline of the specified team's stadium using MLBAM coordinates

    Parameters
    ----------
    team: name of team whose stadium you want plotted
    """
    coords = STADIUM_COORDS[STADIUM_COORDS['team'] == team.lower()]
    stadium = alt.Chart(coords).mark_line().encode(
        x=alt.X('x', axis=None),
        y=alt.Y('y', axis=None),
        color=alt.Color(
            'segment', scale=alt.Scale(range=['grey']), legend=None
        ),
        order='segment'
    )

    return stadium


def spraychart(data, team_stadium, title='', tooltips=[]):
    """
    Produces a spraychart using statcast data overlayed on specified stadium

    Parameters
    ----------
    data: statcast batter data
    team_stadium: team whose stadium the hits will be overlaid on
    title: title of plot
    tooltips: list of variables in data to include as tooltips
    """

    # pull stadium plot to overlay hits on
    base = plot_stadium(team_stadium)
    # scatter plot of hits
    scatter = alt.Chart(data, title=title).mark_circle().encode(
        x=alt.X('hc_x:Q', axis=None),
        y=alt.Y('y:Q', axis=None),
        tooltip=tooltips
    ).transform_calculate(
        y='datum.hc_y * -1'
    )

    plot = alt.layer(base, scatter)
    return plot
