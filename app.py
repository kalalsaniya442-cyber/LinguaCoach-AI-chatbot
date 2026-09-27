import os
import random
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="LinguaCoach - AI Language Tutor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Modern, Premium Design
st.markdown("""
<style>
    /* Global Styling */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #64748B;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .badge-online {
        background-color: #DEF7EC;
        color: #03543F;
        border: 1px solid #BCF0DA;
    }
    .badge-offline {
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #FDE68A;
    }
    .card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.2rem;
    }
    .flashcard-word {
        font-size: 2rem;
        font-weight: 700;
        color: #1E293B;
        text-align: center;
        margin: 1rem 0;
    }
    .flashcard-hint {
        font-size: 0.95rem;
        color: #64748B;
        text-align: center;
        font-style: italic;
    }
    .explanation-box {
        background-color: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 1rem;
        border-radius: 6px;
        margin-top: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2563EB;
    }
    .metric-label {
        font-size: 0.88rem;
        color: #64748B;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-pill {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vocab_correct" not in st.session_state:
    st.session_state.vocab_correct = 0

if "vocab_total" not in st.session_state:
    st.session_state.vocab_total = 0

if "grammar_correct" not in st.session_state:
    st.session_state.grammar_correct = 0

if "grammar_total" not in st.session_state:
    st.session_state.grammar_total = 0

if "vocab_index" not in st.session_state:
    st.session_state.vocab_index = 0

if "grammar_index" not in st.session_state:
    st.session_state.grammar_index = 0

if "vocab_submitted" not in st.session_state:
    st.session_state.vocab_submitted = False

if "grammar_submitted" not in st.session_state:
    st.session_state.grammar_submitted = False

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Learning Settings")
    
    native_lang = st.selectbox(
        "🗣️ Native Language",
        ["English", "Hindi", "Spanish", "French", "German"],
        index=0,
        help="The language you speak fluently. Explanations and corrections will appear in this language."
    )
    
    target_lang = st.selectbox(
        "🎯 Target Language",
        ["Spanish", "French", "German", "Italian"],
        index=0,
        help="The language you are actively learning."
    )
    
    skill_level = st.selectbox(
        "📊 Skill Level",
        ["Beginner", "Intermediate", "Advanced"],
        index=0,
        help="Adjusts conversational vocabulary and quiz difficulty."
    )
    
    topic = st.selectbox(
        "💬 Practice Topic",
        [
            "Greetings & Introductions",
            "Travel & Tourism",
            "Food & Dining",
            "Daily Routine & Lifestyle",
            "Work & Careers",
            "Hobbies & Leisure"
        ],
        index=0,
        help="The theme of the conversation and practice modules."
    )
    
    st.markdown("---")
    st.markdown("### 🔑 OpenAI API Configuration")
    
    env_api_key = os.getenv("OPENAI_API_KEY", "").strip()
    api_key_input = st.text_input(
        "OpenAI API Key (Optional)",
        value=env_api_key if env_api_key != "your_openai_api_key_here" else "",
        type="password",
        help="Enter your API key or configure it in .env. If left blank, LinguaCoach operates seamlessly in local fallback mode!"
    )
    
    env_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    model_choice = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        index=0 if env_model == "gpt-4o-mini" else 1
    )
    
    active_api_key = api_key_input.strip() if api_key_input.strip() else None
    
    if active_api_key:
        st.markdown(
            f'<div class="status-badge badge-online">🟢 OpenAI API Ready ({model_choice})</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="status-badge badge-offline">🟡 Offline Fallback Simulator Active</div>',
            unsafe_allow_html=True
        )
        
    st.markdown("---")
    st.markdown("### 🔄 Reset Session")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col_r2:
        if st.button("Reset Scores", use_container_width=True):
            st.session_state.vocab_correct = 0
            st.session_state.vocab_total = 0
            st.session_state.grammar_correct = 0
            st.session_state.grammar_total = 0
            st.session_state.vocab_index = 0
            st.session_state.grammar_index = 0
            st.session_state.vocab_submitted = False
            st.session_state.grammar_submitted = False
            st.rerun()

# ---------------------------------------------------------
# Curated Learning Content (Vocab & Grammar)
# ---------------------------------------------------------
VOCABULARY_DATA = {
    "Spanish": {
        "Beginner": [
            {
                "word": "La biblioteca",
                "pronunciation": "[lah bee-blee-oh-TEH-kah]",
                "options": ["The library", "The bookstore", "The kitchen", "The school"],
                "correct": "The library",
                "sentence": "Voy a la biblioteca para estudiar en silencio.",
                "sentence_trans": "I am going to the library to study in silence."
            },
            {
                "word": "El desayuno",
                "pronunciation": "[ehl deh-sah-YOO-noh]",
                "options": ["Breakfast", "Lunch", "Dinner", "Dessert"],
                "correct": "Breakfast",
                "sentence": "Siempre tomo café con leche durante el desayuno.",
                "sentence_trans": "I always drink coffee with milk during breakfast."
            },
            {
                "word": "Viajar",
                "pronunciation": "[bee-ah-HAHR]",
                "options": ["To travel", "To work", "To sleep", "To arrive"],
                "correct": "To travel",
                "sentence": "Me encanta viajar a nuevos países cada verano.",
                "sentence_trans": "I love to travel to new countries every summer."
            },
            {
                "word": "El pasaporte",
                "pronunciation": "[ehl pah-sah-POHR-teh]",
                "options": ["Passport", "Ticket", "Luggage", "Boarding pass"],
                "correct": "Passport",
                "sentence": "No olvides llevar tu pasaporte al aeropuerto.",
                "sentence_trans": "Don't forget to take your passport to the airport."
            },
            {
                "word": "La comida",
                "pronunciation": "[lah koh-MEE-dah]",
                "options": ["Food / Meal", "Drink", "Restaurant", "Recipe"],
                "correct": "Food / Meal",
                "sentence": "La comida española es famosa por sus tapas deliciosas.",
                "sentence_trans": "Spanish food is famous for its delicious tapas."
            }
        ],
        "Intermediate": [
            {
                "word": "El desafío",
                "pronunciation": "[ehl deh-sah-FEE-oh]",
                "options": ["Challenge", "Disappointment", "Development", "Discovery"],
                "correct": "Challenge",
                "sentence": "Aprender un nuevo idioma es un gran desafío personal.",
                "sentence_trans": "Learning a new language is a great personal challenge."
            },
            {
                "word": "Desarrollar",
                "pronunciation": "[deh-sah-rroh-YAHR]",
                "options": ["To develop", "To destroy", "To decide", "To deliver"],
                "correct": "To develop",
                "sentence": "Queremos desarrollar nuevas habilidades profesionales este año.",
                "sentence_trans": "We want to develop new professional skills this year."
            },
            {
                "word": "A menudo",
                "pronunciation": "[ah meh-NOO-doh]",
                "options": ["Often", "Rarely", "Quickly", "Suddenly"],
                "correct": "Often",
                "sentence": "Voy a menudo al parque para relajarme después del trabajo.",
                "sentence_trans": "I often go to the park to relax after work."
            },
            {
                "word": "El alojamiento",
                "pronunciation": "[ehl ah-loh-hah-MYEHN-toh]",
                "options": ["Accommodation / Lodging", "Flight", "Transportation", "Rental car"],
                "correct": "Accommodation / Lodging",
                "sentence": "Reservamos un alojamiento cerca del centro de la ciudad.",
                "sentence_trans": "We booked accommodation near the city center."
            }
        ],
        "Advanced": [
            {
                "word": "Imprescindible",
                "pronunciation": "[eem-preh-seen-DEE-bleh]",
                "options": ["Essential / Indispensable", "Unnecessary", "Unpredictable", "Unavoidable"],
                "correct": "Essential / Indispensable",
                "sentence": "La constancia es imprescindible para dominar la fluidez oral.",
                "sentence_trans": "Consistency is essential to master oral fluency."
            },
            {
                "word": "Paulatinamente",
                "pronunciation": "[pow-lah-tee-nah-MEHN-teh]",
                "options": ["Gradually / Step by step", "Instantly", "Carelessly", "Loudly"],
                "correct": "Gradually / Step by step",
                "sentence": "Su pronunciación mejoró paulatinamente con la práctica diaria.",
                "sentence_trans": "His pronunciation improved gradually with daily practice."
            }
        ]
    },
    "French": {
        "Beginner": [
            {
                "word": "La gare",
                "pronunciation": "[lah gahr]",
                "options": ["Train station", "Airport", "Bus stop", "Subway"],
                "correct": "Train station",
                "sentence": "Le train pour Paris part de la gare centrale.",
                "sentence_trans": "The train to Paris leaves from the central station."
            },
            {
                "word": "Le petit-déjeuner",
                "pronunciation": "[luh puh-tee-day-zhuh-nay]",
                "options": ["Breakfast", "Dinner", "Snack", "Appetizer"],
                "correct": "Breakfast",
                "sentence": "Je mange un croissant chaud au petit-déjeuner.",
                "sentence_trans": "I eat a warm croissant for breakfast."
            },
            {
                "word": "Le voyage",
                "pronunciation": "[luh vwah-yahzh]",
                "options": ["Trip / Journey", "Work", "Luggage", "Ticket"],
                "correct": "Trip / Journey",
                "sentence": "Bon voyage et profitez bien de vos vacances !",
                "sentence_trans": "Have a great trip and enjoy your vacation!"
            }
        ],
        "Intermediate": [
            {
                "word": "Cependant",
                "pronunciation": "[suh-pahn-dahn]",
                "options": ["However / Nevertheless", "Therefore", "Because", "Immediately"],
                "correct": "However / Nevertheless",
                "sentence": "Il pleut beaucoup; cependant, nous irons nous promener.",
                "sentence_trans": "It is raining heavily; however, we will go for a walk."
            },
            {
                "word": "Améliorer",
                "pronunciation": "[ah-may-lyoh-ray]",
                "options": ["To improve", "To memorize", "To forget", "To explain"],
                "correct": "To improve",
                "sentence": "Pratiquer chaque jour aide à améliorer la prononciation.",
                "sentence_trans": "Practicing every day helps to improve pronunciation."
            }
        ],
        "Advanced": [
            {
                "word": "Néanmoins",
                "pronunciation": "[nay-ahn-mwan]",
                "options": ["Nonetheless / Regardless", "Furthermore", "Namely", "Otherwise"],
                "correct": "Nonetheless / Regardless",
                "sentence": "Le défi était complexe; néanmoins, nous avons réussi l'épreuve.",
                "sentence_trans": "The challenge was complex; nonetheless, we succeeded in the test."
            }
        ]
    },
    "German": {
        "Beginner": [
            {
                "word": "Der Flughafen",
                "pronunciation": "[dehr FLOOK-hah-fen]",
                "options": ["Airport", "Harbor", "Train station", "Highway"],
                "correct": "Airport",
                "sentence": "Wir müssen zwei Stunden vor Abflug am Flughafen sein.",
                "sentence_trans": "We must be at the airport two hours before departure."
            },
            {
                "word": "Das Frühstück",
                "pronunciation": "[dahs FREW-shtewk]",
                "options": ["Breakfast", "Lunch", "Dinner", "Coffee break"],
                "correct": "Breakfast",
                "sentence": "Zum Frühstück esse ich Brot mit Käse.",
                "sentence_trans": "For breakfast I eat bread with cheese."
            }
        ],
        "Intermediate": [
            {
                "word": "Die Herausforderung",
                "pronunciation": "[dee hehr-OWS-for-duh-roong]",
                "options": ["Challenge", "Opportunity", "Decision", "Promise"],
                "correct": "Challenge",
                "sentence": "Grammatik ist eine spannende Herausforderung.",
                "sentence_trans": "Grammar is an exciting challenge."
            }
        ],
        "Advanced": [
            {
                "word": "Voraussetzung",
                "pronunciation": "[foh-ROWZ-zet-soong]",
                "options": ["Prerequisite / Condition", "Consequence", "Conclusion", "Assumption"],
                "correct": "Prerequisite / Condition",
                "sentence": "Fließende Sprachkenntnisse sind eine wichtige Voraussetzung.",
                "sentence_trans": "Fluent language skills are an important prerequisite."
            }
        ]
    },
    "Italian": {
        "Beginner": [
            {
                "word": "La colazione",
                "pronunciation": "[lah koh-lah-TSYOH-neh]",
                "options": ["Breakfast", "Lunch", "Dinner", "Snack"],
                "correct": "Breakfast",
                "sentence": "In Italia facciamo colazione con un cappuccino e un cornetto.",
                "sentence_trans": "In Italy we have breakfast with a cappuccino and a croissant."
            },
            {
                "word": "La stazione",
                "pronunciation": "[lah stah-TSYOH-neh]",
                "options": ["Station", "Street", "Airport", "Square"],
                "correct": "Station",
                "sentence": "Il treno per Firenze arriva alla stazione centrale.",
                "sentence_trans": "The train for Florence arrives at the central station."
            }
        ],
        "Intermediate": [
            {
                "word": "Tuttavia",
                "pronunciation": "[toot-tah-VEE-ah]",
                "options": ["Nevertheless / However", "Therefore", "Always", "Finally"],
                "correct": "Nevertheless / However",
                "sentence": "Era stanco; tuttavia ha deciso di continuare a studiare.",
                "sentence_trans": "He was tired; however he decided to keep studying."
            }
        ],
        "Advanced": [
            {
                "word": "Dapprima",
                "pronunciation": "[dahp-PREE-mah]",
                "options": ["At first / Initially", "Afterwards", "Constantly", "Suddenly"],
                "correct": "At first / Initially",
                "sentence": "Dapprima sembrava difficile, poi tutto è diventato chiaro.",
                "sentence_trans": "At first it seemed difficult, then everything became clear."
            }
        ]
    }
}

GRAMMAR_DATA = {
    "Spanish": {
        "Beginner": [
            {
                "type": "multiple_choice",
                "prompt": "Choose the correct form of 'ser' or 'estar': 'Yo _____ en el restaurante.'",
                "options": ["soy", "estoy", "es", "está"],
                "correct": "estoy",
                "explanation": "Use 'estar' for temporary locations and current states. 'Yo estoy' is the 1st person singular form."
            },
            {
                "type": "fill_blank",
                "prompt": "Fill in the blank with the correct definite article (el/la/los/las): '_____ manzana es roja.'",
                "options": ["La", "El", "Las", "Los"],
                "correct": "La",
                "explanation": "'Manzana' is a singular feminine noun, so it requires the feminine article 'la'."
            },
            {
                "type": "multiple_choice",
                "prompt": "Select the correct present tense conjugation of 'hablar' for 'nosotros':",
                "options": ["hablamos", "hablan", "habláis", "hablo"],
                "correct": "hablamos",
                "explanation": "For regular -ar verbs, the 'nosotros' (we) ending in the present tense is -amos."
            }
        ],
        "Intermediate": [
            {
                "type": "multiple_choice",
                "prompt": "Select the correct preterite form: 'Ayer nosotros _____ (comer) paella.'",
                "options": ["comimos", "comemos", "comieron", "comíamos"],
                "correct": "comimos",
                "explanation": "'Ayer' (yesterday) triggers the preterite tense for a completed past action. The preterite ending for -er verbs with 'nosotros' is -imos."
            },
            {
                "type": "fill_blank",
                "prompt": "Choose 'por' or 'para': 'Este regalo es _____ ti.'",
                "options": ["para", "por"],
                "correct": "para",
                "explanation": "'Para' is used to indicate the recipient or final destination of an item."
            }
        ],
        "Advanced": [
            {
                "type": "multiple_choice",
                "prompt": "Choose the correct subjunctive form: 'Dudo que él _____ (venir) a la fiesta.'",
                "options": ["venga", "viene", "vendrá", "viniera"],
                "correct": "venga",
                "explanation": "Expressions of doubt like 'Dudo que' require the present subjunctive in the subordinate clause."
            }
        ]
    },
    "French": {
        "Beginner": [
            {
                "type": "multiple_choice",
                "prompt": "Choose the correct present tense of 'être': 'Nous _____ très contents.'",
                "options": ["sommes", "êtes", "sont", "suis"],
                "correct": "sommes",
                "explanation": "The 1st person plural (nous) form of the irregular verb 'être' is 'sommes'."
            },
            {
                "type": "fill_blank",
                "prompt": "Choose the correct article: 'Je veux _____ café s'il vous plaît.'",
                "options": ["un", "une", "des"],
                "correct": "un",
                "explanation": "'Café' is a masculine noun, so it takes the indefinite masculine article 'un'."
            }
        ],
        "Intermediate": [
            {
                "type": "multiple_choice",
                "prompt": "Choose between passé composé auxiliary: 'Elle _____ allée au cinéma hier.'",
                "options": ["est", "a", "était", "sera"],
                "correct": "est",
                "explanation": "'Aller' is a verb of movement and conjugated with 'être' in compound tenses with subject agreement ('allée')."
            }
        ],
        "Advanced": [
            {
                "type": "multiple_choice",
                "prompt": "Subjunctive trigger: 'Il faut que vous _____ (faire) attention.'",
                "options": ["fassiez", "faites", "ferez", "fesiez"],
                "correct": "fassiez",
                "explanation": "The impersonal expression 'Il faut que' mandates the subjunctive mood. For 'vous', 'faire' becomes 'fassiez'."
            }
        ]
    },
    "German": {
        "Beginner": [
            {
                "type": "multiple_choice",
                "prompt": "Choose the correct accusative article: 'Ich habe _____ Hund.' (masculine: der Hund)",
                "options": ["einen", "ein", "eine", "einem"],
                "correct": "einen",
                "explanation": "In German, masculine nouns in the direct object (accusative) case change from 'ein' to 'einen'."
            }
        ],
        "Intermediate": [
            {
                "type": "fill_blank",
                "prompt": "Choose the correct subordinating conjunction: 'Ich lerne Deutsch, _____ ich in Berlin arbeiten möchte.'",
                "options": ["weil", "denn", "aber"],
                "correct": "weil",
                "explanation": "'Weil' (because) sends the conjugated verb to the end of the subordinate clause."
            }
        ],
        "Advanced": [
            {
                "type": "multiple_choice",
                "prompt": "Konjunktiv II for polite request: '_____ Sie mir bitte helfen?'",
                "options": ["Könnten", "Können", "Konnten", "Kann"],
                "correct": "Könnten",
                "explanation": "'Könnten' is the Konjunktiv II form of 'können', standard for polite requests."
            }
        ]
    },
    "Italian": {
        "Beginner": [
            {
                "type": "multiple_choice",
                "prompt": "Choose the correct form of 'avere': 'Noi _____ una bella casa.'",
                "options": ["abbiamo", "hanno", "avete", "ho"],
                "correct": "abbiamo",
                "explanation": "'Abbiamo' is the 1st person plural ('noi') present tense conjugation of 'avere'."
            }
        ],
        "Intermediate": [
            {
                "type": "fill_blank",
                "prompt": "Choose the combined preposition: 'Vado _____ ristorante con amici.' (a + il)",
                "options": ["al", "nel", "sul"],
                "correct": "al",
                "explanation": "The preposition 'a' combines with the masculine singular article 'il' into 'al'."
            }
        ],
        "Advanced": [
            {
                "type": "multiple_choice",
                "prompt": "Congiuntivo presente: 'Penso che tu _____ ragione.'",
                "options": ["abbia", "hai", "avessi", "avrai"],
                "correct": "abbia",
                "explanation": "Verbs of opinion like 'pensare che' require the subjunctive in the subordinate clause ('tu abbia')."
            }
        ]
    }
}

# ---------------------------------------------------------
# Local Fallback Chat Engine (Zero API Key Required)
# ---------------------------------------------------------
LOCAL_FALLBACK_REPLIES = {
    "Spanish": {
        "Greetings & Introductions": [
            "¡Hola! Mucho gusto en saludarte. Me alegra mucho que quieras practicar español hoy. ¿De dónde eres y qué te motivó a aprender este hermoso idioma?",
            "¡Excelente! Saludar con naturalidad es el primer paso. ¿Cómo ha estado tu día hasta ahora?"
        ],
        "Travel & Tourism": [
            "¡Qué maravilloso tema! Viajar por España o América Latina es una experiencia inolvidable. ¿Hay alguna ciudad o país hispanohablante que sueñes con visitar pronto?",
            "Me encanta hablar de viajes. Cuando llegas a un hotel nuevo, ¿qué es lo primero que te gusta preguntar en la recepción?"
        ],
        "Food & Dining": [
            "¡Mmm, la gastronomía! Desde las tapas españolas hasta los tacos mexicanos, la comida es un arte. ¿Cuál es tu plato favorito y qué ingredientes lleva?",
            "¡Qué delicia! Imagina que estás en un restaurante tradicional. ¿Cómo le pedirías la cuenta amablemente al camarero?"
        ],
        "Daily Routine & Lifestyle": [
            "Organizar la rutina diaria es clave para el aprendizaje. ¿A qué hora sueles despertarte y cuál es tu momento favorito del día?",
            "¡Muy bien! Hablar de hábitos ayuda a dominar los verbos reflexivos. ¿Qué sueles hacer los fines de semana para descansar?"
        ],
        "Work & Careers": [
            "El vocabulario profesional te abrirá muchas puertas internacionales. ¿A qué te dedicas o qué tipo de proyecto te apasiona actualmente?",
            "Muy interesante. En el trabajo, ¿prefieres comunicarte por correo electrónico o tener reuniones en persona?"
        ],
        "Hobbies & Leisure": [
            "¡Los pasatiempos son la mejor forma de expresarse! En tus momentos libres, ¿prefieres leer, hacer deporte, o escuchar música?",
            "Tener pasatiempos divertidos mantiene la mente activa. ¿Qué música o películas en español has descubierto recientemente?"
        ]
    },
    "French": {
        "Greetings & Introductions": [
            "Bonjour ! Je suis ravi de faire votre connaissance. C'est un plaisir de vous aider à pratiquer le français. D'où venez-vous ?",
            "Enchanté ! Pratiquer un peu chaque jour est la clé du succès. Comment se passe votre journée ?"
        ],
        "Travel & Tourism": [
            "Voyager en France ou dans un pays francophone est une formidable aventure ! Avez-vous déjà visité Paris ou la Côte d'Azur ?",
            "Les voyages forment la jeunesse ! Quel est le prochain voyage que vous aimeriez planifier ?"
        ],
        "Food & Dining": [
            "La cuisine française est réputée dans le monde entier ! Quel est votre plat ou dessert préféré ?",
            "Un bon repas est toujours un moment de partage. Préférez-vous cuisiner chez vous ou aller au restaurant ?"
        ]
    },
    "German": {
        "Greetings & Introductions": [
            "Hallo! Schön, dich kennenzulernen. Wie geht es dir heute und warum lernst du Deutsch?",
            "Guten Tag! Es freut mich sehr, dir beim Deutschlernen zu helfen. Woher kommst du?"
        ],
        "Travel & Tourism": [
            "Reisen ist wunderbar! Möchtest du bald nach Deutschland, Österreich oder in die Schweiz reisen?",
            "Städte wie Berlin, Wien und München sind faszinierend. Welche Stadt interessiert dich am meisten?"
        ]
    },
    "Italian": {
        "Greetings & Introductions": [
            "Ciao! Piacere di conoscerti. Sono molto felice di praticare l'italiano con te oggi. Come stai?",
            "Buongiorno! Imparare l'italiano è un viaggio meraviglioso. Da dove vieni?"
        ],
        "Food & Dining": [
            "La cucina italiana è straordinaria! Ti piace di più la pasta fresca o la vera pizza napoletana?",
            "Un buon espresso o un cappuccino la mattina fa sempre bene. Come prendi il tuo caffè?"
        ]
    }
}

def generate_fallback_tutor_response(user_text, target, native, level, current_topic):
    """Generates a contextual, structured tutor response without requiring an API key."""
    # Look for matching target language and topic
    lang_dict = LOCAL_FALLBACK_REPLIES.get(target, LOCAL_FALLBACK_REPLIES["Spanish"])
    replies_list = lang_dict.get(current_topic, lang_dict.get("Greetings & Introductions", [
        f"¡Hola! Muy buen intento praticando en {target}. Continúa comunicándote."
    ]))
    
    selected_reply = random.choice(replies_list)
    
    # Generic intelligent feedback tailored to level and native language
    feedback_notes = {
        "English": f"💡 **Tutor Feedback & Tip (English):** Great job communicating your thoughts! Keep practicing sentence rhythm. Remember to pay close attention to noun gender and verb endings for {target}.",
        "Hindi": f"💡 **शिक्षक सुझाव (Hindi):** बहुत अच्छा प्रयास! {target} में लिंग और क्रिया रूपों (verb conjugations) का नियमित अभ्यास करते रहें।",
        "Spanish": f"💡 **Consejo del Tutor (Spanish):** ¡Excelente esfuerzo! Sigue cuidando la concordancia entre género y número en {target}.",
        "French": f"💡 **Conseil du tuteur (French):** Excellent travail ! Continuez à faire attention à la concordance des temps en {target}.",
        "German": f"💡 **Tipp vom Lehrer (German):** Sehr gute Arbeit! Achten Sie weiterhin auf die richtige Wortstellung und Deklination in {target}."
    }
    
    tip = feedback_notes.get(native, feedback_notes["English"])
    
    full_response = f"""{selected_reply}

{tip}

❓ **Proxima Pregunta ({target}):**
¿Podrías contarme un detalle más sobre eso en {target}? *(Try replying with a complete sentence!)*"""
    return full_response

def get_openai_tutor_response(messages_history, api_key, model, target, native, level, current_topic):
    """Calls OpenAI API with structured prompting to teach, correct, and interact."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        system_prompt = f"""You are LinguaCoach, an encouraging, professional, and friendly AI language tutor.
The user wants to learn {target}.
The user's native language is {native}.
The user's skill level is {level}.
The current practice topic is '{current_topic}'.

Instruction Rules:
1. Target Language Reply: First, respond naturally and conversationally in {target}, matching the student's {level} level.
2. Polite Corrections & Tips: In the student's native language ({native}), gently analyze their message.
   - If they made grammatical, vocabulary, or spelling mistakes, point them out kindly with the correct form and a short explanation.
   - If their message was error-free, praise their accuracy and offer a natural native idiom or synonym.
3. Follow-up Question: Always end with an engaging, open-ended question in {target} suited for {level} to encourage the student to keep practicing.
4. Formatting:
   [Your response in {target}]

   💡 **Feedback & Corrections ({native}):**
   - [Clear, helpful notes in {native}]

   ❓ **Question / Follow-up ({target}):**
   - [Follow-up question in {target}]
"""
        
        api_messages = [{"role": "system", "content": system_prompt}]
        for m in messages_history:
            api_messages.append({"role": m["role"], "content": m["content"]})
            
        completion = client.chat.completions.create(
            model=model,
            messages=api_messages,
            temperature=0.7,
            max_tokens=450
        )
        return completion.choices[0].message.content, None
    except Exception as e:
        return None, str(e)


# ---------------------------------------------------------
# Header & Navigation
# ---------------------------------------------------------
st.markdown('<div class="main-title">🌍 LinguaCoach AI</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="subtitle">Personalized language coaching • Learning <strong>{target_lang}</strong> ({skill_level}) in <strong>{native_lang}</strong> • Topic: <em>{topic}</em></div>',
    unsafe_allow_html=True
)

tab_chat, tab_vocab, tab_grammar, tab_progress = st.tabs([
    "💬 Chat Practice",
    "📚 Vocabulary Flashcards",
    "✍️ Grammar Exercises",
    "📊 Learning Progress"
])

# =========================================================
# TAB 1: CHAT PRACTICE
# =========================================================
with tab_chat:
    col_info1, col_info2 = st.columns([3, 1])
    with col_info1:
        st.markdown(f"##### 🗣️ Conversational Room: {target_lang} ({topic})")
        st.caption("Practice conversing freely. Your coach will reply in the target language and provide polite corrections in your native language.")
    with col_info2:
        if active_api_key:
            st.info(f"⚡ OpenAI Connected: {model_choice}", icon="🤖")
        else:
            st.warning("⚡ Local Fallback Mode (No API Key)", icon="💡")
            
    # Initial greeting if chat history is empty
    if not st.session_state.messages:
        initial_greetings = {
            "Spanish": f"¡Hola! Bienvenido/a a tu sesión de LinguaCoach. Hoy practicaremos sobre el tema '{topic}'. ¿Cómo te encuentras hoy?",
            "French": f"Bonjour et bienvenue sur LinguaCoach ! Aujourd'hui nous allons pratiquer sur le thème '{topic}'. Comment allez-vous ?",
            "German": f"Hallo und willkommen bei LinguaCoach! Heute üben wir das Thema '{topic}'. Wie geht es dir heute?",
            "Italian": f"Ciao e benvenuto su LinguaCoach! Oggi faremo pratica sul tema '{topic}'. Come stai oggi?"
        }
        greet_text = initial_greetings.get(target_lang, f"Hello! Welcome to LinguaCoach. Let's practice {target_lang} together!")
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"{greet_text}\n\n💡 **Tutor Note ({native_lang}):** Feel free to type in {target_lang}. If you don't know a word, you can ask in {native_lang}!"
        })

    # Render chat messages
    for msg in st.session_state.messages:
        avatar = "🧑‍🎓" if msg["role"] == "user" else "🌍"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Chat user input
    user_prompt = st.chat_input(f"Type your message in {target_lang} (or ask for help in {native_lang})...")
    if user_prompt:
        # Add user message to state
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(user_prompt)

        # Generate Assistant response
        with st.chat_message("assistant", avatar="🌍"):
            with st.spinner(f"LinguaCoach is crafting your {target_lang} feedback..."):
                response_text = ""
                used_fallback = False
                
                if active_api_key:
                    api_resp, err_msg = get_openai_tutor_response(
                        st.session_state.messages,
                        active_api_key,
                        model_choice,
                        target_lang,
                        native_lang,
                        skill_level,
                        topic
                    )
                    if api_resp:
                        response_text = api_resp
                    else:
                        st.caption(f"⚠️ *Notice: OpenAI API call encountered an issue ({err_msg}). Seamlessly switched to local fallback response.*")
                        response_text = generate_fallback_tutor_response(user_prompt, target_lang, native_lang, skill_level, topic)
                        used_fallback = True
                else:
                    response_text = generate_fallback_tutor_response(user_prompt, target_lang, native_lang, skill_level, topic)
                    used_fallback = True
                
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})


# =========================================================
# TAB 2: VOCABULARY FLASHCARDS
# =========================================================
with tab_vocab:
    st.markdown("### 📚 Interactive Vocabulary Flashcards")
    st.write(f"Test and expand your vocabulary in **{target_lang}** ({skill_level} level). Answer the multiple-choice card to reveal context and example sentences.")

    # Retrieve vocab list for selected target language and skill level
    target_vocab_dict = VOCABULARY_DATA.get(target_lang, VOCABULARY_DATA["Spanish"])
    vocab_items = target_vocab_dict.get(skill_level, target_vocab_dict.get("Beginner", []))

    if not vocab_items:
        st.info(f"No vocabulary items available for {target_lang} at {skill_level} level yet. Try switching to Beginner level.")
    else:
        # Bound index safely
        current_idx = st.session_state.vocab_index % len(vocab_items)
        card = vocab_items[current_idx]

        st.markdown(f"""
        <div class="card">
            <span class="badge-pill" style="background:#EEF2FF; color:#4338CA;">Word #{current_idx + 1} of {len(vocab_items)}</span>
            <span class="badge-pill" style="background:#F0FDF4; color:#15803D;">Level: {skill_level}</span>
            <span class="badge-pill" style="background:#FFF7ED; color:#C2410C;">Language: {target_lang}</span>
            <div class="flashcard-word">{card['word']}</div>
            <div class="flashcard-hint">Pronunciation: {card.get('pronunciation', '')}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**What is the correct translation for '{card['word']}' in {native_lang}?**")
        
        # Form for answering
        with st.form(key=f"vocab_form_{target_lang}_{skill_level}_{current_idx}"):
            user_choice = st.radio(
                "Select the best option:",
                options=card["options"],
                index=None,
                key=f"vocab_radio_{current_idx}"
            )
            submit_vocab = st.form_submit_button("Check Answer", type="primary")

        if submit_vocab:
            if user_choice is None:
                st.warning("Please pick an option before submitting!")
            else:
                st.session_state.vocab_submitted = True
                st.session_state.vocab_total += 1
                if user_choice == card["correct"]:
                    st.session_state.vocab_correct += 1
                    st.success(f"🎉 **Correct!** '{card['word']}' means **{card['correct']}**.")
                else:
                    st.error(f"❌ **Not quite!** You selected '{user_choice}', but the correct answer is **{card['correct']}**.")

                # Show contextual example sentence
                st.markdown(f"""
                <div class="explanation-box">
                    <strong>📖 Example in context:</strong><br>
                    <em>"{card['sentence']}"</em><br>
                    <span style="color:#64748B;">Translation: "{card['sentence_trans']}"</span>
                </div>
                """, unsafe_allow_html=True)

        col_v1, col_v2 = st.columns([1, 4])
        with col_v1:
            if st.button("Next Flashcard ➡️", key="next_vocab_btn"):
                st.session_state.vocab_index = (current_idx + 1) % len(vocab_items)
                st.session_state.vocab_submitted = False
                st.rerun()


# =========================================================
# TAB 3: GRAMMAR EXERCISES
# =========================================================
with tab_grammar:
    st.markdown("### ✍️ Interactive Grammar Exercises")
    st.write(f"Sharpen your grammar rules, conjugations, and syntax in **{target_lang}** ({skill_level} level).")

    target_grammar_dict = GRAMMAR_DATA.get(target_lang, GRAMMAR_DATA["Spanish"])
    grammar_items = target_grammar_dict.get(skill_level, target_grammar_dict.get("Beginner", []))

    if not grammar_items:
        st.info(f"No grammar exercises available for {target_lang} ({skill_level}). Switch to Beginner to practice core fundamentals.")
    else:
        g_idx = st.session_state.grammar_index % len(grammar_items)
        exercise = grammar_items[g_idx]

        st.markdown(f"""
        <div class="card">
            <span class="badge-pill" style="background:#FDF2F8; color:#BE185D;">Exercise #{g_idx + 1} of {len(grammar_items)}</span>
            <span class="badge-pill" style="background:#EFF6FF; color:#1D4ED8;">Type: {exercise['type'].replace('_', ' ').title()}</span>
            <h4 style="margin-top:1rem; color:#1E293B;">{exercise['prompt']}</h4>
        </div>
        """, unsafe_allow_html=True)

        with st.form(key=f"grammar_form_{target_lang}_{skill_level}_{g_idx}"):
            if exercise["type"] == "fill_blank":
                grammar_choice = st.radio(
                    "Choose the correct word to fill in the blank:",
                    options=exercise["options"],
                    index=None,
                    key=f"grammar_radio_{g_idx}"
                )
            else:
                grammar_choice = st.radio(
                    "Choose the correct option:",
                    options=exercise["options"],
                    index=None,
                    key=f"grammar_radio_{g_idx}"
                )
            submit_grammar = st.form_submit_button("Verify Answer", type="primary")

        if submit_grammar:
            if grammar_choice is None:
                st.warning("Please choose an answer first!")
            else:
                st.session_state.grammar_submitted = True
                st.session_state.grammar_total += 1
                if grammar_choice.strip().lower() == exercise["correct"].strip().lower():
                    st.session_state.grammar_correct += 1
                    st.success(f"🎉 **Spot on!** '{exercise['correct']}' is the right answer.")
                else:
                    st.error(f"❌ **Incorrect.** The correct answer is **{exercise['correct']}**.")

                st.markdown(f"""
                <div class="explanation-box">
                    <strong>💡 Deep Explanation:</strong><br>
                    {exercise['explanation']}
                </div>
                """, unsafe_allow_html=True)

        col_g1, col_g2 = st.columns([1, 4])
        with col_g1:
            if st.button("Next Exercise ➡️", key="next_grammar_btn"):
                st.session_state.grammar_index = (g_idx + 1) % len(grammar_items)
                st.session_state.grammar_submitted = False
                st.rerun()


# =========================================================
# TAB 4: LEARNING PROGRESS
# =========================================================
with tab_progress:
    st.markdown("### 📊 Learning Analytics & Milestones")
    st.write("Track your accuracy, quiz completion, and conversational activity in real time.")

    # Calculations
    v_total = st.session_state.vocab_total
    v_correct = st.session_state.vocab_correct
    v_acc = (v_correct / v_total * 100) if v_total > 0 else 0.0

    g_total = st.session_state.grammar_total
    g_correct = st.session_state.grammar_correct
    g_acc = (g_correct / g_total * 100) if g_total > 0 else 0.0

    overall_total = v_total + g_total
    overall_correct = v_correct + g_correct
    overall_acc = (overall_correct / overall_total * 100) if overall_total > 0 else 0.0

    user_messages_count = sum(1 for m in st.session_state.messages if m["role"] == "user")

    # Metrics Display
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{v_acc:.1f}%</div>
            <div class="metric-label">Vocabulary Accuracy</div>
            <small style="color:#64748B;">{v_correct} of {v_total} correct</small>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{g_acc:.1f}%</div>
            <div class="metric-label">Grammar Accuracy</div>
            <small style="color:#64748B;">{g_correct} of {g_total} correct</small>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{overall_acc:.1f}%</div>
            <div class="metric-label">Average Score</div>
            <small style="color:#64748B;">{overall_correct} of {overall_total} total answers</small>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{user_messages_count}</div>
            <div class="metric-label">Chat Messages Sent</div>
            <small style="color:#64748B;">Active conversational turns</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🎯 Mastery Progress Bars")

    col_bar1, col_bar2 = st.columns(2)
    with col_bar1:
        st.write(f"**Vocabulary Mastery ({v_acc:.0f}%)**")
        st.progress(min(1.0, v_acc / 100.0))
    with col_bar2:
        st.write(f"**Grammar Mastery ({g_acc:.0f}%)**")
        st.progress(min(1.0, g_acc / 100.0))

    st.markdown("---")
    st.markdown("#### 🏅 Achievement Milestones")
    
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    with col_b1:
        achieved = user_messages_count >= 1
        st.markdown(f"""
        <div class="card" style="text-align:center; opacity:{'1.0' if achieved else '0.45'};">
            <div style="font-size:2.2rem;">💬</div>
            <strong>First Contact</strong>
            <p style="font-size:0.8rem; color:#64748B; margin:0;">Send your 1st chat message</p>
            <span class="badge-pill" style="margin-top:0.5rem; background:{'#DEF7EC' if achieved else '#F1F5F9'}; color:{'#03543F' if achieved else '#94A3B8'};">
                {'Unlocked ✅' if achieved else 'Locked 🔒'}
            </span>
        </div>
        """, unsafe_allow_html=True)
    with col_b2:
        achieved = v_total >= 3
        st.markdown(f"""
        <div class="card" style="text-align:center; opacity:{'1.0' if achieved else '0.45'};">
            <div style="font-size:2.2rem;">📖</div>
            <strong>Vocab Explorer</strong>
            <p style="font-size:0.8rem; color:#64748B; margin:0;">Attempt 3+ flashcards</p>
            <span class="badge-pill" style="margin-top:0.5rem; background:{'#DEF7EC' if achieved else '#F1F5F9'}; color:{'#03543F' if achieved else '#94A3B8'};">
                {'Unlocked ✅' if achieved else 'Locked 🔒'}
            </span>
        </div>
        """, unsafe_allow_html=True)
    with col_b3:
        achieved = g_total >= 3
        st.markdown(f"""
        <div class="card" style="text-align:center; opacity:{'1.0' if achieved else '0.45'};">
            <div style="font-size:2.2rem;">✍️</div>
            <strong>Grammar Ace</strong>
            <p style="font-size:0.8rem; color:#64748B; margin:0;">Complete 3+ grammar drills</p>
            <span class="badge-pill" style="margin-top:0.5rem; background:{'#DEF7EC' if achieved else '#F1F5F9'}; color:{'#03543F' if achieved else '#94A3B8'};">
                {'Unlocked ✅' if achieved else 'Locked 🔒'}
            </span>
        </div>
        """, unsafe_allow_html=True)
    with col_b4:
        achieved = (overall_total >= 5 and overall_acc >= 75.0)
        st.markdown(f"""
        <div class="card" style="text-align:center; opacity:{'1.0' if achieved else '0.45'};">
            <div style="font-size:2.2rem;">👑</div>
            <strong>Polyglot Star</strong>
            <p style="font-size:0.8rem; color:#64748B; margin:0;">5+ exercises with ≥75% score</p>
            <span class="badge-pill" style="margin-top:0.5rem; background:{'#DEF7EC' if achieved else '#F1F5F9'}; color:{'#03543F' if achieved else '#94A3B8'};">
                {'Unlocked ✅' if achieved else 'Locked 🔒'}
            </span>
        </div>
        """, unsafe_allow_html=True)