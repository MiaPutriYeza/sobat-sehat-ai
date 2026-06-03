# 🌱 SobatSehat AI - Digital Health Assistant

SobatSehat is a comprehensive, end-to-end digital health assistant web application designed to provide reliable lifestyle, fitness, and nutrition guidance. Powered by Flask and Python, the backend utilizes LangChain to orchestrate an intelligent conversational interface with a multi-model selection feature, allowing users to seamlessly toggle between Groq (Llama 3.1) for ultra-fast responses and Gemini 2.5-Flash for deeper contextual reasoning. 

A key technical highlight of this project is its strict system prompt guardrails; the AI is programmed to only address five core wellness domains (diet, nutrition, calorie tracking, exercise, and sleep/stress management) while politely deflecting out-of-scope topics and providing essential medical disclaimers. 

The application features a robust relational database schema using SQLite and SQLAlchemy to manage user authentication, secure session-based chat history, and chat management tools such as pinning, renaming, and deleting conversations. The user interface is elegantly designed with Tailwind CSS, offering a clean, responsive, and modern dashboard equipped with dynamic typing indicators, interactive modals, and an integrated health blog component.

---

## ✨ Key Features
*   🤖 **Multi-Model AI Selection:** Seamlessly switch between **Groq (Llama 3.1 8B)** for speed and **Google Gemini 2.5-Flash** for deep reasoning.
*   🛡️ **Strict Conversational Guardrails:** The AI strictly operates within 5 wellness domains and refuses out-of-scope queries (e.g., politics, coding).
*   🔒 **Secure User Authentication:** Register and login system with hashed passwords.
*   📝 **Smart Chat Management:** Save histories, pin important sessions, rename chats, and delete records permanently.
*   💻 **Modern & Responsive UI:** Built with Tailwind CSS, featuring a clean dashboard, smooth transitions, and dynamic typing indicators.

## 🛠️ Tech Stack
*   **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-CORS
*   **AI Integration:** LangChain, Groq API, Google Generative AI
*   **Database:** SQLite (managed via SQLAlchemy ORM)
*   **Frontend:** HTML5, Tailwind CSS, JavaScript (Vanilla)

