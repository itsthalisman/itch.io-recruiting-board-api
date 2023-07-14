import keyboard
import sys
import subprocess
from bs4 import BeautifulSoup
import requests
import time


def clscr(): # This function enables this script to clear the user's terminal according to the user's operating system. It first detects the user's OS and, depending on the OS, will throw the correct command to clear the user's terminal

    os_type = sys.platform

    if os_type == 'win32' or os_type == 'cygwin':
        subprocess.call('cls', shell=True)

    elif os_type == 'linux' or os_type == 'darwin' or os_type == 'aix':
        subprocess.call('clear', shell=True)


def itch_api():

    clscr() # Though this might seem redundant at first, the function "itch_api()" will restart everytime a new forum post is fetched so it can load the newest forum post and print it to the terminal
	
    url = 'https://itch.io/board/10020/help-wanted-or-offered' 

    response = requests.get(url)  # GET Requests to the URL
    soup = BeautifulSoup(response.content, "html.parser")  # The following lines are an instance and functions of the BeautifulSoup module that will search and fetch, from the HTML data scraped by the GET request, relevant information about the forum posts such as dates, texts, titles and urls from each post.
    script_title = soup.find_all('a', class_='topic_link')
    script_date = soup.find_all('span', class_='topic_date')
    content_list = []

    try:

        with open('itch_results.txt', 'r+', encoding='utf-8') as itch: # Upon first executing this script, a file containing all of the relevant info from all gathered forum posts will be written to this file. Every time that this script detects a new forum post, it will restart and rewrite all of the new forum posts gathered previously along with the newest forum post found.
            itch.truncate(0)
            itch.close()
    except:

        pass

    print("Disclaimer: some links from the posts may not be accessible |    Hold Q to stop running the script" + "\n" * 2)

    for i in range(0, len(script_title)): # This section here prints all of the info scraped and it also writes that info to the txt file

        last_title = script_title[i].get_text()
        last_date = script_date[i]['title']
        last_url = script_title[i]['href']
        content_list.append(last_title)

        print(last_title + " | " + str(last_date + "\n" + "https://itch.io" + str(last_url) + "\n"))

        with open('itch_results.txt', 'a+', encoding='utf-8') as itch:

            itch.write(last_title + "\n" + last_date + "\n" + "https://itch.io" + last_url + "\n" * 2)
            itch.close()

    while keyboard.is_pressed('q') is not True: # This section analyses if the latest forum post is the same as the latest forum post stored on the list "content_list". If the latest forum post doesn't match with what is stored in "content_list", this script will end this function and restart it. I have coded this while loop to allow the user to terminate this entire script by pressing "Q"

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        script_title = soup.find_all('a', class_='topic_link')

        for i in range(0, 1): # For loop for comparing "content_list" info to the latest request info

            last_title = script_title[i].get_text()

            if last_title not in content_list:

                return 0 # Stops the current function so it will be restarted leading to the new forum post to be printed in the terminal

        for i in range(0, 25): # For loop to prevent that the script will break by pressing "Q" while the "time.sleep()" method is activated and also guaranteeing that a new URL GET request will be made every 5 seconds if the button "Q" is not pressed by the user

            if keyboard.is_pressed('q') is not True:
                time.sleep(0.2)

            else:
                break

def main():

    while keyboard.is_pressed('q') is not True: # Necessary loop argument to insure the function "itch_api()" will not be executed again if the user presses "W" while itch_api()'s while loop is running

        try:

            itch_api() # Sometimes, the API might not be able to perform a get request due to lack of internet connection. Once this happens, unless managed with try/except statements, the API will keep mass requesting to the url's server which will lead to a Maximum Retries error and abruptly stop the script. This try/except statement prevents this from happening by making sure the "itch_api()" function will load once every 3 seconds if connection issues ever get in the way of the GET requests

        except:

           print("\n" + "A connection error occurred! Restarting...")
           time.sleep(3)

if __name__ == '__main__':
    main()
