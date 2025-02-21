"""
This module generates a Mermaid flowchart graph from a flow definition of states
and transitions.
"""
import json


def generate_mermaid_graph(initial_state, flow_definition, states_file):
    """
    Generates a Mermaid graph representing a flowchart of states and transitions.

    Args:
        initial_state (str): The starting state for the flow.
        flow_definition (dict): A dictionary containing the flow definition.
        states_file (str or None): The path to a JSON file containing friendly state names (optional).

    Returns:
        list: A list of strings that represents the Mermaid graph syntax.
    """
    # Load friendly state names from the states file if provided
    friendly_states = {}
    if states_file:
        with open(states_file, 'r') as f:
            friendly_states = json.load(f)

    # Initialize the Mermaid graph
    graph_parts = ['```mermaid', 'flowchart TD']
    visited_states = set()

    # Create a mapping of state names to state definitions
    state_map = {state['name']: state for state in flow_definition['states']}
    link_index = [-1]

    def traverse_state(state_name):
        """
        Recursively traverses the states and builds the Mermaid graph.

        Args:
            state_name (str): The name of the state to traverse from.
        """
        # Skip if the state has already been visited or doesn't exist in the flow definition
        if state_name in visited_states or state_name not in state_map:
            return

        visited_states.add(state_name)
        state = state_map[state_name]

        # Determine the friendly name for the state
        friendly_name = friendly_states.get(state_name, state_name)

        # Add node for the current state based on its type
        if state.get('type') == 'split-based-on':
            graph_parts.append(f'    {state_name}{{{friendly_name}}}')
        else:
            graph_parts.append(f'    {state_name}({friendly_name})')

        # Traverse transitions from the current state
        for transition in state.get('transitions', []):
            next_state = transition.get('next')
            if next_state:
                link_index[0] += 1
                # Add condition if available, otherwise use the event value
                conditions = transition.get("conditions")
                if conditions:
                    condition = conditions[0].get("friendly_name")
                    graph_parts.append(f'    {state_name} --> |{condition}| {next_state}')
                else:
                    event = transition.get('event')
                    if event != 'next':
                        graph_parts.append(f'    {state_name} --> |{event}| {next_state}')
                    else:
                        graph_parts.append(f'    {state_name} --> {next_state}')

                    # Style failed links with a red color
                    if event in ["failed", "timeout"]:
                        graph_parts.append(f'    linkStyle {link_index[0]} stroke:red')

                # Recursively traverse the next state
                traverse_state(next_state)

    # Start traversing from the initial state
    traverse_state(initial_state)
    graph_parts.append('```')

    return graph_parts
