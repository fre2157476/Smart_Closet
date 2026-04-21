import plotly.figure_factory as ff
from datetime import date

df = [
    dict(Task="Leaving the Shire", Start=date(2025, 1, 1), Finish=date(2025, 1, 10), Completion=100),
    dict(Task="Crossing the Old Forest", Start=date(2025, 1, 11), Finish=date(2025, 1, 20), Completion=90),
    dict(Task="Journey to Bree", Start=date(2025, 1, 21), Finish=date(2025, 1, 30), Completion=80),
    dict(Task="Meeting Strider", Start=date(2025, 1, 31), Finish=date(2025, 2, 5), Completion=70),
    dict(Task="Journey to Rivendell", Start=date(2025, 2, 6), Finish=date(2025, 2, 20), Completion=60),
    dict(Task="Crossing the Mines of Moria", Start=date(2025, 2, 21), Finish=date(2025, 2, 28), Completion=50),
    dict(Task="Reaching Lothlórien", Start=date(2025, 3, 1), Finish=date(2025, 3, 10), Completion=40),
    dict(Task="Traveling the Anduin River", Start=date(2025, 3, 11), Finish=date(2025, 3, 20), Completion=30),
    dict(Task="Entering Mordor", Start=date(2025, 3, 21), Finish=date(2025, 3, 31), Completion=20),
    dict(Task="Climbing Mount Doom", Start=date(2025, 4, 1), Finish=date(2025, 4, 7), Completion=10),
]

fig = ff.create_gantt(df, colors='Cividis', index_col="Completion", show_colorbar=True)
fig.update_yaxes(autorange="reversed")
fig.update_layout(title="Ring Trip")
fig.show()  # This shows on browser window
