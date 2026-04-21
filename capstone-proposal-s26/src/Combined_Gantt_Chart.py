import plotly.figure_factory as ff
from datetime import date

# Updated data with "Ring Trip" tasks and "Sam" and "Frodo"
df = ([
    dict(Task="Leaving the Shire", Start=date(2025, 1, 28), Finish=date(2025, 2, 2), Resource="Sam"),
    dict(Task="Scouting the Path to Bree", Start=date(2025, 1, 31), Finish=date(2025, 2, 5), Resource="Frodo"),
    dict(Task="Crossing the Old Forest", Start=date(2025, 2, 2), Finish=date(2025, 2, 11), Resource="Sam"),
    dict(Task="Arriving at Bree", Start=date(2025, 2, 5), Finish=date(2025, 2, 20), Resource="Frodo"),
    dict(Task="Meeting Aragorn", Start=date(2025, 2, 11), Finish=date(2025, 2, 20), Resource="Sam"),
    dict(Task="Journey to Rivendell", Start=date(2025, 2, 20), Finish=date(2025, 2, 27), Resource="Sam/Frodo"),
    dict(Task="Crossing the Mines of Moria", Start=date(2025, 2, 27), Finish=date(2025, 3, 4), Resource="Frodo"),
    dict(Task="Reaching Lothlórien", Start=date(2025, 2, 27), Finish=date(2025, 3, 11), Resource="Sam"),
    dict(Task="Traveling Down the Anduin", Start=date(2025, 3, 4), Finish=date(2025, 3, 11), Resource="Frodo"),
    dict(Task="Splitting the Fellowship", Start=date(2025, 3, 11), Finish=date(2025, 3, 15), Resource="Frodo"),
    dict(Task="Entering Mordor", Start=date(2025, 3, 11), Finish=date(2025, 3, 25), Resource="Frodo"),
    dict(Task="Navigating the Plains of Gorgoroth", Start=date(2025, 3, 11), Finish=date(2025, 3, 25), Resource="Sam"),
    dict(Task="Climbing Mount Doom", Start=date(2025, 3, 25), Finish=date(2025, 4, 1), Resource="Sam/Frodo"),
    dict(Task="Destroying the Ring", Start=date(2025, 4, 1), Finish=date(2025, 4, 15), Resource="Sam/Frodo")
])

# Updated colors for "Sam" and "Frodo"
colors = {
    'Sam': 'rgb(109, 130, 153)',
    'Frodo': 'rgb(49, 107, 131)',
    'Sam/Frodo': 'rgb(140, 161, 165)',
    'Complete': 'rgb(250, 180, 200)'
}

# Create Gantt chart
fig = ff.create_gantt(df, colors=colors, index_col="Resource", show_colorbar=True)
fig.update_layout(title="Ring Trip")
fig.update_yaxes(autorange="reversed")

# Display the chart
fig.show()
