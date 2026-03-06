"""
actions.py — Custom Actions for Quotes Recommendation Chatbot
Powered by Rasa NLU

This file contains:
  - ActionRecommendQuote : recommends a quote based on detected intent
  - ActionAnotherQuote   : recommends another quote in the same category
"""

import random
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


# ─────────────────────────────────────────────────────────────────────────────
# QUOTE DATABASE
# ─────────────────────────────────────────────────────────────────────────────

QUOTES = {
    "inspiration": [
        {
            "text": "The only way to do great work is to love what you do.",
            "author": "Steve Jobs"
        },
        {
            "text": "In the middle of every difficulty lies opportunity.",
            "author": "Albert Einstein"
        },
        {
            "text": "It does not matter how slowly you go as long as you do not stop.",
            "author": "Confucius"
        },
        {
            "text": "Life is what happens when you're busy making other plans.",
            "author": "John Lennon"
        },
        {
            "text": "The future belongs to those who believe in the beauty of their dreams.",
            "author": "Eleanor Roosevelt"
        },
        {
            "text": "Spread love everywhere you go. Let no one ever come to you without leaving happier.",
            "author": "Mother Teresa"
        },
        {
            "text": "When you reach the end of your rope, tie a knot in it and hang on.",
            "author": "Franklin D. Roosevelt"
        },
        {
            "text": "Always remember that you are absolutely unique, just like everyone else.",
            "author": "Margaret Mead"
        },
        {
            "text": "Do not go where the path may lead, go instead where there is no path and leave a trail.",
            "author": "Ralph Waldo Emerson"
        },
        {
            "text": "You will face many defeats in life, but never let yourself be defeated.",
            "author": "Maya Angelou"
        },
        {
            "text": "The greatest glory in living lies not in never falling, but in rising every time we fall.",
            "author": "Nelson Mandela"
        },
        {
            "text": "In the end, it's not the years in your life that count. It's the life in your years.",
            "author": "Abraham Lincoln"
        },
    ],

    "motivation": [
        {
            "text": "You are never too old to set another goal or to dream a new dream.",
            "author": "C.S. Lewis"
        },
        {
            "text": "Everything you've ever wanted is on the other side of fear.",
            "author": "George Addair"
        },
        {
            "text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "author": "Winston Churchill"
        },
        {
            "text": "Believe you can and you're halfway there.",
            "author": "Theodore Roosevelt"
        },
        {
            "text": "Act as if what you do makes a difference. It does.",
            "author": "William James"
        },
        {
            "text": "What you get by achieving your goals is not as important as what you become by achieving them.",
            "author": "Zig Ziglar"
        },
        {
            "text": "It's not whether you get knocked down, it's whether you get up.",
            "author": "Vince Lombardi"
        },
        {
            "text": "The secret of getting ahead is getting started.",
            "author": "Mark Twain"
        },
        {
            "text": "With the new day comes new strength and new thoughts.",
            "author": "Eleanor Roosevelt"
        },
        {
            "text": "Energy and persistence conquer all things.",
            "author": "Benjamin Franklin"
        },
        {
            "text": "You don't have to be great to start, but you have to start to be great.",
            "author": "Zig Ziglar"
        },
        {
            "text": "Push yourself, because no one else is going to do it for you.",
            "author": "Unknown"
        },
    ],

    "success": [
        {
            "text": "Success usually comes to those who are too busy to be looking for it.",
            "author": "Henry David Thoreau"
        },
        {
            "text": "Don't watch the clock; do what it does. Keep going.",
            "author": "Sam Levenson"
        },
        {
            "text": "Success is not how high you have climbed, but how you make a positive difference to the world.",
            "author": "Roy T. Bennett"
        },
        {
            "text": "I find that the harder I work, the more luck I seem to have.",
            "author": "Thomas Jefferson"
        },
        {
            "text": "Success is walking from failure to failure with no loss of enthusiasm.",
            "author": "Winston Churchill"
        },
        {
            "text": "Opportunities don't happen. You create them.",
            "author": "Chris Grosser"
        },
        {
            "text": "The road to success and the road to failure are almost exactly the same.",
            "author": "Colin R. Davis"
        },
        {
            "text": "Would you like me to give you a formula for success? It's quite simple, really: Double your rate of failure.",
            "author": "Thomas J. Watson"
        },
        {
            "text": "The secret to success is to know something nobody else knows.",
            "author": "Aristotle Onassis"
        },
        {
            "text": "There are no secrets to success. It is the result of preparation, hard work, and learning from failure.",
            "author": "Colin Powell"
        },
        {
            "text": "Success is liking yourself, liking what you do, and liking how you do it.",
            "author": "Maya Angelou"
        },
        {
            "text": "The only place where success comes before work is in the dictionary.",
            "author": "Vidal Sassoon"
        },
    ],

    "love": [
        {
            "text": "The best thing to hold onto in life is each other.",
            "author": "Audrey Hepburn"
        },
        {
            "text": "We accept the love we think we deserve.",
            "author": "Stephen Chbosky"
        },
        {
            "text": "Love is composed of a single soul inhabiting two bodies.",
            "author": "Aristotle"
        },
        {
            "text": "To love is nothing. To be loved is something. But to love and be loved, that's everything.",
            "author": "T. Tolis"
        },
        {
            "text": "Where there is love there is life.",
            "author": "Mahatma Gandhi"
        },
        {
            "text": "You know you're in love when you can't fall asleep because reality is finally better than your dreams.",
            "author": "Dr. Seuss"
        },
        {
            "text": "Love recognizes no barriers. It jumps hurdles, leaps fences, penetrates walls to arrive at its destination full of hope.",
            "author": "Maya Angelou"
        },
        {
            "text": "The best love is the kind that awakens the soul; that makes us reach for more.",
            "author": "Nicholas Sparks"
        },
        {
            "text": "I have decided to stick with love. Hate is too great a burden to bear.",
            "author": "Martin Luther King Jr."
        },
        {
            "text": "Love yourself first and everything else falls into line.",
            "author": "Lucille Ball"
        },
        {
            "text": "Keep love in your heart. A life without it is like a sunless garden when the flowers are dead.",
            "author": "Oscar Wilde"
        },
        {
            "text": "The giving of love is an education in itself.",
            "author": "Eleanor Roosevelt"
        },
    ],

    "humor": [
        {
            "text": "I'm writing a book. I've got the page numbers done.",
            "author": "Steven Wright"
        },
        {
            "text": "Age is of no importance unless you're a cheese.",
            "author": "Billie Burke"
        },
        {
            "text": "I am so clever that sometimes I don't understand a single word of what I am saying.",
            "author": "Oscar Wilde"
        },
        {
            "text": "Before you criticize someone, walk a mile in their shoes. That way, you'll be a mile away and have their shoes.",
            "author": "Jack Handey"
        },
        {
            "text": "Light travels faster than sound. This is why some people appear bright until they speak.",
            "author": "Alan Dundes"
        },
        {
            "text": "If you think you are too small to make a difference, try sleeping with a mosquito.",
            "author": "Dalai Lama"
        },
        {
            "text": "The trouble with having an open mind, of course, is that people will insist on coming along and trying to put things in it.",
            "author": "Terry Pratchett"
        },
        {
            "text": "Honest officer, the Unicorn rear-ended me.",
            "author": "Unknown"
        },
        {
            "text": "I asked God for a bike, but I know God doesn't work that way. So I stole a bike and asked for forgiveness.",
            "author": "Emo Philips"
        },
        {
            "text": "Never put off until tomorrow what you can do the day after tomorrow just as well.",
            "author": "Mark Twain"
        },
        {
            "text": "A day without laughter is a day wasted.",
            "author": "Charlie Chaplin"
        },
        {
            "text": "Common sense is like deodorant. The people who need it most never use it.",
            "author": "Unknown"
        },
    ],
}

# Maps Rasa intents → quote categories
INTENT_TO_CATEGORY = {
    "ask_inspiration":   "inspiration",
    "ask_motivation":    "motivation",
    "ask_success":       "success",
    "ask_love":          "love",
    "ask_humor":         "humor",
}

# Category display names and emojis
CATEGORY_META = {
    "inspiration": {"emoji": "✨", "label": "Inspiration"},
    "motivation":  {"emoji": "⚡", "label": "Motivation"},
    "success":     {"emoji": "🏆", "label": "Success"},
    "love":        {"emoji": "💛", "label": "Love"},
    "humor":       {"emoji": "😄", "label": "Humor"},
}


def format_quote(quote: dict, category: str) -> str:
    """Format a quote dict into a pretty message string."""
    meta = CATEGORY_META.get(category, {"emoji": "📖", "label": category.title()})
    return (
        f"{meta['emoji']} *{meta['label']} Quote*\n\n"
        f"_{quote['text']}_\n\n"
        f"— **{quote['author']}**"
    )


def get_random_quote(category: str) -> dict:
    """Return a random quote from the given category."""
    return random.choice(QUOTES[category])


# ─────────────────────────────────────────────────────────────────────────────
# ACTION: Recommend Quote
# ─────────────────────────────────────────────────────────────────────────────

class ActionRecommendQuote(Action):
    """
    Recommends a quote based on the detected intent.
    Maps intents like ask_inspiration → inspiration category.
    For ask_random, picks a random category.
    """

    def name(self) -> Text:
        return "action_recommend_quote"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message.get("intent", {}).get("name", "")

        # Determine category
        if intent == "ask_random":
            category = random.choice(list(QUOTES.keys()))
        else:
            category = INTENT_TO_CATEGORY.get(intent)

        if not category:
            dispatcher.utter_message(
                text="I'm not sure which type of quote you'd like. Try saying: "
                     "'inspire me', 'motivate me', 'success quote', 'love quote', "
                     "'funny quote', or 'surprise me'!"
            )
            return []

        quote = get_random_quote(category)
        message = format_quote(quote, category)
        dispatcher.utter_message(text=message)

        return [SlotSet("last_category", category)]


# ─────────────────────────────────────────────────────────────────────────────
# ACTION: Another Quote (same category)
# ─────────────────────────────────────────────────────────────────────────────

class ActionAnotherQuote(Action):
    """
    Returns another quote in the same category as the last one.
    If no previous category, picks a random category.
    """

    def name(self) -> Text:
        return "action_another_quote"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        category = tracker.get_slot("last_category")

        if not category:
            category = random.choice(list(QUOTES.keys()))

        quote = get_random_quote(category)
        message = format_quote(quote, category)
        dispatcher.utter_message(text=message)

        return [SlotSet("last_category", category)]
