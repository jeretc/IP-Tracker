import requests
import json
from colorama import init, Fore, Style
from tabulate import tabulate
import re
import folium
import webbrowser
import os
import logging
import argparse
import sqlite3
import termios
import sys
import tty


# Function to get a single character from user input
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch



# Set up logging
logging.basicConfig(filename='ip_tracker.log', level=logging.INFO)

# Initialize colorama
init(autoreset=True)

# Initialize the database connection
conn = sqlite3.connect('ip_tracker.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS search_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

def get_location(ip):
    access_key = ''  # Replace with your ipstack API key
    url = f'http://api.ipstack.com/{ip}?access_key={access_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred during API request: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding API response: {str(e)}")
        return None

def print_banner():
    print()
    print("\033[1;34m====================================")
    print("\033[1;34m        IP Address Tracker")
    print("\033[1;34m====================================")
    print("\033[0m")



def get_valid_ip():
    while True:
        ip_address = input("Enter an IP address to trace: ")
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip_address):
            return ip_address
        else:
            print("Invalid IP address. Please try again.")

def create_map(latitude, longitude):
    # Create a map centered at the IP address location
    map_ip = folium.Map(location=[latitude, longitude], zoom_start=10)

    # Add a marker for the IP address location
    folium.Marker([latitude, longitude], popup="IP Address Location").add_to(map_ip)

    # Save the map to a file
    map_ip.save("map.html")

def display_location_data(location_data):
    # Format location data as a table with orange values
    table_data = [
        [Fore.GREEN + "IP", Fore.YELLOW + location_data.get("ip", "")],
        [Fore.GREEN + "Type", Fore.YELLOW + location_data.get("type", "")],
        [Fore.GREEN + "Continent", Fore.YELLOW + location_data.get("continent_name", "")],
        [Fore.GREEN + "Country", Fore.YELLOW + location_data.get("country_name", "")],
        [Fore.GREEN + "Region", Fore.YELLOW + location_data.get("region_name", "")],
        [Fore.GREEN + "City", Fore.YELLOW + location_data.get("city", "")],
        [Fore.GREEN + "ZIP Code", Fore.YELLOW + location_data.get("zip", "")],
        [Fore.GREEN + "Latitude", Fore.YELLOW + str(location_data.get("latitude", ""))],
        [Fore.GREEN + "Longitude", Fore.YELLOW + str(location_data.get("longitude", ""))]
    ]

    # Print the formatted table
    print(Fore.GREEN + "Location Data:")
    print(tabulate(table_data, tablefmt="fancy_grid"))
    print(Style.RESET_ALL)

    # Retrieve latitude and longitude coordinates
    latitude = location_data.get("latitude")
    longitude = location_data.get("longitude")

    # Create a geolocation visualization
    create_map(latitude, longitude)
    
    # Print the clickable link to map.html
    link = f"{Fore.BLUE}map.html{Style.RESET_ALL}"
    print(f"Geolocation visualization saved to {link}")

    # Open the HTML file in a browser upon user interaction
    print("Press Enter to open the map in your default browser, or any key to continue: \n")
    choice = getch()  # Get a single character without displaying it
    if choice == '\r':  # Check if the input is Enter key
        webbrowser.open(f"file:///{os.path.abspath('map.html')}")

    # Log the IP address search
    cursor.execute("INSERT INTO search_history (ip_address) VALUES (?)", (location_data.get("ip", ""),))
    conn.commit()

def print_menu():
    print("Select an option:\n")
    print("1. Trace a new IP address")
    print("2. View search history")
    print("3. Clear search history")
    print("4. Exit\n")

def view_search_history():
    cursor.execute("SELECT * FROM search_history ORDER BY timestamp DESC")
    history = cursor.fetchall()

    if history:
        print("\nSearch History:\n")
        for row in history:
            print(f"{Fore.YELLOW}{row[0]} - {row[1]} - {row[2]}{Style.RESET_ALL}")
        print()    
    else:
        print("No search history available.")


def clear_search_history():
    confirm = input("Are you sure you want to clear the search history? (y/n): ")
    if confirm.lower() == "y":
        cursor.execute("DELETE FROM search_history")
        conn.commit()
        print("Search history cleared.")
    else:
        print("Search history was not cleared.")

        

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="IP Address Tracker")
    parser.add_argument("--history", action="store_true", help="View search history")
    args = parser.parse_args()

    # Print the banner
    print_banner()

    if args.history:
        view_search_history()
    else:
        while True:
            print_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                # Get a valid IP address from the user
                ip_address = get_valid_ip()

                # Get the location data
                location_data = get_location(ip_address)

                # Check if location data is available
                if location_data is not None:
                    display_location_data(location_data)
            elif choice == "2":
                view_search_history()
            elif choice == "3":
                clear_search_history()   
            elif choice == "4":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()

