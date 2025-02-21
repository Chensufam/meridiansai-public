# twilio mermaid generation tool

## Motivation

We develop this tool to handle the following missing features in Twilio:

* There is no way to specify a friendly name for a widget.
* The transition is a little hard to read and navigate when the flow is becoming too complex.
* Update the graph automatically as part of another md doc.

## Requirements

```
pip install twilio

export TWILIO_ACCOUNT_SID="your sid"
export TWILIO_AUTH_TOKEN="your auth token"

```
## Concepts and How to run it

```
usage: index.py [-h] [--output_file OUTPUT_FILE]        [--section_identifier SECTION_IDENTIFIER]
                [--flow_state_file FLOW_STATE_FILE]
                cmd
                {TriggerType.INCOMING_MESSAGE,TriggerType.INCOMING_CALL,TriggerType.REST_API,TriggerType.SUBFLOW}
                flow_sid
```

1. Generate a json object for all the states for a trigger type in the flow
   -  trigger type are
        - INCOMING_MESSAGE
        - INCOMING_CALL
        - REST_API
        - SUBFLOW
   - See [Generate States Example](generate_states_example.sh)

1. Update the output file to have a friendly name for each state
   - See [flow_states_example.json](flow_states_example.json)

1. Generate mermaid graph and embed into a github md file [Example](section_sample.md)
   - The section_identifier convention
        - ` <!-- my-section-start -->`
        - ` <!-- my-section-end -->`
   -   - See [Update graph Example](generate_graph_example.sh)


## Future Improvements

* Include subflow in the main flow. Right now, we use a separate mermaid graph chart
* Use color to diffentiate success, failure and others
* Add icon support to appropriate widget type
