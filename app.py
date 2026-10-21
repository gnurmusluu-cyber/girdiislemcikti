import math
import random
import threading
import time
import uuid
import streamlit as st
import streamlit.components.v1 as components

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="GİÇ Dedektifi | 9. Sınıf Bilgisayar Bilimi",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

QUESTION_DURATION_SEC = 20
QUESTION_DURATION_MS = QUESTION_DURATION_SEC * 1000

# ============================================================================
# QUESTION DATASET (9th-Grade Computer Science Input-Process-Output Scenarios)
# ============================================================================
QUESTIONS = [
    {
        "id": 1,
        "title": "Taze Meyve Suyu",
        "theme": "Mutfak",
        "input": "Portakal",
        "process": "Meyve sıkacağında ezilip süzülmesi",
        "output": "?",
        "mystery": "output",
        "question": "Bu senaryoda ortaya çıkan ÇIKTI nedir?",
        "options": ["1 bardak portakal suyu", "Meyve sıkacağının fişi", "Portakal ağacı", "Pazardaki poşet"],
        "correctIndex": 0
    },
    {
        "id": 2,
        "title": "Çamaşır Makinesi",
        "theme": "Ev Eşyası",
        "input": "?",
        "process": "Sıcak su ve deterjanla 40 dk yıkama",
        "output": "Temiz ve mis kokulu kıyafetler",
        "mystery": "input",
        "question": "Makinenin içine ilk başta konulan GİRDİ nedir?",
        "options": ["Ütü masası", "Kurutma askısı", "Kirli çamaşırlar ve deterjan", "Gardırop"],
        "correctIndex": 2
    },
    {
        "id": 3,
        "title": "Telefonun Ses Düğmesi",
        "theme": "Telefon",
        "input": "Ses Açma (+) tuşuna basılması",
        "process": "?",
        "output": "Hoparlörden sesin daha yüksek çıkması",
        "mystery": "process",
        "question": "Telefonun tuşa basıldığında yaptığı İŞLEM nedir?",
        "options": ["Şarkıyı durdurmak", "Ses seviyesini 1 kademe artırmak", "Ekran parlaklığını kısmak", "Telefonu kapatmak"],
        "correctIndex": 1
    },
    {
        "id": 4,
        "title": "Otomatik Market Kapısı",
        "theme": "Sensörler",
        "input": "?",
        "process": "Önünde insan var mı kontrolü",
        "output": "Cam kapıların iki yana açılması",
        "mystery": "input",
        "question": "Kapıyı harekete geçiren GİRDİ hangisidir?",
        "options": ["Kasadaki fiş kağıdı", "Alışveriş arabasının tekeri", "Sensörün önündeki insanı algılaması", "Marketteki indirim afişi"],
        "correctIndex": 2
    },
    {
        "id": 5,
        "title": "Sınav Ortalaması",
        "theme": "Okul",
        "input": "1. Sınav: 60, 2. Sınav: 80",
        "process": "?",
        "output": "Ekranda beliren 70 ortalama notu",
        "mystery": "process",
        "question": "Ortalamayı bulmak için yapılan İŞLEM nedir?",
        "options": ["Notları toplayıp 2'ye bölmek", "İki notu birbiriyle çarpmak", "Notları okul müdürüne sormak", "İki notu birbirinden çıkarmak"],
        "correctIndex": 0
    },
    {
        "id": 6,
        "title": "Klavyeden Yazı Yazma",
        "theme": "Bilgisayar",
        "input": "Klavyedeki 'A' tuşuna basmak",
        "process": "Tuş kodunun ekrana iletilmesi",
        "output": "?",
        "mystery": "output",
        "question": "Bu hareketin sonucunda oluşan ÇIKTI nedir?",
        "options": ["Klavyenin kablosu", "Ekranda 'A' harfinin görünmesi", "Farenin ışığının sönmesi", "Bilgisayarın şarj olması"],
        "correctIndex": 1
    },
    {
        "id": 7,
        "title": "Fırında Kek Pişirme",
        "theme": "Mutfak",
        "input": "Sıvı kek hamuru ve fırın tepsisi",
        "process": "?",
        "output": "Kabarmış sıcak kek",
        "mystery": "process",
        "question": "Fırının gerçekleştirdiği asıl İŞLEM nedir?",
        "options": ["Kek kalıbını yıkamak", "180 derecede 35 dakika pişirmek", "Kekin içine fazladan süt eklemek", "Keki dilimlere ayırmak"],
        "correctIndex": 1
    },
    {
        "id": 8,
        "title": "Fotoğraf Çekme",
        "theme": "Telefon",
        "input": "?",
        "process": "Kameranın görüntüyü dijitale çevirmesi",
        "output": "Galeriye yeni bir fotoğraf eklenmesi",
        "mystery": "input",
        "question": "Fotoğrafın çekilmesini sağlayan GİRDİ nedir?",
        "options": ["Ekranda 'Fotoğraf Çek' butonuna dokunmak", "Telefonun arka kılıfı", "Telefonun şarj aleti", "Galerideki eski resimler"],
        "correctIndex": 0
    },
    {
        "id": 9,
        "title": "WhatsApp Mesajı",
        "theme": "İletişim",
        "input": "'Neredesin?' yazıp gönder okuna basmak",
        "process": "Mesajın internet üzerinden iletilmesi",
        "output": "?",
        "mystery": "output",
        "question": "Karşı tarafın telefonundaki ÇIKTI nedir?",
        "options": ["Telefonun pili", "İnternet modemi", "Arkadaşın ekranına düşen 'Neredesin?' mesajı", "Telefonun cam ekranı"],
        "correctIndex": 2
    },
    {
        "id": 10,
        "title": "Hesap Makinesinde Toplama",
        "theme": "Matematik",
        "input": "Ekrana '15' ve '25' yazıp '+' tuşuna basmak",
        "process": "İki sayının toplanması (15 + 25)",
        "output": "?",
        "mystery": "output",
        "question": "Hesap makinesinin ürettiği ÇIKTI nedir?",
        "options": ["Pil seviyesi", "Ekranda '40' yazması", "Açma/kapama tuşu", "Güneş paneli"],
        "correctIndex": 1
    }
]

OPTION_META = [
    {"label": "🟥 Kırmızı", "color_name": "Kırmızı", "hex": "#e11d48", "border": "#f43f5e", "cls": "opt-red"},
    {"label": "🟦 Mavi",    "color_name": "Mavi",    "hex": "#2563eb", "border": "#3b82f6", "cls": "opt-blue"},
    {"label": "🟨 Sarı",    "color_name": "Sarı",    "hex": "#d97706", "border": "#f59e0b", "cls": "opt-yellow"},
    {"label": "🟩 Yeşil",   "color_name": "Yeşil",   "hex": "#059669", "border": "#10b981", "cls": "opt-green"},
]


# ============================================================================
# SHARED MULTIPLAYER STATE ENGINE (@st.cache_resource)
# Shared across all connected students & teacher on Streamlit Cloud
# ============================================================================
class GameHub:
    def __init__(self):
        self.lock = threading.Lock()
        self.rooms = {}
        self.latest_pin = None
        self.create_room()

    def create_room(self, requested_pin=None):
        with self.lock:
            if requested_pin and str(requested_pin) in self.rooms:
                self.latest_pin = str(requested_pin)
                return self.rooms[str(requested_pin)]
            while True:
                pin = str(random.randint(1000, 9999))
                if pin not in self.rooms:
                    break
            room = {
                "pin": pin,
                "state": "LOBBY",  # LOBBY | QUESTION | REVEAL | LEADERBOARD | FINAL_PODIUM
                "currentQuestionIndex": 0,
                "questionStartTime": None,
                "players": {},
                "specialAwards": [],
                "createdAt": time.time(),
            }
            self.rooms[pin] = room
            self.latest_pin = pin
            return room

    def get_room(self, pin):
        if not pin:
            return None
        return self.rooms.get(str(pin).strip())

    def create_player(self, player_id, nickname, avatar="🕵️", is_bot=False):
        return {
            "id": player_id,
            "nickname": nickname.strip()[:18],
            "avatar": avatar or "🕵️",
            "isBot": is_bot,
            "score": 0,
            "streak": 0,
            "maxStreak": 0,
            "fireMode": False,
            "correctCount": 0,
            "answeredCount": 0,
            "totalResponseTimeMs": 0,
            "correctResponseTimeMs": 0,
            "categoryStats": {
                "input": {"correct": 0, "total": 0},
                "process": {"correct": 0, "total": 0},
                "output": {"correct": 0, "total": 0},
            },
            "currentAnswer": None,
            "botSimulatedDelayMs": None,
            "botSimulatedChoice": None,
            "badges": [],
            "lastSeen": time.time(),
        }

    def join_player(self, pin, player_id, nickname, avatar="🕵️"):
        with self.lock:
            room = self.rooms.get(str(pin).strip())
            if not room:
                return None, "Geçersiz Oyun PIN kodu! Lütfen akıllı tahtadaki 4 haneli PIN kodunu kontrol edin."
            clean_name = nickname.strip()
            if len(clean_name) < 2:
                return None, "Lütfen en az 2 karakterli bir takma ad girin."

            now = time.time()
            for pid, existing in list(room["players"].items()):
                if pid == player_id or (not existing["isBot"] and existing["nickname"].lower() == clean_name.lower()):
                    existing["nickname"] = clean_name
                    existing["avatar"] = avatar or existing["avatar"]
                    existing["lastSeen"] = now
                    room["players"][player_id] = existing
                    if pid != player_id:
                        del room["players"][pid]
                    return existing, None

            new_p = self.create_player(player_id, clean_name, avatar, is_bot=False)
            room["players"][player_id] = new_p
            return new_p, None

    def heartbeat_player(self, pin, player_id):
        with self.lock:
            room = self.rooms.get(str(pin).strip())
            if not room:
                return
            player = room["players"].get(player_id)
            if player:
                player["lastSeen"] = time.time()

    def leave_player(self, pin, player_id):
        with self.lock:
            room = self.rooms.get(str(pin).strip())
            if not room:
                return
            room["players"].pop(player_id, None)

    def prune_inactive_players(self, pin, timeout_sec=6.0):
        with self.lock:
            room = self.rooms.get(str(pin).strip())
            if not room:
                return
            now = time.time()
            stale_ids = [
                pid
                for pid, p in room["players"].items()
                if not p.get("isBot", False) and (now - p.get("lastSeen", now)) > timeout_sec
            ]
            for pid in stale_ids:
                del room["players"][pid]

            if stale_ids and room["state"] == "QUESTION":
                total_players = len(room["players"])
                answered_count = sum(1 for p in room["players"].values() if p["currentAnswer"] is not None)
                if total_players > 0 and answered_count >= total_players:
                    self._transition_to_reveal_locked(room)

    def add_bot(self, pin):
        with self.lock:
            room = self.rooms.get(str(pin).strip())
            if not room:
                return
            bot_catalog = [
                ("Ada_9A", "🤖"),
                ("Efe_Kod", "⚡"),
                ("Zeynep_9B", "🚀"),
                ("Kerem_Veri", "🔍"),
                ("Elif_Algo", "⚙️"),
                ("Mert_Bilişim", "🦊"),
            ]
            existing_names = {p["nickname"] for p in room["players"].values()}
            avail = [b for b in bot_catalog if b[0] not in existing_names]
            name, av = avail[0] if avail else (f"Öğrenci_Bot_{len(room['players'])+1}", "🤖")
            bot_id = f"bot_{uuid.uuid4().hex[:8]}"
            room["players"][bot_id] = self.create_player(bot_id, name, av, is_bot=True)

    def start_question(self, pin, q_idx=0):
        with self.lock:
            room = self.rooms.get(str(pin).strip())
            if not room:
                return
            room["currentQuestionIndex"] = q_idx
            room["state"] = "QUESTION"
            room["questionStartTime"] = time.time() * 1000.0
            q = QUESTIONS[q_idx]
            for p in room["players"].values():
                p["currentAnswer"] = None
                if p["isBot"]:
                    p["botSimulatedDelayMs"] = random.randint(2000, 12000)
                    if random.random() < 0.72:
                        p["botSimulatedChoice"] = q["correctIndex"]
                    else:
                        wrong = [i for i in range(4) if i != q["correctIndex"]]
                        p["botSimulatedChoice"] = random.choice(wrong)

    def submit_answer(self, pin, player_id, option_index, custom_elapsed_ms=None):
        with self.lock:
            room = self.rooms.get(str(pin).strip())
            if not room or room["state"] != "QUESTION":
                return
            player = room["players"].get(player_id)
            if not player or player["currentAnswer"] is not None:
                return
            self._record_answer_locked(room, player, int(option_index), custom_elapsed_ms)
            # Check if all players have now answered -> auto-reveal!
            total_players = len(room["players"])
            answered_count = sum(1 for p in room["players"].values() if p["currentAnswer"] is not None)
            if total_players > 0 and answered_count >= total_players:
                self._transition_to_reveal_locked(room)

    def _record_answer_locked(self, room, player, idx, custom_elapsed_ms=None):
        q = QUESTIONS[room["currentQuestionIndex"]]
        now_ms = time.time() * 1000.0
        elapsed_ms = custom_elapsed_ms if custom_elapsed_ms is not None else (now_ms - room["questionStartTime"])
        elapsed_ms = min(QUESTION_DURATION_MS, max(0, int(elapsed_ms)))
        ratio = max(0.0, (QUESTION_DURATION_MS - elapsed_ms) / float(QUESTION_DURATION_MS))
        is_correct = (idx == q["correctIndex"])

        player["answeredCount"] += 1
        player["totalResponseTimeMs"] += elapsed_ms
        slot_key = q["mystery"]
        player["categoryStats"][slot_key]["total"] += 1

        speed_score = 0
        streak_bonus = 0
        total_pts = 0
        was_in_fire_mode = player["fireMode"]

        if is_correct:
            # Linear decay from 1000 down to 500
            speed_score = int(round(500 + 500 * ratio))
            # 3 consecutive correct answers trigger Alev Modu giving +20% bonus on the next question
            if was_in_fire_mode:
                streak_bonus = int(round(speed_score * 0.20))
            total_pts = speed_score + streak_bonus

            player["streak"] += 1
            if player["streak"] > player["maxStreak"]:
                player["maxStreak"] = player["streak"]
            player["fireMode"] = player["streak"] >= 3

            player["score"] += total_pts
            player["correctCount"] += 1
            player["correctResponseTimeMs"] += elapsed_ms
            player["categoryStats"][slot_key]["correct"] += 1
        else:
            player["streak"] = 0
            player["fireMode"] = False

        player["currentAnswer"] = {
            "optionIndex": idx,
            "elapsedMs": elapsed_ms,
            "elapsedSec": round(elapsed_ms / 1000.0, 2),
            "isCorrect": is_correct,
            "speedScore": speed_score,
            "streakBonus": streak_bonus,
            "pointsEarned": total_pts,
            "hadFireBonus": bool(was_in_fire_mode and is_correct),
            "timedOut": False,
        }

    def tick_room(self, pin):
        with self.lock:
            room = self.rooms.get(str(pin).strip())
            if not room or room["state"] != "QUESTION":
                return
            now_ms = time.time() * 1000.0
            elapsed_ms = now_ms - (room["questionStartTime"] or now_ms)

            for p in room["players"].values():
                if p["isBot"] and p["currentAnswer"] is None and p["botSimulatedDelayMs"] is not None:
                    if elapsed_ms >= p["botSimulatedDelayMs"]:
                        self._record_answer_locked(room, p, p["botSimulatedChoice"], p["botSimulatedDelayMs"])

            total_players = len(room["players"])
            answered_count = sum(1 for p in room["players"].values() if p["currentAnswer"] is not None)

            if elapsed_ms >= QUESTION_DURATION_MS or (total_players > 0 and answered_count >= total_players):
                self._transition_to_reveal_locked(room)

    def _transition_to_reveal_locked(self, room):
        if room["state"] == "REVEAL":
            return
        room["state"] = "REVEAL"
        q = QUESTIONS[room["currentQuestionIndex"]]
        for p in room["players"].values():
            if p["currentAnswer"] is None:
                p["streak"] = 0
                p["fireMode"] = False
                p["categoryStats"][q["mystery"]]["total"] += 1
                p["currentAnswer"] = {
                    "optionIndex": -1,
                    "elapsedMs": QUESTION_DURATION_MS,
                    "elapsedSec": QUESTION_DURATION_SEC,
                    "isCorrect": False,
                    "speedScore": 0,
                    "streakBonus": 0,
                    "pointsEarned": 0,
                    "timedOut": True,
                }

    def next_step(self, pin):
        with self.lock:
            room = self.rooms.get(str(pin).strip())
            if not room:
                return
            if room["state"] == "QUESTION":
                self._transition_to_reveal_locked(room)
            elif room["state"] == "REVEAL":
                if room["currentQuestionIndex"] >= len(QUESTIONS) - 1:
                    self._transition_to_final_locked(room)
                else:
                    room["state"] = "LEADERBOARD"
            elif room["state"] == "LEADERBOARD":
                nxt = room["currentQuestionIndex"] + 1
                if nxt < len(QUESTIONS):
                    room["currentQuestionIndex"] = nxt
                    room["state"] = "QUESTION"
                    room["questionStartTime"] = time.time() * 1000.0
                    q = QUESTIONS[nxt]
                    for p in room["players"].values():
                        p["currentAnswer"] = None
                        if p["isBot"]:
                            p["botSimulatedDelayMs"] = random.randint(2000, 12000)
                            p["botSimulatedChoice"] = q["correctIndex"] if random.random() < 0.72 else random.choice([i for i in range(4) if i != q["correctIndex"]])
                else:
                    self._transition_to_final_locked(room)

    def _transition_to_final_locked(self, room):
        room["state"] = "FINAL_PODIUM"
        players = list(room["players"].values())
        if not players:
            room["specialAwards"] = []
            return

        for p in players:
            p["badges"] = []
            io_c = p["categoryStats"]["input"]["correct"] + p["categoryStats"]["output"]["correct"]
            pr_c = p["categoryStats"]["process"]["correct"]
            avg_ms = (p["correctResponseTimeMs"] / p["correctCount"]) if p["correctCount"] > 0 else 99999

            if io_c >= 4:
                p["badges"].append({"id": "VERI_DEDEKTIFI", "title": "Veri Dedektifi", "icon": "🔍", "desc": "Girdi ve Çıktı verilerini ustalıkla çözdü!"})
            if pr_c >= 2:
                p["badges"].append({"id": "SUREC_MIMARI", "title": "Süreç Mimarı", "icon": "⚙️", "desc": "İşlem (Process) aşamalarını hatasız analiz etti!"})
            if p["correctCount"] >= 3 and avg_ms <= 8500:
                p["badges"].append({"id": "TURBO_HIZLI", "title": "Turbo Hızlı", "icon": "⚡", "desc": f"Şimşek hızında doğru yanıtlar verdi! (Ort. {avg_ms/1000.0:.1f} sn)"})
            if not p["badges"]:
                p["badges"].append({"id": "GIC_DEDEKTIFI", "title": "GİÇ Dedektifi", "icon": "🕵️", "desc": "Tüm görevleri tamamlayarak dedektiflik eğitimini bitirdi!"})

        by_io = sorted(players, key=lambda x: (-(x["categoryStats"]["input"]["correct"] + x["categoryStats"]["output"]["correct"]), -x["score"]))[0]
        by_pr = sorted(players, key=lambda x: (-x["categoryStats"]["process"]["correct"], -x["score"]))[0]
        c_players = [p for p in players if p["correctCount"] > 0]
        by_sp = sorted(c_players, key=lambda x: (x["correctResponseTimeMs"] / x["correctCount"]))[0] if c_players else players[0]

        room["specialAwards"] = [
            {"title": "Veri Dedektifi", "icon": "🔍", "subtitle": "Girdi & Çıktı Uzmanı", "winner": f"{by_io['avatar']} {by_io['nickname']}"},
            {"title": "Süreç Mimarı", "icon": "⚙️", "subtitle": "İşlem (Process) Ustası", "winner": f"{by_pr['avatar']} {by_pr['nickname']}"},
            {"title": "Turbo Hızlı", "icon": "⚡", "subtitle": "En Hızlı Dedektif", "winner": f"{by_sp['avatar']} {by_sp['nickname']}"},
        ]

    def reset_room(self, pin, keep_players=True):
        with self.lock:
            room = self.rooms.get(str(pin).strip())
            if not room:
                return
            room["state"] = "LOBBY"
            room["currentQuestionIndex"] = 0
            room["questionStartTime"] = None
            room["specialAwards"] = []
            if keep_players:
                for p in room["players"].values():
                    p["score"] = 0
                    p["streak"] = 0
                    p["maxStreak"] = 0
                    p["fireMode"] = False
                    p["correctCount"] = 0
                    p["answeredCount"] = 0
                    p["totalResponseTimeMs"] = 0
                    p["correctResponseTimeMs"] = 0
                    p["categoryStats"] = {
                        "input": {"correct": 0, "total": 0},
                        "process": {"correct": 0, "total": 0},
                        "output": {"correct": 0, "total": 0},
                    }
                    p["currentAnswer"] = None
                    p["badges"] = []
            else:
                room["players"].clear()

    def get_leaderboard(self, room):
        players = list(room["players"].values())
        players.sort(key=lambda p: (-p["score"], -p["correctCount"], p["correctResponseTimeMs"]))
        result = []
        for idx, p in enumerate(players):
            avg_s = round(p["correctResponseTimeMs"] / p["correctCount"] / 1000.0, 2) if p["correctCount"] > 0 else None
            result.append({**p, "rank": idx + 1, "avgSpeedSec": avg_s})
        return result


@st.cache_resource
def get_hub() -> GameHub:
    return GameHub()


hub = get_hub()

# ============================================================================
# GLOBAL CSS (INCLUDING THUMB-FRIENDLY COLORED PLAYER BUTTONS)
# ============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@600;700;800&display=swap');

    /* Force dark theme even if .streamlit/config.toml is not uploaded */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #070b19 !important;
        color: #f8fafc !important;
    }

    /* Make Streamlit top bar transparent & prevent it from covering top content */
    header[data-testid="stHeader"] {
        background: rgba(7, 11, 25, 0.75) !important;
        backdrop-filter: blur(8px);
    }

    .block-container {
        padding-top: 4.2rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1220px !important;
    }

    /* Dark-styled form card & inputs regardless of browser light/dark mode */
    [data-testid="stForm"] {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 24px !important;
        padding: 24px !important;
    }
    [data-testid="stForm"] label, [data-testid="stForm"] p, [data-testid="stForm"] h3 {
        color: #f8fafc !important;
    }
    .stTextInput input {
        background-color: #020617 !important;
        color: #fbbf24 !important;
        border: 2px solid #334155 !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }

    @keyframes conveyorMove {
        0% { background-position: 0 0; }
        100% { background-position: 64px 0; }
    }
    .conveyor-bar {
        height: 18px;
        border-radius: 999px;
        border: 2px solid #334155;
        background-image: repeating-linear-gradient(
            90deg,
            #0f172a 0px,
            #0f172a 24px,
            #334155 24px,
            #334155 32px
        );
        background-size: 64px 100%;
        animation: conveyorMove 1s linear infinite;
        margin-top: 12px;
    }

    @keyframes mysteryGlow {
        0%, 100% {
            box-shadow: 0 0 18px rgba(250, 204, 21, 0.55), inset 0 0 15px rgba(250, 204, 21, 0.25);
            transform: translateY(0px);
        }
        50% {
            box-shadow: 0 0 36px rgba(250, 204, 21, 0.9), 0 0 55px rgba(245, 158, 11, 0.65);
            transform: translateY(-3px);
        }
    }
    .slot-mystery {
        animation: mysteryGlow 1.4s ease-in-out infinite;
        border: 2px solid #facc15 !important;
        background: linear-gradient(180deg, rgba(250,204,21,0.14), rgba(15,23,42,0.95)) !important;
    }

    div.stButton > button {
        border-radius: 16px !important;
        font-weight: 700 !important;
        padding: 0.75rem 1.1rem !important;
        font-size: 16px !important;
    }
    div.stButton > button[kind="secondary"] {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        border-color: #fbbf24 !important;
        color: #fbbf24 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_html(raw_html: str):
    """Renders HTML cleanly in Streamlit by stripping line indentation so Markdown never treats it as a code block."""
    clean = "\n".join(line.strip() for line in raw_html.splitlines() if line.strip())
    st.markdown(clean, unsafe_allow_html=True)


def play_web_audio(effect_name: str, unique_key: str):
    js_code = f"""
    <script>
    (function() {{
      const key = "gic_snd_{unique_key}";
      if (window.sessionStorage.getItem(key)) return;
      window.sessionStorage.setItem(key, "1");
      const AudioCtx = window.parent.AudioContext || window.parent.webkitAudioContext || window.AudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      function tone(freq, type, dur, delay, gainVal) {{
        const now = ctx.currentTime + delay;
        const osc = ctx.createOscillator();
        const g = ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, now);
        g.gain.setValueAtTime(gainVal, now);
        g.gain.exponentialRampToValueAtTime(0.001, now + dur);
        osc.connect(g);
        g.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + dur);
      }}
      const eff = "{effect_name}";
      if (eff === "question") {{
        tone(392, "triangle", 0.12, 0, 0.14);
        tone(523.25, "triangle", 0.18, 0.11, 0.16);
      }} else if (eff === "correct" || eff === "reveal") {{
        tone(523.25, "triangle", 0.12, 0, 0.18);
        tone(659.25, "triangle", 0.12, 0.10, 0.18);
        tone(783.99, "triangle", 0.15, 0.20, 0.18);
        tone(1046.5, "triangle", 0.30, 0.30, 0.22);
      }} else if (eff === "wrong") {{
        tone(240, "sawtooth", 0.18, 0, 0.15);
        tone(180, "sawtooth", 0.28, 0.16, 0.18);
      }}
    }})();
    </script>
    """
    components.html(js_code, height=0)


def trigger_canvas_confetti(unique_key: str):
    js_code = f"""
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
    <script>
    (function() {{
      const key = "gic_conf_{unique_key}";
      if (window.sessionStorage.getItem(key)) return;
      window.sessionStorage.setItem(key, "1");
      if (window.confetti) {{
        window.confetti({{ particleCount: 100, spread: 80, origin: {{ y: 0.6 }} }});
      }}
    }})();
    </script>
    """
    components.html(js_code, height=0)


# ============================================================================
# SESSION STATE
# ============================================================================
if "client_id" not in st.session_state:
    st.session_state.client_id = f"st_{uuid.uuid4().hex[:10]}"

query_mode = st.query_params.get("mode", "")
query_pin = st.query_params.get("pin", "")

if "role" not in st.session_state:
    st.session_state.role = "host" if query_mode == "host" else "player"

if "host_pin" not in st.session_state:
    st.session_state.host_pin = hub.latest_pin or hub.create_room()["pin"]

if "player_pin" not in st.session_state:
    st.session_state.player_pin = query_pin if query_pin else None

if "player_joined" not in st.session_state:
    st.session_state.player_joined = False

# ============================================================================
# HEADER & ROLE SWITCHER
# Hide the Host switcher once a student is actively joined in a game (or came via ?mode=play)
# so students don't accidentally click the teacher's Host screen during class!
# ============================================================================
is_locked_student_link = (query_mode == "play") or st.session_state.player_joined

if not is_locked_student_link:
    top_col1, top_col2, top_col3 = st.columns([3, 2, 2])
    with top_col1:
        render_html(
            """
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="width:46px;height:46px;border-radius:14px;background:linear-gradient(135deg,#f59e0b,#e11d48);display:flex;align-items:center;justify-content:center;font-size:24px;">🕵️</div>
                <div>
                    <div style="font-family:'Fredoka',sans-serif;font-size:22px;font-weight:700;color:#fbbf24;line-height:1.1;">
                        GİÇ DEDEKTİFİ <span style="font-size:12px;background:rgba(34,211,238,0.15);color:#67e8f9;padding:3px 10px;border-radius:99px;border:1px solid rgba(34,211,238,0.3);vertical-align:middle;">9. Sınıf Bilgisayar Bilimi</span>
                    </div>
                    <div style="font-size:12px;color:#94a3b8;">[ GİRDİ (Input) ] ➔ [ İŞLEM (Process) ] ➔ [ ÇIKTI (Output) ]</div>
                </div>
            </div>
            """
        )
    with top_col2:
        if st.button("📱 Öğrenci Ekranı", use_container_width=True, type="primary" if st.session_state.role == "player" else "secondary"):
            st.session_state.role = "player"
            st.rerun()
    with top_col3:
        if st.button("🖥️ Akıllı Tahta (Öğretmen) Ekranı", use_container_width=True, type="primary" if st.session_state.role == "host" else "secondary"):
            st.session_state.role = "host"
            st.rerun()
    render_html("<hr style='border-color:#1e293b;margin:0.6rem 0 1.2rem 0;'>")


# ============================================================================
# HOST SCREEN (/host)
# ============================================================================
@st.fragment(run_every=1.0)
def render_host_screen():
    pin = st.session_state.host_pin
    room = hub.get_room(pin)
    if not room:
        room = hub.create_room()
        st.session_state.host_pin = room["pin"]
        pin = room["pin"]

    hub.prune_inactive_players(pin, timeout_sec=6.0)

    if room["state"] == "QUESTION":
        hub.tick_room(pin)

    leaderboard = hub.get_leaderboard(room)
    total_players = len(room["players"])
    answered_count = sum(1 for p in room["players"].values() if p["currentAnswer"] is not None)

    ctrl1, ctrl2, ctrl3, ctrl4, ctrl5 = st.columns([2.0, 1.8, 2.0, 1.6, 1.8])
    with ctrl1:
        render_html(
            f"""
            <div style="background:#0f172a;border:2px solid #f59e0b;border-radius:16px;padding:8px 16px;text-align:center;">
                <span style="font-size:11px;color:#94a3b8;font-weight:700;">4 HANELİ PIN:</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:800;color:#fbbf24;margin-left:8px;letter-spacing:4px;">{pin}</span>
            </div>
            """
        )
    with ctrl2:
        render_html(
            f"""
            <div style="background:#0f172a;border:1px solid #334155;border-radius:16px;padding:8px 16px;text-align:center;">
                <span style="font-size:18px;">🎓</span>
                <span style="font-size:20px;font-weight:800;color:#34d399;margin:0 6px;">{total_players}</span>
                <span style="font-size:12px;color:#cbd5e1;font-weight:600;">Aktif</span>
            </div>
            """
        )
    with ctrl3:
        if st.button("🤖 + Örnek Öğrenci", use_container_width=True, disabled=(room["state"] != "LOBBY")):
            hub.add_bot(pin)
            st.rerun()
    with ctrl4:
        if st.button("↺ Lobiye Dön", use_container_width=True):
            hub.reset_room(pin, keep_players=True)
            st.rerun()
    with ctrl5:
        if st.button("🗑️ Odayı Temizle", use_container_width=True):
            hub.reset_room(pin, keep_players=False)
            st.rerun()

    st.write("")

    if room["state"] == "LOBBY":
        left_col, right_col = st.columns([5, 7])
        with left_col:
            render_html(
                f"""
                <div style="background:#0f172a;border:2px solid rgba(251,191,36,0.5);border-radius:24px;padding:24px;text-align:center;">
                    <div style="font-size:12px;font-weight:800;color:#fbbf24;letter-spacing:2px;text-transform:uppercase;">4 HANELİ OYUN PIN KODU</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:64px;font-weight:800;color:#fbbf24;letter-spacing:8px;margin:4px 0;">{pin}</div>
                </div>
                """
            )
            components.html(
                f"""
                <div style="background:#0f172a;border:1px solid #1e293b;border-radius:20px;padding:14px;display:flex;align-items:center;gap:16px;color:#f8fafc;font-family:sans-serif;margin-top:10px;">
                    <div id="qrbox" style="background:white;padding:10px;border-radius:14px;width:128px;height:128px;display:flex;align-items:center;justify-content:center;flex-shrink:0;"></div>
                    <div style="flex:1;min-width:0;">
                        <div style="font-weight:800;font-size:14px;color:#38bdf8;margin-bottom:6px;">📱 Öğrenci Katılım Linki & QR</div>
                        <div id="urltext" style="font-family:monospace;font-size:11px;color:#fbbf24;word-break:break-all;background:#020617;padding:6px 10px;border-radius:8px;border:1px solid #334155;margin-bottom:8px;"></div>
                        <button id="copyBtn" onclick="copyLink()" style="background:#f59e0b;color:#0f172a;border:none;padding:6px 12px;border-radius:8px;font-weight:800;font-size:12px;cursor:pointer;">📋 Öğrenci Linkini Kopyala</button>
                    </div>
                </div>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
                <script>
                let joinUrl = "";
                (function() {{
                    let baseUrl = window.location.origin;
                    try {{ baseUrl = window.parent.location.origin + window.parent.location.pathname; }} catch(e) {{}}
                    joinUrl = baseUrl.replace(/\\/$/, "") + "?mode=play&pin={pin}";
                    document.getElementById("urltext").textContent = joinUrl;
                    if (window.QRCode) {{
                        new QRCode(document.getElementById("qrbox"), {{
                            text: joinUrl,
                            width: 112,
                            height: 112,
                            colorDark: "#0f172a",
                            colorLight: "#ffffff"
                        }});
                    }}
                }})();
                function copyLink() {{
                    navigator.clipboard.writeText(joinUrl).then(() => {{
                        const b = document.getElementById("copyBtn");
                        b.textContent = "✓ Link Kopyalandı!";
                        setTimeout(() => {{ b.textContent = "📋 Öğrenci Linkini Kopyala"; }}, 1800);
                    }});
                }}
                </script>
                """,
                height=190,
            )

        with right_col:
            st.markdown("### 🎓 Katılan Öğrenciler")
            if not leaderboard:
                st.info("📡 Öğrencilerin katılması bekleniyor... Öğrenciler kendi bilgisayarlarından linke tıklayıp 4 haneli PIN ile katıldığında burada görünecek.")
            else:
                cols = st.columns(3)
                for idx, p in enumerate(leaderboard):
                    with cols[idx % 3]:
                        render_html(
                            f"""
                            <div style="background:#020617;border:1px solid #334155;border-radius:14px;padding:10px 12px;margin-bottom:8px;display:flex;align-items:center;gap:10px;">
                                <span style="font-size:22px;">{p['avatar']}</span>
                                <div style="font-weight:700;font-size:14px;color:white;">{p['nickname']}</div>
                            </div>
                            """
                        )
            st.write("")
            if st.button("🚀 Oyunu Başlat", type="primary", use_container_width=True):
                hub.start_question(pin, 0)
                st.rerun()

    elif room["state"] in ("QUESTION", "REVEAL"):
        q_idx = room["currentQuestionIndex"]
        q = QUESTIONS[q_idx]
        is_reveal = (room["state"] == "REVEAL")

        now_ms = time.time() * 1000.0
        elapsed_ms = (now_ms - room["questionStartTime"]) if room["questionStartTime"] else 0
        rem_ms = 0 if is_reveal else max(0, int(QUESTION_DURATION_MS - elapsed_ms))
        rem_sec = int(math.ceil(rem_ms / 1000.0))
        ratio = max(0.0, min(1.0, rem_ms / float(QUESTION_DURATION_MS)))
        dash_offset = round(169.65 * (1.0 - ratio), 2)

        play_web_audio("reveal" if is_reveal else "question", f"st_{room['state']}_{pin}_{q_idx}")

        h_col1, h_col2 = st.columns([4.2, 1.3])
        with h_col1:
            stroke_col = "#f43f5e" if (rem_sec <= 5 and not is_reveal) else "#10b981"
            render_html(
                f"""
                <div style="background:#0f172a;border:1px solid #1e293b;border-radius:20px;padding:14px 20px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="background:rgba(245,158,11,0.2);color:#fbbf24;padding:3px 10px;border-radius:99px;font-size:12px;font-weight:800;">Görev {q_idx+1} / {len(QUESTIONS)}</span>
                        <span style="background:rgba(56,189,248,0.15);color:#38bdf8;padding:3px 10px;border-radius:99px;font-size:12px;font-weight:700;margin-left:6px;">Tema: {q['theme']}</span>
                        <div style="font-family:'Fredoka',sans-serif;font-size:26px;font-weight:700;color:white;margin-top:4px;">{q['title']}</div>
                    </div>
                    <div style="display:flex;align-items:center;gap:16px;">
                        <div style="background:#020617;border:1px solid #334155;border-radius:14px;padding:8px 14px;font-family:monospace;font-size:18px;font-weight:800;color:#38bdf8;">
                            {answered_count}/{total_players} cevap verdi
                        </div>
                        <div style="position:relative;width:64px;height:64px;display:flex;align-items:center;justify-content:center;">
                            <svg width="64" height="64" viewBox="0 0 64 64" style="transform:rotate(-90deg);">
                                <circle cx="32" cy="32" r="27" stroke="#1e293b" stroke-width="6" fill="transparent"/>
                                <circle cx="32" cy="32" r="27" stroke="{stroke_col}" stroke-width="6" stroke-linecap="round" fill="transparent" stroke-dasharray="169.65" stroke-dashoffset="{dash_offset}"/>
                            </svg>
                            <span style="position:absolute;font-family:monospace;font-size:20px;font-weight:800;color:{stroke_col};">{rem_sec}</span>
                        </div>
                    </div>
                </div>
                """
            )

        with h_col2:
            btn_lbl = "Cevabı Aç ➔" if not is_reveal else ("Final Podyumu ➔" if q_idx >= len(QUESTIONS) - 1 else "Liderlik Tablosu ➔")
            if st.button(btn_lbl, type="primary", use_container_width=True):
                hub.next_step(pin)
                st.rerun()

        unlocked_text = q["options"][q["correctIndex"]]

        def render_stage_html(stage_key, label_txt, color_hex, raw_val):
            is_mys = (q["mystery"] == stage_key)
            if is_mys and not is_reveal:
                return f"""
                <div class="slot-mystery" style="border-radius:20px;padding:18px;min-height:135px;text-align:center;display:flex;flex-direction:column;justify-content:space-between;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-weight:800;font-size:13px;color:#fde047;">{label_txt}</span>
                        <span style="font-size:11px;font-weight:800;color:#facc15;">🔒 KİLİTLİ</span>
                    </div>
                    <div style="margin:10px 0;">
                        <span style="display:inline-block;padding:8px 18px;border-radius:14px;border:2px solid #facc15;background:rgba(250,204,21,0.25);font-size:26px;font-weight:900;color:#fde047;">🔒 ?</span>
                    </div>
                </div>
                """
            val_shown = f"✓ {unlocked_text}" if (is_mys and is_reveal) else raw_val
            border_c = "#10b981" if (is_mys and is_reveal) else color_hex
            bg_c = "rgba(6, 78, 59, 0.5)" if (is_mys and is_reveal) else "#020617"
            status_txt = "🔓 AÇILDI ✓" if (is_mys and is_reveal) else ""
            return f"""
            <div style="background:{bg_c};border:2px solid {border_c};border-radius:20px;padding:18px;min-height:135px;display:flex;flex-direction:column;justify-content:space-between;text-align:center;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-weight:800;font-size:13px;color:{color_hex};">{label_txt}</span>
                    <span style="font-size:11px;font-weight:800;color:#34d399;">{status_txt}</span>
                </div>
                <div style="font-size:17px;font-weight:700;color:white;margin:auto 0;">{val_shown}</div>
            </div>
            """

        render_html(
            f"""
            <div style="background:#0f172a;border:1px solid #1e293b;border-radius:24px;padding:20px;margin-top:12px;">
                <div style="display:grid;grid-template-columns:1fr auto 1fr auto 1fr;gap:12px;align-items:center;">
                    {render_stage_html("input", "[ GİRDİ (Input) ]", "#38bdf8", q["input"])}
                    <div style="font-size:26px;color:#fbbf24;font-weight:900;">➔</div>
                    {render_stage_html("process", "[ İŞLEM (Process) ]", "#c084fc", q["process"])}
                    <div style="font-size:26px;color:#fbbf24;font-weight:900;">➔</div>
                    {render_stage_html("output", "[ ÇIKTI (Output) ]", "#34d399", q["output"])}
                </div>
                <div class="conveyor-bar"></div>
                <div style="text-align:center;font-family:'Fredoka',sans-serif;font-size:22px;font-weight:700;color:#fcd34d;margin-top:12px;">
                    {q['question']}
                </div>
            </div>
            """
        )

        opt_counts = [0, 0, 0, 0]
        for p in room["players"].values():
            if p["currentAnswer"] and 0 <= p["currentAnswer"]["optionIndex"] < 4:
                opt_counts[p["currentAnswer"]["optionIndex"]] += 1

        c_left, c_right = st.columns(2)
        for idx, opt_text in enumerate(q["options"]):
            meta = OPTION_META[idx]
            target_col = c_left if idx % 2 == 0 else c_right
            is_correct_opt = is_reveal and (idx == q["correctIndex"])
            bg_col = "#059669" if is_correct_opt else meta["hex"]
            opacity = "0.45" if (is_reveal and not is_correct_opt) else "1.0"
            ring = "3px solid #6ee7b7" if is_correct_opt else f"2px solid {meta['border']}"
            vote_badge = f"<span style='background:#020617;padding:4px 10px;border-radius:10px;font-family:monospace;font-size:13px;'>{opt_counts[idx]} kişi {'✓' if is_correct_opt else ''}</span>" if is_reveal else ""

            with target_col:
                render_html(
                    f"""
                    <div style="background:{bg_col};border:{ring};opacity:{opacity};border-radius:18px;padding:16px 18px;margin-top:10px;display:flex;align-items:center;justify-content:space-between;gap:14px;color:white;font-weight:700;font-size:16px;">
                        <span>{meta['label']} — {opt_text}</span>
                        {vote_badge}
                    </div>
                    """
                )

        # Reveal Mode Answer Distribution Bar Chart
        if is_reveal:
            total_votes = max(1, sum(opt_counts))
            bars_html = ""
            for idx, cnt in enumerate(opt_counts):
                meta = OPTION_META[idx]
                is_corr = (idx == q["correctIndex"])
                h_pct = max(14, int(round((cnt / total_votes) * 100)))
                bars_html += f"""
                <div style="display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:110px;">
                    <div style="font-family:monospace;font-size:12px;font-weight:800;color:white;margin-bottom:4px;">{cnt} {'✓' if is_corr else ''}</div>
                    <div style="width:56px;height:{h_pct}%;background:{meta['hex']};border-radius:10px 10px 0 0;border:{'2px solid white' if is_corr else 'none'};"></div>
                    <div style="font-size:12px;font-weight:700;color:#cbd5e1;margin-top:6px;">{meta['label']}</div>
                </div>
                """
            render_html(
                f"""
                <div style="background:#0f172a;border:1px solid #1e293b;border-radius:20px;padding:16px 20px;margin-top:14px;">
                    <div style="font-weight:800;font-size:15px;color:white;margin-bottom:10px;">📊 Sınıf Cevap Dağılım Grafiği</div>
                    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;background:#020617;padding:14px;border-radius:14px;border:1px solid #1e293b;">
                        {bars_html}
                    </div>
                </div>
                """
            )

    elif room["state"] == "LEADERBOARD":
        top1, top2 = st.columns([4, 1.5])
        with top1:
            st.markdown(f"### 🏆 Görev {room['currentQuestionIndex'] + 1} Sonrası Liderlik Tablosu (İlk 5)")
        with top2:
            if st.button("Sonraki Soru ➔", type="primary", use_container_width=True):
                hub.next_step(pin)
                st.rerun()

        medals = ["🥇", "🥈", "🥉", "4.", "5."]
        for idx, p in enumerate(leaderboard[:5]):
            fire_html = (
                f"<span style='background:linear-gradient(90deg,#ea580c,#e11d48);color:white;padding:3px 10px;border-radius:99px;font-size:12px;font-weight:800;margin-left:8px;'>🔥 {p['streak']}x Seri</span>"
                if p["fireMode"]
                else ""
            )
            render_html(
                f"""
                <div style="background:#0f172a;border:2px solid {'#f97316' if p['fireMode'] else '#334155'};border-radius:18px;padding:14px 20px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;">
                    <div style="display:flex;align-items:center;gap:14px;">
                        <span style="font-size:24px;font-weight:800;">{medals[idx]}</span>
                        <span style="font-size:26px;">{p['avatar']}</span>
                        <div>
                            <span style="font-size:18px;font-weight:800;color:white;">{p['nickname']}</span>
                            {fire_html}
                        </div>
                    </div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:24px;font-weight:800;color:#fbbf24;">
                        {p['score']} PUAN
                    </div>
                </div>
                """
            )

    elif room["state"] == "FINAL_PODIUM":
        trigger_canvas_confetti(f"host_final_{pin}")
        st.markdown("## 🏆 GİÇ Dedektifi Final Podyumu")
        p_cols = st.columns(3)
        podium_order = [
            (1, "🥈 2. İKİNCİ", "#94a3b8"),
            (0, "👑 🥇 1. ŞAMPİYON", "#fbbf24"),
            (2, "🥉 3. ÜÇÜNCÜ", "#d97706"),
        ]
        for col_idx, (rank_idx, label, border_col) in enumerate(podium_order):
            with p_cols[col_idx]:
                if rank_idx < len(leaderboard):
                    pl = leaderboard[rank_idx]
                    render_html(
                        f"""
                        <div style="background:#0f172a;border:3px solid {border_col};border-radius:24px;padding:22px;text-align:center;">
                            <div style="font-size:14px;font-weight:800;color:{border_col};">{label}</div>
                            <div style="font-size:44px;margin:8px 0;">{pl['avatar']}</div>
                            <div style="font-size:22px;font-weight:800;color:white;">{pl['nickname']}</div>
                            <div style="font-family:'JetBrains Mono',monospace;font-size:28px;font-weight:800;color:#fbbf24;margin-top:8px;">{pl['score']} P</div>
                        </div>
                        """
                    )

        st.write("")
        st.markdown("### 🎖️ Özel Dedektif Rozetleri")
        b_cols = st.columns(3)
        for idx, aw in enumerate(room.get("specialAwards", [])):
            with b_cols[idx % 3]:
                render_html(
                    f"""
                    <div style="background:#020617;border:1px solid rgba(251,191,36,0.4);border-radius:18px;padding:16px;display:flex;align-items:center;gap:14px;">
                        <div style="font-size:34px;">{aw['icon']}</div>
                        <div>
                            <div style="font-size:11px;color:#fbbf24;font-weight:800;">{aw['subtitle']}</div>
                            <div style="font-size:17px;font-weight:800;color:white;">{aw['title']}</div>
                            <div style="font-size:14px;font-weight:700;color:#38bdf8;margin-top:2px;">{aw['winner']}</div>
                        </div>
                    </div>
                    """
                )


# ============================================================================
# STUDENT / PLAYER SCREEN (/play)
# ============================================================================
@st.fragment(run_every=1.0)
def render_player_screen():
    if not st.session_state.player_joined or not st.session_state.player_pin:
        default_pin = query_pin or hub.latest_pin or ""
        with st.form("player_join_form"):
            st.markdown("### 🕵️ GİÇ Dedektifi — Oyuna Katıl")
            pin_val = st.text_input("4 Haneli Oyun PIN Kodu", value=default_pin, max_chars=4)
            nick_val = st.text_input("Takma Adın (Nickname)", placeholder="Adın veya Takma Adın", max_chars=16)
            submitted = st.form_submit_button("🚀 Katıl", type="primary", use_container_width=True)

            if submitted:
                player_obj, err = hub.join_player(pin_val, st.session_state.client_id, nick_val)
                if err:
                    st.error(err)
                else:
                    st.session_state.player_pin = str(pin_val).strip()
                    st.session_state.player_joined = True
                    st.rerun()
        return

    pin = st.session_state.player_pin
    room = hub.get_room(pin)
    if not room or st.session_state.client_id not in room["players"]:
        st.session_state.player_joined = False
        st.rerun()
        return

    hub.heartbeat_player(pin, st.session_state.client_id)
    hub.prune_inactive_players(pin, timeout_sec=6.0)

    if room["state"] == "QUESTION":
        hub.tick_room(pin)

    player = room["players"][st.session_state.client_id]
    leaderboard = hub.get_leaderboard(room)
    my_rank = next((item["rank"] for item in leaderboard if item["id"] == player["id"]), 1)

    # Top Student Status Bar
    streak_badge_html = (
        f"<span style='background:#ea580c;color:white;padding:3px 10px;border-radius:99px;font-size:12px;font-weight:800;'>🔥 {player['streak']}x Seri</span>"
        if player["fireMode"]
        else ""
    )
    st_bar_col1, st_bar_col2 = st.columns([5.2, 1.3])
    with st_bar_col1:
        render_html(
            f"""
            <div style="background:#0f172a;border:1px solid #334155;border-radius:16px;padding:10px 16px;margin-bottom:14px;display:flex;justify-content:space-between;align-items:center;">
                <div style="font-weight:800;font-size:15px;color:white;">🕵️ {player['nickname']} <span style="font-size:11px;color:#94a3b8;margin-left:6px;">(PIN: {pin})</span></div>
                <div style="display:flex;gap:10px;align-items:center;">
                    {streak_badge_html}
                    <span style="background:#020617;border:1px solid #334155;color:#38bdf8;padding:3px 10px;border-radius:10px;font-family:monospace;font-weight:800;">#{my_rank}</span>
                    <span style="background:rgba(245,158,11,0.2);border:1px solid rgba(245,158,11,0.4);color:#fbbf24;padding:3px 12px;border-radius:10px;font-family:monospace;font-weight:800;">{player['score']} P</span>
                </div>
            </div>
            """
        )
    with st_bar_col2:
        if st.button("🚪 Çıkış", use_container_width=True):
            hub.leave_player(pin, st.session_state.client_id)
            st.session_state.player_joined = False
            st.rerun()

    if room["state"] == "LOBBY":
        render_html(
            f"""
            <div style="background:#0f172a;border:2px solid #10b981;border-radius:24px;padding:28px;text-align:center;">
                <div style="font-size:48px;margin-bottom:8px;">🕵️</div>
                <div style="font-family:'Fredoka',sans-serif;font-size:24px;font-weight:700;color:white;">Hoş Geldin, {player['nickname']}!</div>
                <div style="font-size:16px;color:#fbbf24;font-weight:700;margin-top:8px;">Öğretmenin oyunu başlatması bekleniyor...</div>
            </div>
            """
        )

    elif room["state"] == "QUESTION":
        q_idx = room["currentQuestionIndex"]
        q = QUESTIONS[q_idx]
        now_ms = time.time() * 1000.0
        rem_sec = max(0, int(math.ceil((QUESTION_DURATION_MS - (now_ms - room["questionStartTime"])) / 1000.0)))

        if player["fireMode"]:
            render_html(
                "<div style='background:linear-gradient(90deg,#ea580c,#e11d48);color:white;padding:8px 14px;border-radius:12px;font-weight:800;text-align:center;margin-bottom:10px;'>🔥 Alev Modu Aktif! (Bu soruda +%20 Puan Bonusu!)</div>"
            )

        render_html(
            f"""
            <div style="background:#0f172a;border:1px solid #334155;border-radius:18px;padding:14px 18px;margin-bottom:14px;display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:12px;font-weight:800;color:#fbbf24;">Görev {q_idx+1} / {len(QUESTIONS)}</div>
                    <div style="font-size:20px;font-weight:800;color:white;">{q['title']}</div>
                    <div style="font-size:13px;color:#cbd5e1;margin-top:2px;">{q['question']}</div>
                </div>
                <div style="font-family:monospace;font-size:22px;font-weight:800;color:#34d399;">⏱️ {rem_sec}s</div>
            </div>
            """
        )

        if player["currentAnswer"] is not None:
            render_html(
                """
                <div style="background:#0f172a;border:2px solid #38bdf8;border-radius:22px;padding:28px;text-align:center;">
                    <div style="font-size:40px;margin-bottom:6px;">⏳</div>
                    <div style="font-family:'Fredoka',sans-serif;font-size:22px;font-weight:700;color:white;">Cevabın Alındı! Bekleniyor...</div>
                </div>
                """
            )
        else:
            b_col1, b_col2 = st.columns(2)
            for idx, opt_text in enumerate(q["options"]):
                meta = OPTION_META[idx]
                target = b_col1 if idx % 2 == 0 else b_col2
                with target:
                    render_html(
                        f"<div style='background:{meta['hex']};color:white;padding:8px 14px;border-radius:14px 14px 0 0;font-weight:800;font-size:14px;'>{meta['label']}</div>"
                    )
                    if st.button(f"{opt_text}", key=f"ans_{q_idx}_{idx}", use_container_width=True):
                        hub.submit_answer(pin, st.session_state.client_id, idx)
                        st.rerun()

    elif room["state"] in ("REVEAL", "LEADERBOARD"):
        q = QUESTIONS[room["currentQuestionIndex"]]
        ans = player["currentAnswer"] or {"isCorrect": False, "pointsEarned": 0}
        if ans["isCorrect"]:
            play_web_audio("correct", f"p_rev_{pin}_{q['id']}")
            render_html(
                f"""
                <div style="background:linear-gradient(180deg,rgba(6,95,70,0.92),#0f172a);border:2px solid #10b981;border-radius:24px;padding:26px;text-align:center;">
                    <div style="font-size:48px;">✅</div>
                    <div style="font-family:'Fredoka',sans-serif;font-size:28px;font-weight:700;color:white;">Tebrikler! +{ans['pointsEarned']} Puan</div>
                    <div style="font-size:14px;color:#d1fae5;margin-top:8px;">Sıralaman: <b>#{my_rank}</b> • Toplam Puanın: <b>{player['score']}</b></div>
                </div>
                """
            )
        else:
            play_web_audio("wrong", f"p_rev_{pin}_{q['id']}")
            render_html(
                f"""
                <div style="background:linear-gradient(180deg,rgba(136,19,55,0.92),#0f172a);border:2px solid #f43f5e;border-radius:24px;padding:26px;text-align:center;">
                    <div style="font-size:48px;">❌</div>
                    <div style="font-family:'Fredoka',sans-serif;font-size:28px;font-weight:700;color:white;">Yanlış Cevap</div>
                    <div style="font-size:13px;color:#fecdd3;margin-top:6px;">Doğru Cevap: <b>{q['options'][q['correctIndex']]}</b></div>
                    <div style="font-size:14px;color:#f8fafc;margin-top:8px;">Sıralaman: <b>#{my_rank}</b> • Toplam Puanın: <b>{player['score']}</b></div>
                </div>
                """
            )

    elif room["state"] == "FINAL_PODIUM":
        trigger_canvas_confetti(f"p_final_{pin}")
        render_html(
            f"""
            <div style="background:#0f172a;border:2px solid #fbbf24;border-radius:24px;padding:24px;text-align:center;">
                <div style="font-size:52px;">🏆</div>
                <div style="font-family:'Fredoka',sans-serif;font-size:28px;font-weight:700;color:white;">Sıralaman: #{my_rank}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:32px;font-weight:800;color:#fbbf24;margin:6px 0;">{player['score']} Puan</div>
            </div>
            """
        )
        st.write("")
        for b in player.get("badges", []):
            st.info(f"{b['icon']} **{b['title']}**: {b['desc']}")


if st.session_state.role == "host":
    render_host_screen()
else:
    render_player_screen()
