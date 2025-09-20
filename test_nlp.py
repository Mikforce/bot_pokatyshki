from message_analyzer import analyze_message

# Тестовые сообщения
test_messages = [
    "го покатаемся на мотоциклах",
    "есть кто хочет на картинг?",
    "у меня сломался мотоцикл",
    "какое масло лить?",
    "поехали катать вечером",
    "посмотрите этот видос с мотокросса"
]

print("🧪 Тестирование NLP модели:")
for msg in test_messages:
    result, confidence = analyze_message(msg)
    print(f"'{msg}' -> {'🎯 Событие' if result else '❌ Не событие'} ({confidence:.2%})")