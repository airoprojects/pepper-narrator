from naoqi import ALProxy

# Define the NAOqi broker IP and port
NAOQI_IP = "localhost"  # or the IP address of your Docker container
NAOQI_PORT = 9559       # or the port you've mapped

def get_variable_value(variable_name):
    try:
        # Create a proxy to the ALMemory service
        memory_proxy = ALProxy("ALMemory", NAOQI_IP, NAOQI_PORT)
        
        # Get the value of the variable
        value = memory_proxy.getData(variable_name)
        return value
    except Exception as e:
        print(f"Error while retrieving variable: {e}")
        return None

if __name__ == "__main__":
    variable_name = "YourVariableName"  # Replace with your actual variable name
    value = get_variable_value(variable_name)
    if value is not None:
        print(f"The value of '{variable_name}' is {value}")
    else:
        print(f"Failed to retrieve the value of '{variable_name}'")
