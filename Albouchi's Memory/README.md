# CTF Write-up: Albouchi's Memory

**Category:** Web / WebSockets  
**Difficulty:** Easy  
**Description:** Can you help Albouchi to find his memory back ??

## Challenge Overview

The challenge presents a web interface titled "Albouchi's Secret" where users interact with a character named Albouchi [cite: web/index.html]. The goal is to answer a series of personal questions correctly to help him "remember" his secret code.

The application is built using:
- **Frontend:** HTML/JS with Tailwind CSS [cite: web/index.html].
- **Backend:** Python websockets server running on port 8765 [cite: app/Dockerfile, app/server.py].
- **Infrastructure:** Docker Compose with Nginx serving static files [cite: docker-compose.yml].

## Vulnerability Analysis

The challenge can be solved by inspecting the WebSocket traffic. The backend server (`server.py`) contains a logic flaw where it sends sensitive debug information to the client immediately upon connection.

### The Leak

In `server.py`, the handler function calls `send_all_answers_debug(websocket)` right after a client connects:

```python
# app/server.py

async def handler(websocket, path):
    # ...
    # Send one big debug with all answers at the start
    await send_all_answers_debug(websocket)
```
[cite: app/server.py]

This function sends a JSON object containing every correct answer to the client:

```python
async def send_all_answers_debug(websocket):
    """Send a single big debug frame with all answers (handy for Burp to show everything at connect)."""
    all_answers = {i: q["answers"] for i, q in enumerate(QUESTIONS)}
    payload = {
        "type": "debug",
        "note": "All answers for this instance ",
        "all_answers": all_answers
    }
    await websocket.send(json.dumps(payload))
```
[cite: app/server.py]

## Solution Steps

### 1. Intercept Network Traffic
1. Open the challenge URL in your browser.
2. Open Developer Tools (F12 or Right-Click -> Inspect).
3. Navigate to the **Network** tab.
4. Filter by **WS** (WebSockets).
5. Refresh the page to capture the handshake.

### 2. Retrieve the Answers
Click on the WebSocket connection (usually `localhost` or the server IP) and view the **Messages** or **Response** tab. The first message received from the server will be the debug payload:

```json
{
    "type": "debug", 
    "note": "All answers for this instance ", 
    "all_answers": {
        "0": ["Mcha7em"], 
        "1": ["Beekeeping"], 
        "2": ["under the bed"], 
        "3": ["nahi dokhan mech behilk"], 
        "4": ["asf"]
    }
}
```
[cite: app/server.py]

### 3. Submit Answers
Using the leaked data, answer the questions in the web interface:

- **Q:** What's my favorite food?
  - **A:** `Mcha7em`
- **Q:** What is the hobby that my father passed on to me?
  - **A:** `Beekeeping`
- **Q:** And where did i hide from my freind amri?
  - **A:** `under the bed`
- **Q:** I have one only advice that always i say it. What is it?
  - **A:** `nahi dokhan mech behilk`
- **Q:** do you know how much is that task is easy ?
  - **A:** `asf`

### 4. Flag Capture
After submitting the final answer, the server returns the flag:

**Flag:** `Securinets{7lili_na_throntha_denia_kleha_lme!}`
[cite: app/server.py]
