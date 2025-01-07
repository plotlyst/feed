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
    icon_color: str = "#4B0763"


statuses = [
    Status("Planned", "dcce7399-a45c-4ff4-a699-03fd01e3cb08", "#0077b6"),
    Status("In Progress", "c36602fe-d08b-4554-8526-b3f034131c39", "#9f86c0"),
    Status("Completed", "cfa85d26-524c-4364-b089-691000094b52", "#588157")
]

tags = {
    "character": Tag("Character related tasks", "fa5s.user"),
    "scene": Tag("Scene related tasks", "mdi.movie-open"),
    "structure": Tag("Story structure related tasks", "mdi6.bridge"),
    "milieu": Tag("Milieu and world-building related tasks", "mdi.globe-model"),
    "manuscript": Tag("Manuscript related tasks", "fa5s.scroll"),
    "documents": Tag("Document and mindmap related tasks", "mdi.file-document-outline"),
    "series": Tag("Series related tasks", "ph.books"),
    "appearance": Tag("General application appearance and style", "fa5s.palette"),
    "quality of life": Tag("Quality of life improvements", "fa5s.hand-holding-heart"),
    "knowledge base": Tag("Knowledge base and guides", "mdi6.school-outline"),
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
    return [tag.replace('_', ' ') for tag in tag_matches if tag.replace('_', ' ') in tags], cleaned_content


tasks = []

with open('/home/zkovari/Downloads/plotlyst-fb.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["Status"] == 'In Review':
            continue
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
