# IP Address Tracker

Author: [Jeret Christopher@M0du5](https://github.com/jeretc)

This is a Python script that allows you to trace the location of an IP address using the ipstack API.


## Prerequisites

- Python 3.x
- requests
- colorama
- tabulate
- folium


## Installation

1. Clone the repository:

```bash
git clone https://github.com/jeretc/ip-tracker.git

```

2. pip install -r requirements.txt


3. Obtain an API key from ipstack:

    Visit ipstack.com and sign up for an account.
    Once signed in, navigate to your account dashboard to find your API key.

Note: The script uses the ipstack API to retrieve location data. You need to replace the access_key variable in the code with your own API key.


## Usage

python ip-tracker.py


# Accuracy and Limitations

The accuracy of the location data provided by the ipstack API can vary. While it generally provides reliable results, there are a few factors to consider:

Geolocation Accuracy: The accuracy of geolocation data depends on various factors, including the IP address database and the quality of IP address assignments.
In some cases, the location information might be approximate or based on the registered owner of the IP address.
IP Address Types: The accuracy might differ between IPv4 and IPv6 addresses. IPv4 addresses are generally more accurately geolocated than IPv6 addresses.
VPN and Proxy Servers: If an IP address belongs to a VPN or proxy server, the location information might point to the server's location instead of the actual user's location.

Keep these limitations in mind when interpreting the results obtained from the script.


## License
This project is licensed under the [MIT License](LICENSE).




