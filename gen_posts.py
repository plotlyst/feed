import csv
import json
import re
from dataclasses import dataclass, asdict


@dataclass
class Status:
    text: str
    id: str
    color_hexa: str


@dataclass
class Tag:
    text: str
    icon: str
    icon_color: str


statuses = [
    Status("Planned", "dcce7399-a45c-4ff4-a699-03fd01e3cb08", "#0077b6"),
    Status("In progress", "c36602fe-d08b-4554-8526-b3f034131c39", "#9f86c0"),
    Status("Done", "cfa85d26-524c-4364-b089-691000094b52", "#588157")
]

tags = {
    "character": Tag("Character related tasks", "fa5s.user", "darkBlue"),
    "milieu": Tag("Milieu and worldbuilding related tasks", "mdi.globe-model", "#2d6a4f"),
    "scene": Tag("Scene related tasks", "mdi.movie-open", "#4B0763")
}


def get_status_id(status_text):
    for status in statuses:
        if status.text == status_text:
            return status.id
    return None


def parse_tags_and_clean_summary(content):
    pattern = r"#(\w+)"
    tag_matches = re.findall(pattern, content)
    cleaned_content = re.sub(pattern, '', content).strip()
    cleaned_content = cleaned_content.rstrip('\n')  # Remove trailing newlines from the summary
    return [tag for tag in tag_matches if tag in tags], cleaned_content


tasks = []

with open('posts-input.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        task_tags, cleaned_summary = parse_tags_and_clean_summary(row["Content"])
        task = {
            "title": row["Title"],
            "status_ref": get_status_id(row["Status"]),
            "summary": cleaned_summary,
            "votes": int(row["Upvote Count"]),
            "tags": task_tags,
            "web_link": row["Link"],
            "version": row["Tags"]
        }
        tasks.append(task)

output = {
    "tasks": tasks,
    "statuses": [asdict(status) for status in statuses],
    "tags": {key: asdict(tag) for key, tag in tags.items()}
}

with open('posts.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(output, jsonfile, ensure_ascii=False, indent=2)
