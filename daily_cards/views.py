from django.shortcuts import render
from .models import DailyCardSet
from tarot_chatbot.models import TarotCard
import datetime
import random
from datetime import date
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Global cache to store today's cards and horoscope
CARDS_CACHE = {
    "date": None,
    "cards": [],
    "horoscope": ""
}

def cards_of_the_day(request):
    today = date.today()

    if CARDS_CACHE["date"] != today:
        all_cards = list(TarotCard.objects.all())
        if len(all_cards) < 3:
            return render(request, 'daily_cards/error.html', {
                "message": "ยังไม่มีไพ่ในระบบมากพอสำหรับการสุ่มรายวัน (ต้องมีอย่างน้อย 3 ใบ)"
            })
        selected_cards = random.sample(all_cards, 3)

        # Get card names for prompt
        card_names = [card.name for card in selected_cards]

        # Generate horoscope using GPT
        prompt = f"""
		Today’s tarot cards are: {', '.join(card_names)}.
		Please provide a daily horoscope in Thai language, but do not translate the tarot card names (keep them in English).
		The horoscope should be no more than 5 sentences.
		"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.8
            )
            horoscope = response.choices[0].message.content.strip()
        except Exception as e:
            horoscope = "ขออภัย ไม่สามารถให้คำทำนายได้ในขณะนี้"

        CARDS_CACHE["date"] = today
        CARDS_CACHE["cards"] = selected_cards
        CARDS_CACHE["horoscope"] = horoscope

    else:
        selected_cards = CARDS_CACHE["cards"]
        horoscope = CARDS_CACHE["horoscope"]

    return render(request, 'daily_cards/cards_of_the_day.html', {
        'cards': selected_cards,
        'today': today,
        'horoscope': horoscope,
    })