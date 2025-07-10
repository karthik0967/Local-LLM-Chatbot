from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests

# View function to render the main chat interface.


def chat_page(request):
    # This renders the HTML page located at templates/chat/chat.html
    return render(request, 'chat/chat.html')


# API endpoint to handle AJAX POST requests from the chat frontend.
@csrf_exempt  # Disable CSRF just for this API view (only okay for local dev)
def chat_api(request):
    if request.method == 'POST':
        # Get the user's message from the POST request.
        user_message = request.POST.get('message')

        # Prepare the payload for Ollama’s local LLM API.
        payload = {
            "model": "llama3.2",  # The local model name you installed
            "messages": [
                {"role": "user", "content": user_message}  # User input
            ],
            "stream": False  # Disable streaming; get full response at once
        }

        # Make a POST request to Ollama’s local chat API.
        response = requests.post(
            'http://localhost:11434/api/chat',
            json=payload
        )

        # Parse the JSON response from Ollama.
        response_json = response.json()

        # Extract the AI’s message text.
        ai_message = response_json['message']['content']

        # Return the AI response as JSON for the frontend to display.
        return JsonResponse({'message': ai_message})
