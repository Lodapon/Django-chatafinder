from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
import random
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create your views here.

TAROT_CARDS = [
    # Major Arcana (22)
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World",

    # Minor Arcana - Cups (14)
    "Ace of Cups", "Two of Cups", "Three of Cups", "Four of Cups", "Five of Cups",
    "Six of Cups", "Seven of Cups", "Eight of Cups", "Nine of Cups", "Ten of Cups",
    "Page of Cups", "Knight of Cups", "Queen of Cups", "King of Cups",

    # Minor Arcana - Pentacles (14)
    "Ace of Pentacles", "Two of Pentacles", "Three of Pentacles", "Four of Pentacles", "Five of Pentacles",
    "Six of Pentacles", "Seven of Pentacles", "Eight of Pentacles", "Nine of Pentacles", "Ten of Pentacles",
    "Page of Pentacles", "Knight of Pentacles", "Queen of Pentacles", "King of Pentacles",

    # Minor Arcana - Swords (14)
    "Ace of Swords", "Two of Swords", "Three of Swords", "Four of Swords", "Five of Swords",
    "Six of Swords", "Seven of Swords", "Eight of Swords", "Nine of Swords", "Ten of Swords",
    "Page of Swords", "Knight of Swords", "Queen of Swords", "King of Swords",

    # Minor Arcana - Wands (14)
    "Ace of Wands", "Two of Wands", "Three of Wands", "Four of Wands", "Five of Wands",
    "Six of Wands", "Seven of Wands", "Eight of Wands", "Nine of Wands", "Ten of Wands",
    "Page of Wands", "Knight of Wands", "Queen of Wands", "King of Wands"
]


def homepage(request):
    return render(request, 'tarot_chatbot/homepage.html')

@csrf_exempt
def select_cards(request):
    if request.method == 'POST':
        selected = request.POST.getlist('selected_cards')
        if len(selected) == 10:
            request.session['tarot_cards'] = selected
            return redirect('tarot_chat')  # go to chat after selection
        else:
            error = "กรุณาเลือกไพ่ให้ครบ 10 ใบ"
            return render(request, 'tarot_chatbot/select_cards.html', {
                'card_pool': TAROT_CARDS,
                'error': error,
                'selected': selected,
            })

    return render(request, 'tarot_chatbot/select_cards.html', {'card_pool': TAROT_CARDS})

def extract_cards_from_text(text):
    """Return a list of card names that appear in the given text."""
    matches = []
    for card in TAROT_CARDS:
        if card in text:
            matches.append(card)
    return matches


@csrf_exempt
def tarot_chat(request):

    if 'tarot_cards' not in request.session:
        return redirect('select_cards')

    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    chat = request.session['chat_history'].copy()

    if request.method == 'POST':
        if request.POST.get('reset') == 'true':
            request.session.flush()
            return redirect('tarot_chat')

        user_input = request.POST.get('user_input')

        if user_input:
            chat.append({'sender': 'user', 'text': user_input})

            # ✅ DRAW ONLY IF NOT YET DRAWN
            # if 'tarot_cards' not in request.session:
            #     drawn_cards = random.sample(TAROT_CARDS, 10)
            #     request.session['tarot_cards'] = drawn_cards
            if 'tarot_cards' not in request.session:
                return render(request, 'tarot_chatbot/select_cards.html', {'card_pool': TAROT_CARDS})
            else:
                drawn_cards = request.session['tarot_cards']

            # Initialize or retrieve extra drawn cards
            if 'extra_tarot_cards' not in request.session:
                request.session['extra_tarot_cards'] = []
            extra_cards = request.session['extra_tarot_cards']

            # ✅ FORMAT TEXT
            card_text = ", ".join(drawn_cards)

            # ✅ SYSTEM INSTRUCTION (your long prompt as one system message) (Prompt ตอบดี)
            system_prompt = f"""คุณคือนักพยากรณ์ไพ่ทาโรต์ผู้เชี่ยวชาญด้านอาชีพ โชคชะตา และจิตวิทยา

            คุณกำลังสนทนากับผู้ใช้เพื่อช่วยให้คำปรึกษาในเรื่องอะไรก็ตามที่ถูกถาม

            คุณสามารถเริ่มต้นด้วยการพูดคุยอย่างเป็นมิตร สร้างความไว้วางใจ และถ้าคุณรู้สึกว่าได้รับคำถามหรือบริบทที่เหมาะสม คุณสามารถตัดสินใจ "จับไพ่ทาโรต์ 10 ใบตามหลัก Celtic Cross" ด้วยตนเอง และวิเคราะห์ผลของไพ่ 10 ใบดังกล่าวให้ผู้ใช้ฟังก่อน

            คุณสามารถถามถึงความกังวลหรือคำถามที่ผู้ใช้อยากรู้ได้

            ถ้าในภายหลังคุณรู้สึกว่าไพ่ 10 ใบไม่เพียงพอสำหรับคำถามต่อๆ มา คุณสามารถขอให้ผู้ใช้จับไพ่เพิ่มอีก 3 ใบได้

            คุณไม่จำเป็นต้องอธิบายถึงไพ่ทีละใบทุกครั้งที่ทำนาย (ถ้าคุณได้อธิบายไปแล้วในครั้งแรก) ดังนั้นคุณสามารถพูดถึงคำทำนายได้เลย

            **อย่าจับไพ่ทันที** — จงพิจารณาความเหมาะสมของคำถามก่อน และตอบกลับอย่างเป็นธรรมชาติแบบนักพยากรณ์ที่อบอุ่นและรอบคอบ

            ไพ่ที่จับไว้: {card_text}
            (ใช้ไพ่ชุดนี้ตลอดการสนทนา ยกเว้นคุณขอไพ่เพิ่มเอง)
            ไพ่เพิ่มเติม (ถ้ามี): {', '.join(extra_cards) if extra_cards else 'ไม่มี'}
            """

            # Prompt ตอบเร็ว
            # system_prompt = f"""
            # คุณคือนักพยากรณ์ไพ่ทาโรต์ที่อบอุ่นและเชี่ยวชาญด้านอาชีพ โชคชะตา และจิตวิทยา

            # คุณกำลังสนทนากับผู้ใช้เพื่อให้คำแนะนำจากไพ่ 10 ใบที่จับไว้:
            # {card_text}

            # (ใช้ไพ่ชุดนี้ตลอดการสนทนา ยกเว้นขอไพ่เพิ่ม)
            # ไพ่เพิ่มเติม: {', '.join(extra_cards) if extra_cards else 'ไม่มี'}
            # """

            # ✅ BUILD MESSAGES LIST (limit to last 30 interactions to save tokens)
            messages = [{"role": "system", "content": system_prompt}]
            max_history = 5
            for entry in chat[-max_history:]:
                role = "user" if entry["sender"] == "user" else "assistant"
                messages.append({"role": role, "content": entry["text"]})

            # ✅ ADD LATEST USER INPUT
            messages.append({"role": "user", "content": user_input})

            # ✅ CALL GPT WITH MESSAGES
            reply = ask_chatgpt(messages)

            # Check if GPT requested 3 more cards
            if any(keyword in reply.lower() for keyword in ["จับไพ่เพิ่ม", "ไพ่เพิ่มอีก 3", "เพิ่มอีก 3 ใบ"]) and len(extra_cards) == 0:
                # Filter remaining cards
                remaining = list(set(TAROT_CARDS) - set(drawn_cards) - set(extra_cards))
                new_cards = random.sample(remaining, 3)
                extra_cards.extend(new_cards)
                request.session['extra_tarot_cards'] = extra_cards

                # Append extra card info to GPT reply
                reply += f"\n\n🃏 ไพ่เพิ่มเติมที่จับได้: {', '.join(new_cards)}"

            chat.append({'sender': 'bot', 'text': reply})
            request.session['chat_history'] = chat

    return render(request, 'tarot_chatbot/chat.html', {
        'chat_history': chat
    })


def ask_chatgpt(messages):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.9,
    )
    return response.choices[0].message.content.strip()