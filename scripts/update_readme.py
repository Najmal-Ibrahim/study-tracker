import json

README_FILE = "README.md"
STATS_FILE = "data/stats.json"

START_MARKER = "<!--START_SECTION:mastery-->"
END_MARKER = "<!--END_SECTION:mastery-->"

# -----------------------------------
# LOAD STUDY DATA
# -----------------------------------

with open(STATS_FILE, "r") as file:
    stats = json.load(file)

# -----------------------------------
# GENERATE PROGRESS BARS
# -----------------------------------

def generate_progress_bar(value, max_value=20):

    filled = min(value, max_value)

    empty = max_value - filled

    return "█" * filled + "░" * empty

# -----------------------------------
# BUILD README SECTION
# -----------------------------------

section = "## 📚 AI Mastery Progress\n\n"

total_pomodoros = sum(stats.values())

section += f"### Total Pomodoros: {total_pomodoros}\n\n"

for topic, value in stats.items():

    progress_bar = generate_progress_bar(value)

    section += (
        f"### {topic.title()}\n"
        f"`{progress_bar}`\n\n"
        f"Pomodoros: {value}\n\n"
    )

# -----------------------------------
# LOAD README
# -----------------------------------

with open(README_FILE, "r", encoding="utf-8") as file:
    readme = file.read()

# -----------------------------------
# REPLACE SECTION
# -----------------------------------

start_index = readme.index(START_MARKER) + len(START_MARKER)

end_index = readme.index(END_MARKER)

updated_readme = (
    readme[:start_index]
    + "\n\n"
    + section
    + "\n"
    + readme[end_index:]
)

# -----------------------------------
# SAVE UPDATED README
# -----------------------------------

with open(README_FILE, "w", encoding="utf-8") as file:
    file.write(updated_readme)

print("README updated successfully.")