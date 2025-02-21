#!/bin/bash

python3 srcs/index.py generate_states_file incoming_message \
    <flow_sid> \
    --flow_state_file "flow_states_example.json"
