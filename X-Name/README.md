# The Elite Greeting Service

A beginner-level web challenge focused on Server-Side Template Injection via HTTP headers.

## Scenario

A sophisticated web service offers personalized greetings. However, the personalization logic is flawed. Find the flag hidden on the server!

## How to Run

Make sure you have Docker and Docker Compose installed.

1.  Open a terminal in this directory.
2.  Run the command:
    ```sh
    docker-compose up --build
    ```
3.  The challenge is now accessible at: `http://localhost:8000`

## Objective

Find the flag stored in an environment variable on the server.

## Solution 

The vulnerability is a Server-Side Template Injection (SSTI) in the `X-Name` HTTP header. The player needs to use a tool like `curl` or Burp Suite to send requests with this custom header.

**Step 1: Verify the vulnerability**
Send a simple mathematical operation.

```sh
curl http://localhost:8000 -H "X-Name: {{ 7*7 }}"