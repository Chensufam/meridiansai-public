"""
Module: mermaid_graph_updater

This module provides functionality to update specific sections of a file
containing Mermaid.js diagrams. It locates and replaces a designated
Mermaid graph section identified by custom tags and writes the updated
content back to the file.

Key Functionality:
- Reads a file's content and identifies a Mermaid graph section using
  start and end tags.
- Replaces the identified section with a new Mermaid graph.
- Handles errors gracefully, such as missing files.

Dependencies:
- Regular expressions (re) for pattern matching and section replacement.

Example Usage:
    filename = "example.md"
    new_graph = "graph TD\nA-->B"
    section_identifier = "mermaid"
    update_mermaid_graph(filename, new_graph, section_identifier)
"""

import re

def update_mermaid_graph(filename, new_graph, section_identifier):
    """
    Loads a file, replaces a specific mermaid graph section,
    and writes the updated content back.

    Args:
        filename (str): The name of the file to be modified.
        new_graph (str): The new mermaid graph to insert into the section.
        section_identifier (str): A custom identifier for locating the section to be replaced.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    try:
        # Read the file's content
        with open(filename, 'r') as f:
            content = f.read()

        # Define the start and end tags for the section
        mermaid_start_tag = f"<!-- {section_identifier}-start -->"
        mermaid_end_tag = f"<!-- {section_identifier}-end -->"

        # Build the regex pattern dynamically using the tags
        regex_pattern = fr"{re.escape(mermaid_start_tag)}\s*(.*?)\s*{re.escape(mermaid_end_tag)}"

        # Replace the old Mermaid graph section with the new graph
        updated_content = re.sub(
            regex_pattern,
            f"{mermaid_start_tag}\n{new_graph}\n{mermaid_end_tag}",
            content,
            flags=re.DOTALL
        )

        # Write the updated content back to the file
        with open(filename, 'w') as f:
            f.write(updated_content)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
