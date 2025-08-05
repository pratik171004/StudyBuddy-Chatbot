from modules.study_assistant import StudyAssistant

bot = StudyAssistant()

print("\n🤖 Welcome to StudyMate CLI Bot! Ask me anything about your studies.")
print("🔚 Type 'exit' or 'quit' to close the bot.\n")

while True:
    query = input("You: ")
    if query.lower().strip() in ["exit", "quit"]:
        print("Bot: 👋 Goodbye! Keep learning.")
        break
    try:
        response = bot.get_response(query)
        print("Bot:", response)
    except Exception as e:
        print("❌ Error:", str(e))