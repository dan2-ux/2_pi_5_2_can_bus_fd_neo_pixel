import asyncio                      # Import asyncio for asynchronous programming
import can                         # Import python-can for CAN bus communication
import math                        # Import math library for math functions

# Initialize CAN bus
can_bus = can.interface.Bus(channel='can0', interface='socketcan')  # Create CAN bus interface on 'can0' with socketcan driver

# Variables to store the last known state
intent_state = 0.0                 # Store last known intensity value
color_state = "#FFFFFF"            # Default color (white)

def parse_color(color_str: str):
    """Convert a hex color string like '#FFAABB' to (r, g, b)."""
    color_str = color_str.lstrip('#')  # Remove '#' if present
    if len(color_str) == 8:             # If color includes alpha channel (e.g. '#AARRGGBB')
        color_str = color_str[2:]       # Ignore alpha by taking last 6 chars (RRGGBB)
    elif len(color_str) != 6:
        return (0, 0, 0)                # Return black if invalid format
    r = int(color_str[0:2], 16)         # Parse red component
    g = int(color_str[2:4], 16)         # Parse green component
    b = int(color_str[4:6], 16)         # Parse blue component
    return (r, g, b)                    # Return RGB tuple

async def send_can_message(is_light_on: bool, intent_value: float, color_str: str):
    """Send a CAN message with the light state (ON/OFF), intensity, and color."""
    led_state = 0x01 if is_light_on else 0x00   # Convert light state to 0x01 (on) or 0x00 (off)
    intent_scaled = math.ceil(intent_value / 10)  # Scale intensity (0-100) down to 0-10 and ceil

    r, g, b = parse_color(color_str)             # Parse hex color string to RGB values

    # CAN data: [led_state, red, green, blue, 0, 0, 0, intent_scaled]
    data = [led_state, r, g, b, 255]

    msg = can.Message(arbitration_id=0x123, data=data, is_extended_id=False)  # Create CAN message with ID 0x123
    try:
        can_bus.send(msg)                         # Send CAN message on the bus        
        print(f"CAN message sent → Light: {'ON' if is_light_on else 'OFF'} | Intensity: {intent_scaled * 10}% | Color: {color_str}")
    except can.CanError as e:                                                                                                         
        print(f"Failed to send CAN message: {e}")  # Print error on failure                     
                                                                                                 
async def monitor_ambient_light():                                                                              
    """Toggle the light ON/OFF in a continuous loop."""                                
    is_light_on = False  # Initially, start with light off                         
    while True:                                                                                                                       
        # Toggle light state between ON and OFF                                                 
        is_light_on = not is_light_on                                                            
        await send_can_message(is_light_on, intent_state, color_state)  # Send the updated CAN message          
                                                                                                      
        await asyncio.sleep(1)  # Sleep for 1 second before toggling again         
                                                                                                                                      
def main():                                                                                     
    loop = asyncio.get_event_loop()                                                              
    try:                                                                                                        
        loop.run_until_complete(monitor_ambient_light())  # Start sending ON/OFF signals              
    except KeyboardInterrupt:                                                           
        print("Monitoring stopped by user.")                                                                                          
    finally:                                                         
        loop.close()                                                       
                                                                                                                
if __name__ == "__main__":                                                                                      
    main()    
