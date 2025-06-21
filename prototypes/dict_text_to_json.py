import re
import json
import sys

def parse_entry(entry):
    # Split entry into lines
    lines = entry.strip().split('\n')
    
    # Parse first line: "word [part_of_speech]"
    word_line = lines[0]
    
    # Simpler regex: match everything up to [part_of_speech]
    word_match = re.match(r'^(.*?)\s+\[([\w\s]+)\]', word_line)
    if not word_match:
        raise ValueError(f"Could not parse word line: {word_line}")
    
    word = word_match.group(1).strip()
    part_of_speech = word_match.group(2)
    
    # Parse second line: "(example) [source]"
    example_line = lines[1]
    example_match = re.match(r'\((.*?)\)(?:\s+\[(.*?)\])?', example_line)
    example = example_match.group(1) if example_match else ""
    source = example_match.group(2) if example_match and example_match.group(2) else ""
    
    # Parse translations (remaining lines)
    translations = []
    for line in lines[2:]:
        if match := re.match(r'\d+\.\s+(.*)', line):
            translations.append(match.group(1))
    
    return {
        "word": word,
        "part_of_speech": part_of_speech,
        "example": example,
        "source": source,
        "translations": translations
    }


def dict_text_to_json(source_file_path: str, output_file_path: str):
    # Read and parse the file
    entries = []
    with open(source_file_path, 'r') as file:
        content = file.read()
        # Split on double newlines to separate entries
        raw_entries = [e.strip() for e in content.split('\n\n') if e.strip()]
        # print(raw_entries[1])
        for entry in raw_entries:
            parsed = parse_entry(entry)
            entries.append(parsed)

    # Save to JSON file
    with open(output_file_path, 'w') as f:
        json.dump(entries, f, indent=2)

    # Example output for the given entry
    print(json.dumps(entries[0], indent=2))


if __name__ == '__main__':
    source = sys.argv[1] if len(sys.argv) > 1 else 'vocabulary/dicts/english.txt'
    output = sys.argv[2] if len(sys.argv) > 2 else 'english_dictionary.json'

    dict_text_to_json(source, output)
