import os
import hashlib
import csv
import re

TARGET_DIR = "006_System-Manifests"
ABS_PATH_LIMIT = 220
FILENAME_LIMIT = 60
HASH_LEN = 6

FILLER_WORDS = [
    r"implementing-rules-and-regulations-of-the",
    r"implementing_rules_and_regulations_of_the",
    r"statement-that",
    r"statement_that",
    r"implementing-rules-and-regulations",
    r"implementing_rules_and_regulations",
    r"revised-implementing-rules-and-regulations",
    r"revised_implementing_rules_and_regulations",
    r"Full Implementing Rules and Regulations",
    r"Implementing Rules and Regulations",
]

ACRONYMS = {
    r"fire-code-of-the-philippines": "fcp",
    r"fire_code_of_the_philippines": "fcp",
    r"Fire Code of the Philippines": "fcp",
    r"national-building-code": "nbcp",
    r"national_building_code": "nbcp",
    r"National Building Code": "nbcp",
    r"batas-pambansa": "bp",
    r"batas_pambansa": "bp",
    r"Batas Pambansa": "bp",
    r"republic-act": "ra",
    r"republic_act": "ra",
    r"Republic Act": "ra",
    r"presidential-decree": "pd",
    r"presidential_decree": "pd",
    r"Presidential Decree": "pd",
    r"Professional Practice": "pp",
    r"Professional-Practice": "pp",
    r"Professional_Practice": "pp",
    r"Standards of": "standards",
}

def get_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()[:HASH_LEN]

def abbreviate(filename):
    name, ext = os.path.splitext(filename)
    
    # Apply acronyms
    for long_form, short_form in ACRONYMS.items():
        name = re.sub(long_form, short_form, name, flags=re.IGNORECASE)
    
    # Strip filler words
    for word in FILLER_WORDS:
        name = re.sub(word, "", name, flags=re.IGNORECASE)
    
    # Special handling for rel-*.md if needed (though target is 006_System-Manifests)
    # The prompt says: For relationship files (rel-*.md), strip out filler words.
    # These might be in 006_System-Manifests/runs/ or elsewhere.
    
    # Clean up multiple dashes/underscores/spaces
    name = re.sub(r'[-_\s]{2,}', '-', name)
    name = name.replace(' ', '-')
    name = name.strip('-_ ')
    
    if len(name) > FILENAME_LIMIT:
        h = get_hash(name)
        name = name[:FILENAME_LIMIT] + "-" + h
    
    return name + ext

def main():
    rename_map = {}
    base_path = os.path.abspath(".")
    
    print(f"Scanning {TARGET_DIR} for paths exceeding {ABS_PATH_LIMIT} characters...")
    
    # 1. Collect files to rename
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            old_rel_path = os.path.join(root, file)
            # Normalize path for matching
            old_rel_path = os.path.normpath(old_rel_path)
            abs_path = os.path.join(base_path, old_rel_path)
            
            if len(abs_path) > ABS_PATH_LIMIT:
                new_filename = abbreviate(file)
                new_rel_path = os.path.join(root, new_filename)
                new_rel_path = os.path.normpath(new_rel_path)
                
                # Collision check
                if new_rel_path in rename_map.values():
                    # Append extra hash if collision
                    name, ext = os.path.splitext(new_filename)
                    new_filename = f"{name}-{get_hash(old_rel_path)}{ext}"
                    new_rel_path = os.path.join(root, new_filename)
                    new_rel_path = os.path.normpath(new_rel_path)
                
                rename_map[old_rel_path] = new_rel_path

    if not rename_map:
        print("No files exceed the path limit.")
        # Create empty CSV anyway to satisfy the requirement
        with open("rename_manifest.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["old_path", "new_path"])
        return

    # 2. Output CSV
    with open("rename_manifest.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["old_path", "new_path"])
        # Sort by old_path for deterministic output
        for old in sorted(rename_map.keys()):
            writer.writerow([old, rename_map[old]])
    
    print(f"Generated rename_manifest.csv with {len(rename_map)} entries.")

    # 3. Update references
    # Sort by length descending to avoid partial replacements
    sorted_old_paths = sorted(rename_map.keys(), key=len, reverse=True)
    
    print("Updating references in .md and .json files...")
    for root, dirs, files in os.walk("."):
        if any(ignored in root for ignored in [".git", ".chunkhound", ".omc", ".omx", ".pytest_cache"]):
            continue
        for file in files:
            if file.endswith((".md", ".json")):
                file_path = os.path.join(root, file)
                if os.path.basename(file_path) in ["rename_manifest.csv", "mass_rename_manifests.py"]:
                    continue
                    
                try:
                    with open(file_path, "r", encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    continue
                
                new_content = content
                changed = False
                for old_path in sorted_old_paths:
                    new_path = rename_map[old_path]
                    # Check both forward and backward slashes if needed, 
                    # but usually these are relative paths in the repo
                    if old_path in new_content:
                        new_content = new_content.replace(old_path, new_path)
                        changed = True
                    
                    # Also check for variations (e.g. without leading 006_...)
                    # but the requirement says "points to the old verbose filenames"
                
                if changed:
                    with open(file_path, "w", encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated references in {file_path}")

    # 4. Perform Renaming
    print("Renaming files...")
    for old, new in rename_map.items():
        if os.path.exists(old):
            # Ensure target directory exists (should exist)
            os.makedirs(os.path.dirname(new), exist_ok=True)
            os.rename(old, new)
            # print(f"Renamed: {old} -> {new}")
    
    print("Renaming complete.")

if __name__ == "__main__":
    main()
