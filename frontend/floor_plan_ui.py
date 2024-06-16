import requests
from tabulate import tabulate
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama for automatic reset

def beautify_floor_plans(floor_plans):
    formatted_floor_plans = []

    for floor in floor_plans:
        formatted_floor_plan = [f"{Fore.CYAN}Floor {floor['floorNumber']}{Style.RESET_ALL}"]
        formatted_rooms = []
        for room in floor['rooms']:
            capacity_color = get_capacity_color(room['capacity'])
            formatted_rooms.append(f"{capacity_color}| {room['name']} (Capacity: {room['capacity']}){Style.RESET_ALL} ")
        formatted_floor_plan.extend(formatted_rooms)
        formatted_floor_plans.append(formatted_floor_plan)

    return tabulate(formatted_floor_plans, tablefmt='fancy_grid')

def get_capacity_color(capacity):
    if capacity > 20:
        return Fore.RED     # High capacity, use red color
    elif capacity > 10:
        return Fore.YELLOW  # Medium capacity, use yellow color
    else:
        return Fore.GREEN   # Low capacity, use green color

def colorful_input(prompt):
    return input(f"{Fore.BLUE}{Style.BRIGHT}{prompt}{Style.RESET_ALL}")

def colorful_input_red(prompt):
    return input(f"{Fore.RED}{Style.BRIGHT}{prompt}{Style.RESET_ALL}")

def colorful_input_green(prompt):
    return input(f"{Fore.GREEN}{Style.BRIGHT}{prompt}{Style.RESET_ALL}")

def display_welcome_message():
    """Display a stylish welcome message."""
    welcome_message = """
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                   ___                                ║
║                         |  |  _ |  _  _   _   _    |   _                             ║
║                         |/\| (- | (_ (_) ||| (-    |  (_)                            ║
║                                                                                      ║
║     __                                                         __                    ║
║    |_  |  _   _   _   |\/|  _   _   _   _   _  _   _  _  |_   (_      _ |_  _  _     ║
║    |   | (_) (_) |    |  | (_| | ) (_| (_) (- ||| (- | ) |_   __) \/ _) |_ (- |||    ║
║                                        _/                         /                  ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
"""
    print(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}{welcome_message}{Style.RESET_ALL}\n")

def main():
    api_url = "http://localhost:9070/api/floor-plan"
    
    display_welcome_message()
    while True:
        # Get the username from the user
        username = colorful_input_red("Enter username: ")

        # Get the version
        version = colorful_input_red("Enter the version: ")

        # Ask for the operation
        operation = colorful_input("""Operations Available: 
    Select 1 for GET
    Select 2 for POST
    Select 0 to exit
    Enter operation number: """)

        if operation == '0':
            print("Exiting the program.")
            break

        if operation == '1':
            # Perform a GET request
            get_url = f"{api_url}?username={username}&version={version}"
            response = requests.get(get_url)
            if response.status_code == 200:
                try:
                    floor_plans = response.json()
                    print("Floor Plans:")
                    print(beautify_floor_plans(floor_plans))
                except requests.exceptions.JSONDecodeError:
                    print("The Input(Username/Version is invalid)")
            else:
                print(f"GET request failed with status code {response.status_code}")

        elif operation == '2':
            # Perform a POST request
            if(username != 'admin'):
                print("Only admin can update the floor plan")
                continue
            # Get the number of floors
            num_floors = int(colorful_input("Enter the number of floors: "))

            updated_floor_plans = []
            for i in range(1, num_floors + 1):
                # Get the number of rooms for each floor
                num_rooms = int(colorful_input(f"""    ╔═══════════════════════════════════════════════╗
    ║   Enter the number of rooms for Floor {i}:      ║
    ╚═══════════════════════════════════════════════╝
                           """))

                rooms = []
                for j in range(1, num_rooms + 1):
                    room_name = colorful_input(f"        Enter the name for Room {j} on Floor {i}: ")
                    room_capacity = int(colorful_input(f"""        ║
        ╚══ Enter the capacity for Room {j} on Floor {i}: """))
                    rooms.append({"name": room_name, "capacity": room_capacity})

                updated_floor_plans.append({"floorNumber": i, "rooms": rooms})

            payload = {"username": username, "version": version, "floorDTOs": updated_floor_plans}

            
            response = requests.post(api_url+'/update', json=payload)

            if response.status_code == 200:
                print("Floor plan updated successfully")
            else:
                print(f"PUT request failed with status code {response.status_code}")

        else:
            print("Invalid operation selected")

if __name__ == "__main__":
    main()