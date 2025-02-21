"""
Module: state_extractor

This module provides functionality to extract all states for a given
trigger type in a Twilio flow definition. It includes recursive traversal
of the flow's state transitions, starting from the initial state, to
identify and map relevant states.

Key Functionality:
- Validates the structure of a Twilio flow definition.
- Extracts states associated with a specific trigger type.
- Traverses transitions between states recursively to ensure all
  connected states are captured.

Dependencies:
- `utils` module for utility functions such as retrieving the first state.

Example Usage:
    flow_definition = {...}  # JSON representation of a Twilio flow
    trigger_type = TriggerType.EVENT  # Example trigger type
    states = get_states_by_trigger_type(flow_definition, trigger_type)
"""

import json
import utils

def get_states_by_trigger_type(flow_definition, trigger_type):
    """
    Extracts all states for a given trigger type in a Twilio flow.

    Args:
        flow_definition (dict): The JSON representation of the Twilio flow.
        trigger_type (TriggerType): The trigger type to search for.

    Returns:
        dict: A dictionary mapping state names to their default friendly names.
    """
    all_states = {}

    # Validate the flow definition structure
    if 'states' not in flow_definition:
        print("Invalid flow definition: 'states' key not found.")
        return all_states

    # Get the initial state based on the trigger type
    initial_state = utils.get_first_state(flow_definition, trigger_type)
    if not initial_state:
        print(f"No states found for trigger type '{trigger_type.value}'.")
        return all_states

    # Create a mapping of state names to their definitions
    state_map = {state['name']: state for state in flow_definition['states']}

    def traverse_state(state_name):
        """
        Recursively traverse states starting from the given state name.

        Args:
            state_name (str): The name of the state to traverse from.
        """
        if state_name in all_states or state_name not in state_map:
            return

        # Add the current state to the results
        all_states[state_name] = state_name
        state = state_map[state_name]

        # Traverse all transitions leading to other states
        for transition in state.get('transitions', []):
            next_state = transition.get('next')
            if next_state:
                traverse_state(next_state)

    # Start traversal from the initial state
    traverse_state(initial_state)

    return all_states
