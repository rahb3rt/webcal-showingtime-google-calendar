# Showing Time Calendar Sync

## Prerequisits

- cedentials.json - Must be generated on Google Cloud Console
- Set URI and Redirect `URI: http://localhost:8080 and http://localhost:8080/`
- SET EMAIL to your Google Calendar
- Set CAL to your ShowingTime Calendar URL 

This script performs various operations related to the Google Calendar and ICS file format. Below is a step-by-step breakdown of what the script does:

1. **Import necessary modules:**
    - : For operating system interactions
    - : To serialize and deserialize Python object structures
    - : To handle the OAuth flow
    - : To send requests during the OAuth process
    - : To make HTTP requests
    - : To work with ICS (iCalendar) files

2. **Set constants and URLs:**
    - : A list containing the required Google Calendar API scopes.
    - : The Google Calendar API endpoint for events.
    - : The external calendar URL to fetch.

3. **Fetch ICS file:**
    - Make a GET request to fetch the ICS file from the provided calendar URL.
    - Write the ICS content to .

4. **Load credentials and authenticate with Google:**
    - Check if a saved token exists.
    - If credentials are expired, refresh them.
    - If no credentials exist or they are invalid, perform OAuth flow to get them.
    - Save the credentials as .

5. **Convert ICS to JSON:**
    - Parse the ICS file using the  module.
    - Extract event details and format them in a JSON-friendly way.

6. **Fetch events from Google Calendar:**
    - Make a GET request to fetch events from the Google Calendar within the range of the imported events.

7. **Check for duplicates and add unique events:**
    - For each event in the converted list, check against the fetched Google Calendar events.
    - If the event doesn't exist in Google Calendar, POST it.

## Code:

```python

```

