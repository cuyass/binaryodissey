import os
import sys
import re
import yaml

def extract_frontmatter(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"---\n(.*?)\n---", content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as e:
            print(f"FATAL reading frontmatter in {filepath}: {e}")
    return {}

def collect_tags(base_dir):
    tags = set()
    notes = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                fm = extract_frontmatter(path)
                if "tags" in fm:
                    for t in fm["tags"]:
                        tags.add(t)
                    notes.append((fm.get("title", file), path, fm["tags"]))
    return sorted(tags), notes

if __name__ == "__main__":
    base_dir = "."
    tags, notes = collect_tags(base_dir)

    if len(sys.argv) == 1:
        print("\nAvailable tags:\n")
        for t in tags:
            print(f"- {t}")
        print("\nUse: python tags_manager.py TAG to filter tags.")
    else:
        tag = sys.argv[1]
        results = [(title, path) for title, path, note_tags in notes if tag in note_tags]

        if results:
            print(f"\nNotes with tag '{tag}':\n")
            for title, path in results:
                print(f"- {title} ({path})")
        else:
            print(f"\nNo notes were found with tag '{tag}'.")
