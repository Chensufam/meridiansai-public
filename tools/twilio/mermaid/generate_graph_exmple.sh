#!/bin/bash

python3 tools/twilio/mermaid/index.py update_graph rest_api \
    <flow_sid> \
    --output_file "MD file with an idenifier to update"\
    --section_identifier "my-section" \
    --flow_state_file "flow_states_example.json"
