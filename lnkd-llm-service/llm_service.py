from ollama import Client

llm = Client(host="ollama")

def prompt_llm(doc: dict):
    PROMPT = "I want to send a personalized LinkedIn connection request. Here is the information about the person I'm connecting with:\n"

    if doc["target_name"]:
        PROMPT += f"NAME: {doc['target_name']}\n\n"
    if doc["target_headline"]:
        PROMPT += f"HEADLINE: {doc['target_headline']}\n\n"
    if doc["target_about"]:
        PROMPT += f"ABOUT: {doc['target_about']}\n\n"
    
    if len(doc["posts"]) > 0:
        PROMPT += "RECENT POSTS :\n\n"
    for index, post in enumerate(doc["posts"], start=1):
        PROMPT += f"-\tPost {index} : \"{post}\"\n"
    
    response = llm.chat(
        model="llama3.1",
        messages=[{
            "role": "system",
            "content": "Create a warm and personalized connection message using this information, highlighting common interests, a genuine compliment, or a shared professional topic if applicable. Make it friendly, concise, and authentic, ensuring that it respects LinkedIn's character limits."
        }, {
            "role": "user",
            "content": PROMPT
        }],
        stream=False,
    )

    return response['message']['content']