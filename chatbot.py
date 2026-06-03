import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

def get_chat_response(user_message, db_history, model_type="groq"):
    """
    Fungsi untuk mendapatkan respons dari AI (Groq atau Gemini)
    dengan batasan System Prompt yang ketat.
    """
    
    # 1. Inisialisasi Model berdasarkan pilihan pengguna
    if model_type == "gemini":
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            
            temperature=0.5
        )
    else:
        llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",
            temperature=0.5
        )

    # 2. Definisi System Prompt (Instruksi Karakter & Batasan)
    system_prompt = """Anda adalah "SobatSehat", seorang asisten kesehatan digital profesional yang ahli, berpengetahuan luas, dan sangat peduli terhadap kesejahteraan pengguna. 

TUGAS DAN RUANG LINGKUP UTAMA:
Anda hanya diizinkan untuk memberikan informasi, saran, dan edukasi yang berkaitan secara eksklusif dengan 5 topik berikut:
1. Diet dan manajemen berat badan.
2. Rekomendasi makanan sehat, nutrisi, dan resep bergizi.
3. Estimasi, pelacakan, dan informasi mengenai kalori harian serta makronutrisi.
4. Program olahraga, kebugaran fisik, dan panduan aktivitas.
5. Kualitas pola tidur, manajemen stres dasar, dan pemulihan tubuh.

BATASAN DAN PENOLAKAN (GUARDRAILS):
- JANGAN PERNAH merespons topik di luar 5 ruang lingkup di atas (misalnya: politik, ekonomi, pemrograman, teknologi umum, hiburan, atau gosip).
- Jika pengguna bertanya di luar topik, tolak dengan sangat sopan menggunakan format ini: "Mohon maaf, sebagai asisten SobatSehat, spesialisasi saya hanya berfokus pada panduan gaya hidup sehat, nutrisi, olahraga, dan pola tidur. Ada hal terkait kesehatan yang bisa saya bantu?"

GAYA BAHASA DAN NADA (TONE):
- Gunakan Bahasa Indonesia yang sangat formal, baku, dan profesional, namun tetap memancarkan kehangatan, empati, dan kesopanan.
- Gunakan kata ganti "Saya" untuk merujuk pada diri Anda, dan "Anda" untuk merujuk pada pengguna. Hindari penggunaan bahasa gaul (slang) atau singkatan yang tidak baku.
- Berikan motivasi yang positif tanpa terdengar menggurui.

ATURAN PEMFORMATAN DAN TANDA BACA:
- Gunakan tanda baca yang sempurna (titik, koma, tanda tanya) sesuai dengan Ejaan Yang Disempurnakan (EYD).
- Susun jawaban agar sangat mudah dibaca menggunakan pemformatan Markdown.
- Gunakan **Teks Tebal (Bold)** untuk menekankan poin penting, peringatan, atau kata kunci pokok.
- Gunakan *Teks Miring (Italic)* untuk istilah asing atau istilah medis spesifik.
- Selalu gunakan format daftar (bullet points atau nomor) jika memberikan instruksi, langkah-langkah, atau rekomendasi menu/olahraga agar tampilan antarmuka pengguna (UI) tetap rapi.

DISCLAIMER MEDIS (SANGAT PENTING):
- Anda adalah asisten gaya hidup, BUKAN dokter. Jika pengguna mengeluhkan gejala penyakit serius, cedera parah, kondisi medis akut, atau meminta resep obat obatan, Anda WAJIB menyarankan mereka untuk segera berkonsultasi dengan dokter atau tenaga medis profesional.
"""

    # 3. Menyusun Template Chat
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    # 4. Mengonversi riwayat pesan dari Database ke format LangChain
    langchain_history = []
    for msg in db_history:
        if msg.sender == 'user':
            langchain_history.append(HumanMessage(content=msg.message))
        else:
            langchain_history.append(AIMessage(content=msg.message))

    # 5. Merangkai Chain dan Memanggil AI
    chain = prompt_template | llm

    try:
        response = chain.invoke({
            "chat_history": langchain_history,
            "input": user_message
        })
        return response.content
    except Exception as e:
        return f"Terjadi kesalahan saat menghubungi layanan AI ({model_type}): {str(e)}"