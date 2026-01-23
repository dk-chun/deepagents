from langchain_core.tools import tool
from data.devices import HOME_DEVICES
import json

@tool
def check_device_status(device_name: str) -> str:
    """
    Checks the status of a specific device by its name.
    
    Args:
        device_name: The name of the device to check (e.g., "고데기", "에어컨").
        
    Returns:
        A JSON string containing the device ID, current status, and location.
        Returns a "Not Found" message if the device doesn't exist.
    """
    print(f"[DEBUG] Checking status for: {device_name}")
    
    # Simple keyword matching
    for device_id, info in HOME_DEVICES.items():
        if any(name in device_name or device_name in name for name in info["name"]):
            result = {
                "id": info["id"],
                "status": info["status"],
                "location": info["location"],
                "name_matched": info["name"][0]
            }
            return json.dumps(result, ensure_ascii=False)
            
    return json.dumps({"error": "Device not found", "query": device_name})

@tool
def turn_off_device(device_id: str) -> str:
    """
    Turns off a specific device using its ID.
    
    Args:
        device_id: The unique ID of the device to turn off (e.g., "smart_plug_dressing_room").
        
    Returns:
        A success message indicating the new status, or an error if not found.
    """
    print(f"[DEBUG] Turning OFF device: {device_id}")
    
    # Find device by ID
    target_device = None
    for _, info in HOME_DEVICES.items():
        if info["id"] == device_id:
            target_device = info
            break
            
    if target_device:
        previous_status = target_device["status"]
        target_device["status"] = "OFF"
        return f"Successfully turned off {target_device['name'][0]}. (Status: {previous_status} -> OFF)"
    else:
        return f"Error: Device with ID '{device_id}' not found."
