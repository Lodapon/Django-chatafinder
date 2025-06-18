from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def homepage(request):
    return render(request, 'tarot_chatbot/homepage.html')


@csrf_exempt
def tarot_chat(request):
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        if user_input:
            chat = request.session['chat_history']
            chat.append({'sender': 'user', 'text': user_input})
            # Fake response for now
            chat.append({'sender': 'bot', 'text': f"คุณพิมพ์ว่า: {user_input}"})
            request.session['chat_history'] = chat

    return render(request, 'tarot_chatbot/chat.html', {
        'chat_history': request.session.get('chat_history', [])
    })