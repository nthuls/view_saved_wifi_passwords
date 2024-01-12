import subprocess
import re

def get_wifi_profiles():
    profiles = []
    try:
        # Command to list WiFi profiles
        output = subprocess.check_output('netsh wlan show profiles', shell=True, text=True)
        # Regex to extract profile names
        profiles = re.findall(r'All User Profile\s*:\s*(.*)', output)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    return profiles

def get_wifi_passwords(profiles):
    wifi_data = {}
    for profile in profiles:
        try:
            # Command to get WiFi password
            output = subprocess.check_output(f'netsh wlan show profile name="{profile}" key=clear', shell=True, text=True)
            # Regex to extract password
            password = re.search(r'Key Content\s*:\s*(.*)', output)
            if password:
                wifi_data[profile] = password.group(1)
            else:
                wifi_data[profile] = None
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
    return wifi_data

def main():
    profiles = get_wifi_profiles()
    wifi_data = get_wifi_passwords(profiles)
    
    # Write data to a file
    with open('wifi_passwords.txt', 'w') as file:
        for profile, password in wifi_data.items():
            file.write(f'Profile: {profile}, Password: {password}\n')
    print("Wi-Fi profiles and passwords have been saved to wifi_passwords.txt")
    
    # Print data to the command line
    for profile, password in wifi_data.items():
        print(f'Profile: {profile}, Password: {password}')

if __name__ == "__main__":
    main()
