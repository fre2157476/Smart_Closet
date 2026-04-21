import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Define tasks and sub-tasks
tasks = [
    {
        "Task": "  Proposal Development",
        "Subtasks": [
            {"Task": "Pre-approval", "Start": datetime(2025, 1, 13), "Finish": datetime(2025, 2, 5)},
            {"Task": "Presentations", "Start": datetime(2025, 2, 5), "Finish": datetime(2025, 2, 14), "Color": "cyan"},
            {"Task": "Final approval", "Start": datetime(2025, 2, 5), "Finish": datetime(2025, 2, 17)},
        ],
        "Color" : "lightblue"
    },
    {
        "Task": "  Intermediate Milestone 1",
        "Subtasks": [
            {"Task": "Development", "Start": datetime(2025, 2, 5), "Finish": datetime(2025, 3, 10)},
            {"Task": "Spring Break", "Start": datetime(2025, 3, 3), "Finish": datetime(2025, 3, 9), "Color": "lightgreen"},
            {"Task": "Presentations", "Start": datetime(2025, 3, 10), "Finish": datetime(2025, 3, 14), "Color": "cyan"},
        ],
        "Color" : "lightblue"
    },
    {
        "Task": "  Intermediate Milestone 2",
        "Subtasks": [
            {"Task": "Development", "Start": datetime(2025, 3, 14), "Finish": datetime(2025, 4, 6)},
            {"Task": "Presentations", "Start": datetime(2025, 4, 7), "Finish": datetime(2025, 4, 11), "Color": "cyan"},
        ],
        "Color" : "lightblue"
    },
    {
        "Task": "  Final Sprint",
        "Subtasks": [
            {"Task": "Development", "Start": datetime(2025, 4, 14), "Finish": datetime(2025, 4, 22)},
            {"Task": "Capstone Fair", "Start": datetime(2025, 4, 22), "Finish": datetime(2025, 4, 23), "Color" : "red"},
        ],
        "Color" : "lightblue"
    },
    {
        "Task": "  Finish",
        "Subtasks": [
            {"Task": "Demonstration", "Start": datetime(2025, 4, 24), "Finish": datetime(2025, 4, 28)},
            {"Task": "Presentations", "Start": datetime(2025, 4, 30), "Finish": datetime(2025, 5, 3), "Color" : "red"},
        ],
        "Color" : "lightblue"
    },


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
    color = task.get("Color", "gray")
    ax.barh(i, (finish - start).days, left=start, color=color, edgecolor="black")
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
ax.set_title("CPSC 498 Capstone 2025 Dates")

# Remove duplicate legends
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

# Show earliest task on top
plt.gca().invert_yaxis()

# Adjust layout and display
plt.tight_layout()
fig.savefig('capstone_gantt.png')
plt.show()
