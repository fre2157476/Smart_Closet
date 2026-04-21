import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Define tasks and sub-tasks
tasks = [
    {
        "Task": "Leaving the Shire",
        "Subtasks": [
            {"Task": "Crossing the Old Forest", "Start": datetime(2025, 2, 2), "Finish": datetime(2025, 2, 5), "Resource": "Sam"},
            {"Task": "Scouting the Path to Bree", "Start": datetime(2025, 1, 31), "Finish": datetime(2025, 2, 5), "Resource": "Frodo"},
            {"Task": "Arriving at Bree", "Start": datetime(2025, 2, 5), "Finish": datetime(2025, 2, 6), "Resource": "Frodo"},
        ],
        "Resource": "Sam/Frodo",
    },
    {
        "Task": "Meeting Aragorn",
        "Subtasks": [],
        "Start": datetime(2025, 2, 7),
        "Finish": datetime(2025, 2, 8),
        "Resource": "Sam",
    },
    {
        "Task": "Journey to Rivendell",
        "Subtasks": [],
        "Start": datetime(2025, 2, 9),
        "Finish": datetime(2025, 2, 27),
        "Resource": "Sam/Frodo",
    },

    {"Task": "Crossing the Mines of Moria", "Start": datetime(2025, 2, 27), "Finish": datetime(2025, 3, 4), "Resource": "Frodo"},
    {"Task": "Reaching Lothlórien", "Start": datetime(2025, 2, 27), "Finish": datetime(2025, 3, 11), "Resource": "Sam"},
    {"Task": "Traveling Down the Anduin", "Start": datetime(2025, 3, 4), "Finish": datetime(2025, 3, 11), "Resource": "Frodo"},
    {"Task": "Entering Mordor", "Start": datetime(2025, 3, 11), "Finish": datetime(2025, 3, 25), "Resource": "Frodo"},
    {"Task": "Navigating the Plains of Gorgoroth", "Start": datetime(2025, 3, 11), "Finish": datetime(2025, 3, 25), "Resource": "Sam"},
    {"Task": "Climbing Mount Doom", "Start": datetime(2025, 3, 25), "Finish": datetime(2025, 4, 1), "Resource": "Sam/Frodo"},
    {"Task": "Destroying the Ring", "Start": datetime(2025, 4, 1), "Finish": datetime(2025, 4, 2), "Resource": "Frodo"},


]

# Process tasks to calculate parent finish dates and flatten for plotting
plot_tasks = []
for task in tasks:
    if task.get("Subtasks"):
        # Calculate parent task finish date based on latest subtask
        task["Start"] = min(subtask["Start"] for subtask in task["Subtasks"])
        task["Finish"] = max(subtask["Finish"] for subtask in task["Subtasks"])
        plot_tasks.append(task)
        # Add subtasks to the plot
        for subtask in task["Subtasks"]:
            subtask['Task'] = f"  - {subtask['Task']}"  # Prepend a dash
            plot_tasks.append(subtask)
    else:
        # Add tasks without subtasks
        plot_tasks.append(task)

# Sort tasks by Start date
plot_tasks = sorted(plot_tasks, key=lambda x: x["Start"])

# Map resources to colors
resource_colors = {
    "Sam": "skyblue",
    "Frodo": "orange",
    "Sam/Frodo": "green"
}

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

print(plot_tasks)
# Plot tasks
for i, task in enumerate(plot_tasks):
    start = task["Start"]
    finish = task["Finish"]
    color = resource_colors.get(task["Resource"], "gray")
    ax.barh(i, (finish - start).days, left=start, color=color, edgecolor="black", label=task["Resource"])
    # Left-justify labels
    ax.text(
        start,  # Place text at the start of the bar
        i,  # Align with the bar's vertical position
        task["Task"],
        va="center",  # Vertically align at the center of the bar
        ha="left",  # Left-justify the text
        fontsize=10
    )

# Format x-axis
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=45)

# Set y-ticks to empty (remove default labels)
ax.set_yticks([])
ax.set_xlabel("Time")
ax.set_title("Ring Trip with Sub-Tasks and Dynamic Parent Finish Dates")

# Remove duplicate legends
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

# Show earliest task on top
plt.gca().invert_yaxis()

# Adjust layout and display
plt.tight_layout()
fig.savefig('ring_trip_gantt.png')
plt.show()
