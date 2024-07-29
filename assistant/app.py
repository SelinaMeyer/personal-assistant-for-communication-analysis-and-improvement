import requests, json
import ollama
from ollama import AsyncClient
import time
import asyncio

import gradio as gr


model = 'phi3:mini' #You can replace the model name if needed; stablelm-zephyr      phi3:mini
context = [] 

client = AsyncClient(host='http://ollama:11434')


import gradio as gr

def clear_text(message):
    """
    Clears the Textbox after the response has been generated
    """
    return ""


async def generate(input, context, relationship_type, conversational_context, person):
    """
    This asynchronous function generates a conversation prompt based on the 
    given input, relationship type, conversational context, and persona. It 
    uses predefined dictionaries to construct the relationship type, 
    conversational context, and context string, then loads the corresponding 
    JSON file to get the chatbot prompt. The function interacts with the chat 
    model using the Ollama.chat API to generate a response and returns it 
    along with the conversation context.

    Args:
    - input (str): User input for the conversation prompt
    - context (List[Dict]): Previous conversation context
    - relationship_type (str): Type of relationship between the personas in 
    the conversation
    - conversational_context (str): Current conversational context for the 
    interaction
    - person (str): Persona involved in the conversation

    Returns:
    A tuple containing the generated response and updated conversation 
    context
    """

    relationship_dict = {
        "Romantic Relationship": "relationship", 
        "Friendship": "friendship", 
        "Workplace (Colleagues)": "workplace-no-hierarchy", 
        "Workplace (Manager)": f"workplace-hierarchy"
    }

    conversational_contexts_dict = {
        "I feel like I may have acted wrong":"Advice-for-culprit",
        "I feel I might have been mistreated":"Advice for victim",
        "I don't know what to say next":"Next reply"
    }

    with open(f"few_shot_prompts/{relationship_dict.get(relationship_type)}-{conversational_contexts_dict.get(conversational_context)}.json", "r") as file:
        prompt = json.load(file)

    relationship_types = {
        "Romantic Relationship": f"This is a conversation between me ({person}) and my romantic partner", 
        "Friendship": f"This is a conversation between me ({person}) and my friends", 
        "Workplace (Colleagues)": f"This is a conversation between me ({person}) and my colleagues", 
        "Workplace (Manager)": f"This is a conversation between me ({person}) and my manager"
    }

    conversational_contexts = {
        "I feel like I may have acted wrong": "I feel I might have acted wrong in the conversation. Did I make any mistakes? What could I do better?",
        "I feel I might have been mistreated": "The conversation leaves me uneasy, but I do not know why. What went wrong in this interaction?",
        "I don't know what to say next": "I don't like the way this interaction went. What should I say next? Why would that be the right reaction?"
    }
    
    user_string = f"""{relationship_types.get(relationship_type)} 

                        {input} 
                        
                        {conversational_contexts.get(conversational_context)}"""
    prompt.append({"role": "user", "content": user_string})

    response = ""
    async for chunk in await client.chat(model=model, messages=prompt,stream=True):
        print(chunk)
        response_part = chunk['message']['content']
        print(response_part)
        if 'error' in chunk:
            raise Exception(chunk['error'])

        response += response_part
        context = chunk.get('context', [])
        yield response, context
        
    yield response, context


async def chat(input, chat_history, relationship_type, conversational_context, person):
    """
    This asynchronous generator function takes user input and generates a 
    response using the `generate` function. The conversation history is 
    updated with the latest input-response pair and appended to the history 
    list. It yields the updated conversation history at each iteration.

    Args:
    - input (str): User input for the conversation prompt
    - chat_history (List[Tuple[str, str]] = []): Previous conversation history
    - relationship_type (str): Type of relationship between the personas in 
    the conversation
    - conversational_context (str): Current conversational context for the 
    interaction
    - person (str): Persona involved in the conversation

    Yields:
    A generator that yields the updated conversation history at each 
    iteration
    """

    chat_history = chat_history or []

    global context
    chat_history.append((input, ""))

    async for response, new_context in generate(input, context, relationship_type, conversational_context, person):
        context = new_context
        chat_history[-1] = (input, response)
        yield chat_history, chat_history

    yield chat_history, chat_history

#########################Gradio Code##########################
block = gr.Blocks()


with block:

    gr.Markdown("""<h1><center> Communication Advice Assistant </center></h1>
    """)

    # Creating an instance of gr.Chatbot() to be used as the chatbot interface
    chatbot = gr.Chatbot()

    # Creating a gr.Textbox widget for users to paste their chat messages, with 5 lines in height and a placeholder text
    message = gr.Textbox(placeholder="Paste your Chat here.", lines=5)

    # Setting up a state variable to store the current state of the application
    state = gr.State()

    with gr.Row():
        # Create a dropdown menu for selecting the relationship type
        relationship_type = gr.Dropdown(choices=["Romantic Relationship", "Friendship", "Workplace (Colleagues)", "Workplace (Manager)"], label="What type of relationship are you seeking advice on?", value="Romantic Relationship")
        # Create a dropdown menu for the conversational context
        conversational_context = gr.Dropdown(choices=["I feel like I may have acted wrong", "I feel I might have been mistreated", "I don't know what to say next"], label="What is the reason you are seeking advice?", value="I feel I might have been mistreated")
        # Create a textbox for the user's name
        person = gr.Textbox(label="Who are you in this conversation?", value="Your Name")

    # Creating a submit button
    submit = gr.Button("SEND")

    # Setting up a click event for the submit button:
    # 1) call 'chat' function with inputs: message, state, relationship_type, conversational_context, and person
    # 2) call 'clear_text' function with input: message
    # 3) Launch the application if the script is run as the main file using asyncio.run()

    submit.click(chat, inputs=[message, state, relationship_type, conversational_context, person], outputs=[chatbot, state]).then(clear_text, [message], [message])

# Launching the application if the script is run as the main file using asyncio.run()
if __name__ == "__main__":
    asyncio.run(block.launch(debug=True))