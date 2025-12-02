# save as ctf_ws_server.py
import asyncio
import websockets
import json
import os

FLAG = os.environ.get("FLAG", "Securinets{7lili_na_throntha_denia_kleha_lme!}")

QUESTIONS = [
    {
        "question": "Ahla bik! To help me, first tell me: What's my favorite food ?",
        "answers": ["Mcha7em"]
    },
    {
        "question": "Excellent! Now, what is the hobby that my father passed on to me?",
        "answers": ["Beekeeping"]
    },
    {
        "question": "S7i7! And where did i hide from my freind amri?",
        "answers": ["under the bed"]
    },
    {
        "question": "Almost there! I have one only advice that always i say it. What is it?",
        "answers": ["nahi dokhan mech behilk"]
    },
    {
        "question": "Perfect! Last question: do you know how much is that task is easy ?",
        "answers": ["asf"]
    }
]

CLIENT_STATE = {}

async def send_question(websocket):
    client_id = id(websocket)
    question_index = CLIENT_STATE.get(client_id, 0)
    if question_index < len(QUESTIONS):
        q = QUESTIONS[question_index]
        payload = {
            "type": "question",
            "text": q["question"],
            "progress": [question_index + 1, len(QUESTIONS)]
        }
        await websocket.send(json.dumps(payload))

async def send_all_answers_debug(websocket):
    """Send a single big debug frame with all answers (handy for Burp to show everything at connect)."""
    all_answers = {i: q["answers"] for i, q in enumerate(QUESTIONS)}
    payload = {
        "type": "debug",
        "note": "All answers for this instance ",
        "all_answers": all_answers
    }
    await websocket.send(json.dumps(payload))

async def handler(websocket, path):
    client_id = id(websocket)
    CLIENT_STATE[client_id] = 0
    print(f"New challenger connected: {websocket.remote_address}")

    try:
        # Send one big debug with all answers at the start
        await send_all_answers_debug(websocket)

        # Send the first question
        await send_question(websocket)

        async for message in websocket:
            try:
                data = json.loads(message)
                if data.get("type") != "answer":
                    continue

                # 1. Normalize the user's submitted answer
                answer_text = data.get("text", "").lower().strip()
                
                question_index = CLIENT_STATE.get(client_id, 0)
                
                if question_index >= len(QUESTIONS):
                    continue

                question_data = QUESTIONS[question_index]
                
                # 2. FIX: Normalize all the correct answers from the list for consistent comparison
                correct_answers = question_data["answers"]
                normalized_correct_answers = [a.lower().strip() for a in correct_answers]

                # 3. Check against the normalized list
                if answer_text in normalized_correct_answers:
                    # ✅ Correct Answer: Move to the next question
                    CLIENT_STATE[client_id] += 1
                    feedback = {
                        "type": "feedback", "correct": True,
                        "message": "S7i7! That's correct! Here's the next one."
                    }
                    await websocket.send(json.dumps(feedback))

                    if CLIENT_STATE[client_id] == len(QUESTIONS):
                        flag_payload = {"type": "flag", "flag": FLAG}
                        await websocket.send(json.dumps(flag_payload))
                    else:
                        await send_question(websocket)
                else:
                    # ❌ Incorrect Answer: Send feedback with the correct answer (Active Leak)
                    
                    # Get the first correct answer from the original list (for the leak)
                    valid_response = correct_answers[0] 
                    
                    feedback = {
                        "type": "feedback", 
                        "correct": False,
                        "message": "Ghalet! That's not it. Think harder, ya m3allem!",
                        # INJECTION: Include the valid answer for the current question
                        "valid_answer_for_current_question": valid_response
                    }
                    await websocket.send(json.dumps(feedback))

            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error processing message: {e}")
                error_payload = {"type": "error", "message": "Invalid message format."}
                await websocket.send(json.dumps(error_payload))

    finally:
        print(f"Challenger {websocket.remote_address} disconnected.")
        if client_id in CLIENT_STATE:
            del CLIENT_STATE[client_id]

async def main():
    host = "0.0.0.0"
    port = 8765
    async with websockets.serve(handler, host, port):
        print(f"Choufli Hal CTF Server started on ws://{host}:{port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())