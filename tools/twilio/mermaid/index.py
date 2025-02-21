"""
A command-line tool for interacting with Twilio Studio Flows.
It allows the user to perform the following actions:

1. Generate a states file based on a specific trigger type of a flow.
2. Update a mermaid graph for a flow based on the flow's states.

The tool supports the following commands:
- `generate_states_file`: Generates a states file for a given Twilio Flow and trigger type.
- `update_graph`: Generates a mermaid graph based on the flow's state and updates the provided output file.

Required arguments:
- `cmd`: The command to execute (either "generate_states_file" or "update_graph").
- `trigger_type`: The trigger type of the flow.
- `flow_sid`: The SID (identifier) of the Twilio Flow.

Optional arguments:
- `--output_file`: The path to the output mermaid graph file (used only for the update_graph command).
- `--section_identifier`: The section identifier for the mermaid graph (used only for the update_graph command).
- `--flow_state_file`: The path to the state file name

Ensure that the necessary environment variables (`TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`) are set for authenticating with Twilio.

Example usage:
1. To generate a states file:
   python script_name.py generate_states_file <trigger_type> <flow_sid> --flow_state_file <file_path>

2. To update a mermaid graph:
   python script_name.py update_graph <trigger_type> <flow_sid> --output_file <file_path> --section_identifier <section_id> -- flow_state_file <file_path>
"""
import argparse
import json
import os
from enum import Enum

import mermaid
import output_states
import trigger_type
import update_doc
import utils
from twilio.rest import Client

# Load Twilio credentials from environment variables for security
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')


def load_twilio_flow(sid):
    """
    Fetch and display details of a Twilio Flow using the provided SID.

    Args:
        sid (str): The SID of the Twilio Flow.

    Returns:
        dict: The definition of the Twilio Flow if found.

    Raises:
        Exception: If there is an error fetching the flow from Twilio.
    """
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        # Fetch the Twilio Flow using the Flow SID
        flow = client.studio.v2.flows(sid).fetch()

        # Print Flow details
        print(f"Flow SID: {flow.sid}")
        print(f"Flow Friendly Name: {flow.friendly_name}")
        print(f"Flow Status: {flow.status}")
        print(f"Flow Date Created: {flow.date_created}")

        return flow.definition

    except Exception as e:
        print(f"Error loading flow: {e}")


class Command(Enum):
    """
    Enum to define valid commands for the tool.

    Attributes:
        GENERATE_STATES_FILE (str): Command to generate a states file.
        UPDATE_GRAPH (str): Command to update the graph.
    """
    GENERATE_STATES_FILE = "generate_states_file"
    UPDATE_GRAPH = "update_graph"


def str_to_trigger_type(s):
    """
    Convert string to TriggerType enum.

    Args:
        s (str): The string to convert to TriggerType.

    Returns:
        TriggerType: The corresponding TriggerType enum value.

    Raises:
        argparse.ArgumentTypeError: If the string doesn't match any TriggerType.
    """
    try:
        return trigger_type.TriggerType[s.upper()]
    except KeyError:
        raise argparse.ArgumentTypeError(
            f"Invalid value: '{s}' is not a valid trigger type."
        )


def str_to_command(s):
    """
    Convert string to Command enum.

    Args:
        s (str): The string to convert to Command.

    Returns:
        Command: The corresponding Command enum value.

    Raises:
        argparse.ArgumentTypeError: If the string doesn't match any Command.
    """
    try:
        return Command[s.upper()]
    except KeyError:
        raise argparse.ArgumentTypeError(
            f"Invalid command: '{s}' is not a valid command."
        )


def main():
    """
    Main function for the command-line tool that processes the input arguments
    and executes the corresponding command (generate states file or update graph).

    Raises:
        Exception: If required arguments are missing or invalid for the specified command.
    """
    parser = argparse.ArgumentParser(description="Twilio Tool command lines.")

    # Command argument
    parser.add_argument(
        "cmd", type=str_to_command,
        choices=list(Command),
        help="The command to execute (generate_states_file or update_graph)."
    )

    # Required arguments
    parser.add_argument(
        "trigger_type", type=str_to_trigger_type,
        choices=list(trigger_type.TriggerType),
        help="The trigger type of the flow."
    )

    parser.add_argument(
        "flow_sid", type=str,
        help="The SID of the flow."
    )

    # Optional arguments
    parser.add_argument(
        "--output_file", type=str, default="",
        help="The path to the file to output mermaid graph."
    )
    parser.add_argument(
        "--section_identifier", type=str, default="",
        help="The section identifier for the mermaid graph."
    )
    parser.add_argument(
        "--flow_state_file", type=str, default="",
        help="The path to the state file name."
    )

    # Parse command-line arguments
    args = parser.parse_args()

    # Load the flow definition using the SID
    flow_definition = load_twilio_flow(args.flow_sid)

    if args.cmd == Command.GENERATE_STATES_FILE:
        if not args.flow_state_file:
            raise Exception(f"flow_state_file needs to be specified for generate_states_file cmd")

        # Generate states based on the trigger type
        states = output_states.get_states_by_trigger_type(
            flow_definition, args.trigger_type)
        utils.write_output_to_file(states, args.flow_state_file)

    elif args.cmd == Command.UPDATE_GRAPH:
        if not args.section_identifier or not args.output_file:
            raise Exception("section_identifier and output_file cannot be empty for update_graph cmd")

        # Get the first state and generate mermaid graph
        first_state = utils.get_first_state(flow_definition, args.trigger_type)
        mermaid_graph = mermaid.generate_mermaid_graph(
            first_state, flow_definition, args.flow_state_file)

        mermaid_graph = '\n'.join(mermaid_graph)
        print(mermaid_graph)

        # Update the mermaid graph in the specified output file
        update_doc.update_mermaid_graph(
            args.output_file, mermaid_graph, args.section_identifier)


if __name__ == "__main__":
    main()
