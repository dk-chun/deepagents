# Outing Guardian Skill

The Outing Guardian skill provides high-level logic for managing home safety and alleviating user anxiety when they leave the house.

## Core Capabilities
- **Status Verification**: Confirms if specific appliances (hair straighteners, AC, gas etc.) are safely turned off.
- **Remote Control**: Allows turning off devices if they were accidentally left on.
- **Anxiety Mitigation**: Provides reassuring and clear communication about the state of the home.

## Protocol
1. When a user expresses concern about a device (e.g., "Did I turn off the iron?"):
   - Identify the device from the user's utterance.
   - Use `check_device_status` to verify its current state.
   - Report the status clearly (e.g., "The hair straightener is currently OFF. You can relax!").
2. If the device is ON:
   - Ask the user if they want to turn it off, or proceed to turn it off if the intent is clear (e.g., "I'm worried I left it on, please check and turn it off").
   - Use `turn_off_device` if needed.
   - Confirm the operation.
