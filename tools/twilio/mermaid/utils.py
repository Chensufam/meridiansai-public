# Utilities for the tool
import json


def write_output_to_file(output, output_file):
    """
    Writes the output to a JSON file.

    Args:
        output (json object or list): A json object or list.
        output_file (str): The file path to save the output as JSON.
    """
    with open(output_file, 'w') as file:
        if isinstance(output, dict):
            json.dump(output, file, indent=4)
        else:
            file.writelines(f"{line}\n" for line in output)

    print(f"Output written to {output_file}.")

def get_first_state(flow_definition, trigger_type):
    """
    Get initial state for a trigger type all states for a given trigger type in a Twilio flow and
    saves them to a file.

    Args:
        flow_definition (dict): The JSON representation of the Twilio flow.
        trigger_type (TriggerType): The trigger type to search for.

    Returns:
        dict: the first state for the trigger.
    """
    # Find the trigger state
    trigger_state = {"transitions": {}}

    #  Find the trigger state
    for state in flow_definition['states']:
        if state['type'] == 'trigger':
            trigger_state = state
            break

    first_state = None

    # Loop through all states in the flow definition to locate the first
    for transition in trigger_state.get('transitions', []):
        event = transition.get('event')
        next_state = transition.get('next')
        if event == trigger_type.value:
            first_state = next_state
            break

    return first_state

def load_json_object(file_path):
    """
    Loads a JSON object from a file with error handling.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The JSON object loaded as a Python dictionary, or None if an error occurs.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)  # Parse the JSON file into a Python dictionary
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError as e:
        print(f"Error: The file '{file_path}' contains invalid JSON. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

