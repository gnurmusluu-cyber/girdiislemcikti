#!/usr/bin/env python3
"""
GİÇ Dedektifi (Input-Process-Output Game)
9. Sınıf Bilgisayar Bilimi Dersi - Gerçek Zamanlı Çok Oyunculu Eğitim Uygulaması
Mirrors server.js protocol 1:1 on port 3000.
"""

import json
import math
import os
import random
import socket
import time
import uuid
import tornado.ioloop
import tornado.web
import tornado.websocket

PORT = int(os.environ.get("PORT", 3000))
PUBLIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
QUESTION_DURATION_SEC = 20
QUESTION_DURATION_MS = QUESTION_DURATION_SEC * 1000

# ============================================================================
# QUESTION DATASET (Embed directly into the backend)
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

rooms = {}
clients = {}
latest_active_pin = None


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"


def generate_pin():
    while True:
        pin = str(random.randint(1000, 9999))
        if pin not in rooms:
            return pin


def create_room(requested_pin=None):
    global latest_active_pin
    if requested_pin and len(str(requested_pin)) == 4 and str(requested_pin).isdigit():
        pin = str(requested_pin)
    else:
        pin = generate_pin()

    room = {
        "pin": pin,
        "state": "LOBBY",
        "hostClientId": None,
        "currentQuestionIndex": 0,
        "questionStartTime": None,
        "remainingSeconds": QUESTION_DURATION_SEC,
        "timerCallback": None,
        "botTimeouts": [],
        "players": {},
        "specialAwards": [],
        "createdAt": time.time() * 1000
    }
    rooms[pin] = room
    latest_active_pin = pin
    return room


def create_player_obj(player_id, nickname, avatar="🕵️", is_bot=False):
    return {
        "id": player_id,
        "nickname": nickname.strip()[:18],
        "avatar": avatar or "🕵️",
        "isBot": is_bot,
        "connected": True,
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
            "output": {"correct": 0, "total": 0}
        },
        "currentAnswer": None,
        "badges": []
    }


def clear_room_timers(room):
    loop = tornado.ioloop.IOLoop.current()
    if room.get("timerCallback"):
        room["timerCallback"].stop()
        room["timerCallback"] = None
    for t in room.get("botTimeouts", []):
        try:
            loop.remove_timeout(t)
        except Exception:
            pass
    room["botTimeouts"] = []


def get_sorted_leaderboard(room):
    players = list(room["players"].values())
    players.sort(key=lambda p: (-p["score"], -p["correctCount"], p["correctResponseTimeMs"]))
    result = []
    for idx, p in enumerate(players):
        avg_speed = round(p["correctResponseTimeMs"] / p["correctCount"] / 1000.0, 2) if p["correctCount"] > 0 else None
        result.append({
            "id": p["id"],
            "rank": idx + 1,
            "nickname": p["nickname"],
            "avatar": p["avatar"],
            "isBot": p["isBot"],
            "score": p["score"],
            "streak": p["streak"],
            "maxStreak": p["maxStreak"],
            "fireMode": p["fireMode"],
            "correctCount": p["correctCount"],
            "answeredCount": p["answeredCount"],
            "avgSpeedSec": avg_speed,
            "badges": p.get("badges", [])
        })
    return result


def compute_end_game_badges(room):
    players = list(room["players"].values())
    if not players:
        return []

    for p in players:
        p["badges"] = []
        io_correct = p["categoryStats"]["input"]["correct"] + p["categoryStats"]["output"]["correct"]
        proc_correct = p["categoryStats"]["process"]["correct"]
        avg_ms = (p["correctResponseTimeMs"] / p["correctCount"]) if p["correctCount"] > 0 else 99999

        if io_correct >= 4:
            p["badges"].append({
                "id": "VERI_DEDEKTIFI",
                "title": "Veri Dedektifi",
                "icon": "🔍",
                "desc": "Girdi ve Çıktı verilerini ustalıkla çözdü!"
            })
        if proc_correct >= 2:
            p["badges"].append({
                "id": "SUREC_MIMARI",
                "title": "Süreç Mimarı",
                "icon": "⚙️",
                "desc": "İşlem (Process) aşamalarını hatasız analiz etti!"
            })
        if p["correctCount"] >= 3 and avg_ms <= 8500:
            p["badges"].append({
                "id": "TURBO_HIZLI",
                "title": "Turbo Hızlı",
                "icon": "⚡",
                "desc": f"Şimşek hızında doğru yanıtlar verdi! (Ort. {avg_ms / 1000.0:.1f} sn)"
            })
        if not p["badges"]:
            p["badges"].append({
                "id": "GIC_DEDEKTIFI",
                "title": "GİÇ Dedektifi",
                "icon": "🕵️",
                "desc": "Tüm görevleri tamamlayarak dedektiflik eğitimini bitirdi!"
            })

    by_io = sorted(
        players,
        key=lambda x: (-(x["categoryStats"]["input"]["correct"] + x["categoryStats"]["output"]["correct"]), -x["score"])
    )[0]
    by_proc = sorted(
        players,
        key=lambda x: (-x["categoryStats"]["process"]["correct"], -x["score"])
    )[0]
    correct_players = [p for p in players if p["correctCount"] > 0]
    by_speed = sorted(
        correct_players,
        key=lambda x: (x["correctResponseTimeMs"] / x["correctCount"])
    )[0] if correct_players else players[0]

    return [
        {
            "id": "VERI_DEDEKTIFI",
            "title": "Veri Dedektifi",
            "icon": "🔍",
            "subtitle": "Girdi & Çıktı Uzmanı",
            "winner": {
                "nickname": by_io["nickname"],
                "avatar": by_io["avatar"],
                "stat": f"{by_io['categoryStats']['input']['correct'] + by_io['categoryStats']['output']['correct']} Doğru"
            }
        },
        {
            "id": "SUREC_MIMARI",
            "title": "Süreç Mimarı",
            "icon": "⚙️",
            "subtitle": "İşlem (Process) Ustası",
            "winner": {
                "nickname": by_proc["nickname"],
                "avatar": by_proc["avatar"],
                "stat": f"{by_proc['categoryStats']['process']['correct']} Doğru"
            }
        },
        {
            "id": "TURBO_HIZLI",
            "title": "Turbo Hızlı",
            "icon": "⚡",
            "subtitle": "En Hızlı Dedektif",
            "winner": {
                "nickname": by_speed["nickname"],
                "avatar": by_speed["avatar"],
                "stat": f"{by_speed['correctResponseTimeMs'] / by_speed['correctCount'] / 1000.0:.2f} sn ort." if by_speed["correctCount"] > 0 else f"{by_speed['score']} Puan"
            }
        }
    ]


def build_host_state_payload(room):
    q = QUESTIONS[room["currentQuestionIndex"]] if room["currentQuestionIndex"] < len(QUESTIONS) else QUESTIONS[0]
    leaderboard = get_sorted_leaderboard(room)
    total_players = len(room["players"])
    answered_count = 0
    option_counts = [0, 0, 0, 0]

    for p in room["players"].values():
        if p["currentAnswer"] is not None:
            answered_count += 1
            opt_idx = p["currentAnswer"]["optionIndex"]
            if 0 <= opt_idx < 4:
                option_counts[opt_idx] += 1

    is_reveal_or_later = room["state"] in ("REVEAL", "LEADERBOARD", "FINAL_PODIUM")
    unlocked_ans = q["options"][q["correctIndex"]]

    stages = {
        "input": (unlocked_ans if is_reveal_or_later else "?") if q["mystery"] == "input" else q["input"],
        "process": (unlocked_ans if is_reveal_or_later else "?") if q["mystery"] == "process" else q["process"],
        "output": (unlocked_ans if is_reveal_or_later else "?") if q["mystery"] == "output" else q["output"]
    }

    return {
        "pin": room["pin"],
        "lanIp": get_local_ip(),
        "port": PORT,
        "state": room["state"],
        "questionIndex": room["currentQuestionIndex"],
        "totalQuestions": len(QUESTIONS),
        "remainingSeconds": room["remainingSeconds"],
        "totalSeconds": QUESTION_DURATION_SEC,
        "totalPlayers": total_players,
        "answeredCount": answered_count,
        "players": leaderboard,
        "top5": leaderboard[:5],
        "question": {
            "id": q["id"],
            "title": q["title"],
            "theme": q["theme"],
            "mystery": q["mystery"],
            "question": q["question"],
            "stages": stages,
            "options": q["options"],
            "correctIndex": q["correctIndex"] if is_reveal_or_later else None,
            "optionCounts": option_counts if is_reveal_or_later else None
        },
        "specialAwards": room.get("specialAwards", []) if room["state"] == "FINAL_PODIUM" else []
    }


def build_player_state_payload(room, player):
    q = QUESTIONS[room["currentQuestionIndex"]] if room["currentQuestionIndex"] < len(QUESTIONS) else QUESTIONS[0]
    leaderboard = get_sorted_leaderboard(room)
    rank = len(leaderboard)
    for item in leaderboard:
        if item["id"] == player["id"]:
            rank = item["rank"]
            break
    is_reveal_or_later = room["state"] in ("REVEAL", "LEADERBOARD", "FINAL_PODIUM")

    return {
        "pin": room["pin"],
        "state": room["state"],
        "questionIndex": room["currentQuestionIndex"],
        "totalQuestions": len(QUESTIONS),
        "remainingSeconds": room["remainingSeconds"],
        "totalSeconds": QUESTION_DURATION_SEC,
        "player": {
            "id": player["id"],
            "nickname": player["nickname"],
            "avatar": player["avatar"],
            "score": player["score"],
            "streak": player["streak"],
            "maxStreak": player["maxStreak"],
            "fireMode": player["fireMode"],
            "rank": rank,
            "totalPlayers": len(room["players"]),
            "correctCount": player["correctCount"],
            "answeredCount": player["answeredCount"],
            "badges": player.get("badges", []),
            "currentAnswer": player["currentAnswer"]
        },
        "question": {
            "id": q["id"],
            "title": q["title"],
            "theme": q["theme"],
            "mystery": q["mystery"],
            "question": q["question"],
            "options": q["options"],
            "correctIndex": q["correctIndex"] if is_reveal_or_later else None,
            "correctOptionText": q["options"][q["correctIndex"]] if is_reveal_or_later else None
        },
        "top3": leaderboard[:3] if room["state"] == "FINAL_PODIUM" else [],
        "top5": leaderboard[:5] if room["state"] in ("LEADERBOARD", "FINAL_PODIUM") else []
    }


def emit_to_client(client_id, event, data):
    c = clients.get(client_id)
    if c and c.get("ws"):
        try:
            c["ws"].write_message(json.dumps({"event": event, "data": data}))
        except Exception:
            pass


def broadcast_room_state(room):
    if not room:
        return
    if room.get("hostClientId"):
        emit_to_client(room["hostClientId"], "game:state_update", build_host_state_payload(room))
    for p in room["players"].values():
        if not p["isBot"]:
            emit_to_client(p["id"], "player:state_update", build_player_state_payload(room, p))


def broadcast_timer_tick(room):
    if not room:
        return
    now_ms = time.time() * 1000
    elapsed = (now_ms - room["questionStartTime"]) if room.get("questionStartTime") else 0
    remaining_ms = max(0, int(QUESTION_DURATION_MS - elapsed))
    room["remainingSeconds"] = int(math.ceil(remaining_ms / 1000.0))
    payload = {
        "remainingSeconds": room["remainingSeconds"],
        "remainingMs": remaining_ms,
        "totalSeconds": QUESTION_DURATION_SEC
    }
    if room.get("hostClientId"):
        emit_to_client(room["hostClientId"], "game:timer_tick", payload)
    for p in room["players"].values():
        if not p["isBot"]:
            emit_to_client(p["id"], "game:timer_tick", payload)

    if remaining_ms <= 0:
        transition_to_reveal(room)


def start_question(room, question_index):
    clear_room_timers(room)
    room["currentQuestionIndex"] = question_index
    room["state"] = "QUESTION"
    room["questionStartTime"] = time.time() * 1000
    room["remainingSeconds"] = QUESTION_DURATION_SEC

    for p in room["players"].values():
        p["currentAnswer"] = None

    broadcast_room_state(room)
    schedule_bot_answers(room)

    cb = tornado.ioloop.PeriodicCallback(lambda: broadcast_timer_tick(room), 250)
    room["timerCallback"] = cb
    cb.start()


def schedule_bot_answers(room):
    q = QUESTIONS[room["currentQuestionIndex"]]
    loop = tornado.ioloop.IOLoop.current()

    for p in room["players"].values():
        if not p["isBot"]:
            continue
        delay_sec = random.uniform(1.8, 12.0)

        def make_bot_cb(bot_player):
            def _cb():
                if room["state"] != "QUESTION" or bot_player["currentAnswer"] is not None:
                    return
                if random.random() < 0.72:
                    chosen = q["correctIndex"]
                else:
                    wrong = [i for i in range(4) if i != q["correctIndex"]]
                    chosen = random.choice(wrong)
                handle_player_answer(room, bot_player, chosen)
            return _cb

        handle = loop.call_later(delay_sec, make_bot_cb(p))
        room["botTimeouts"].append(handle)


def handle_player_answer(room, player, option_index):
    if not room or room["state"] != "QUESTION":
        return
    if player["currentAnswer"] is not None:
        return

    q = QUESTIONS[room["currentQuestionIndex"]]
    try:
        idx = int(option_index)
    except Exception:
        return
    if idx < 0 or idx > 3:
        return

    now_ms = time.time() * 1000
    elapsed_ms = min(QUESTION_DURATION_MS, max(0, int(now_ms - room["questionStartTime"])))
    time_remaining_ratio = max(0.0, (QUESTION_DURATION_MS - elapsed_ms) / float(QUESTION_DURATION_MS))
    is_correct = (idx == q["correctIndex"])

    player["answeredCount"] += 1
    player["totalResponseTimeMs"] += elapsed_ms
    slot_key = q["mystery"]
    if slot_key in player["categoryStats"]:
        player["categoryStats"][slot_key]["total"] += 1

    speed_score = 0
    streak_bonus = 0
    points_earned = 0
    was_in_fire_mode = player["fireMode"]

    if is_correct:
        # Linear decay from 1000 down to 500 over 20s window
        speed_score = int(round(500 + 500 * time_remaining_ratio))
        # +20% bonus points if player already unlocked Alev Modu (3 consecutive correct answers)
        if was_in_fire_mode:
            streak_bonus = int(round(speed_score * 0.20))
        points_earned = speed_score + streak_bonus

        player["streak"] += 1
        if player["streak"] > player["maxStreak"]:
            player["maxStreak"] = player["streak"]
        player["fireMode"] = player["streak"] >= 3

        player["score"] += points_earned
        player["correctCount"] += 1
        player["correctResponseTimeMs"] += elapsed_ms
        if slot_key in player["categoryStats"]:
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
        "pointsEarned": points_earned,
        "hadFireBonus": bool(was_in_fire_mode and is_correct)
    }

    answered_count = sum(1 for p in room["players"].values() if p["currentAnswer"] is not None)

    if not player["isBot"]:
        emit_to_client(player["id"], "player:answer_ack", {
            "optionIndex": idx,
            "answeredCount": answered_count,
            "totalPlayers": len(room["players"])
        })

    if room.get("hostClientId"):
        emit_to_client(room["hostClientId"], "host:answer_progress", {
            "answeredCount": answered_count,
            "totalPlayers": len(room["players"]),
            "playerId": player["id"],
            "nickname": player["nickname"]
        })

    if len(room["players"]) > 0 and answered_count >= len(room["players"]):
        clear_room_timers(room)
        tornado.ioloop.IOLoop.current().call_later(
            0.55,
            lambda: transition_to_reveal(room) if room["state"] == "QUESTION" else None
        )


def transition_to_reveal(room):
    if not room or room["state"] == "REVEAL":
        return
    clear_room_timers(room)
    room["state"] = "REVEAL"
    room["remainingSeconds"] = 0
    q = QUESTIONS[room["currentQuestionIndex"]]

    for p in room["players"].values():
        if p["currentAnswer"] is None:
            p["streak"] = 0
            p["fireMode"] = False
            slot_key = q["mystery"]
            if slot_key in p["categoryStats"]:
                p["categoryStats"][slot_key]["total"] += 1
            p["currentAnswer"] = {
                "optionIndex": -1,
                "elapsedMs": QUESTION_DURATION_MS,
                "elapsedSec": QUESTION_DURATION_SEC,
                "isCorrect": False,
                "speedScore": 0,
                "streakBonus": 0,
                "pointsEarned": 0,
                "timedOut": True
            }

    broadcast_room_state(room)


def transition_to_leaderboard(room):
    if not room:
        return
    clear_room_timers(room)
    room["state"] = "LEADERBOARD"
    broadcast_room_state(room)


def transition_to_final_podium(room):
    if not room:
        return
    clear_room_timers(room)
    room["state"] = "FINAL_PODIUM"
    room["specialAwards"] = compute_end_game_badges(room)
    broadcast_room_state(room)


def handle_client_event(client_id, event, payload):
    global latest_active_pin
    client = clients.get(client_id)
    if not client:
        return

    if event == "host:create_room":
        req_pin = str(payload.get("pin", "")).strip()
        room = rooms.get(req_pin) if (req_pin and len(req_pin) == 4) else None
        if not room:
            room = create_room(req_pin if len(req_pin) == 4 else None)
        room["hostClientId"] = client_id
        client["roomPin"] = room["pin"]
        client["role"] = "host"
        latest_active_pin = room["pin"]
        broadcast_room_state(room)

    elif event == "host:add_bot":
        pin = str(payload.get("pin") or client.get("roomPin") or "")
        room = rooms.get(pin)
        if not room or room["state"] != "LOBBY":
            return
        bot_catalog = [
            {"nickname": "Ada_9A", "avatar": "🤖"},
            {"nickname": "Efe_Kod", "avatar": "⚡"},
            {"nickname": "Zeynep_9B", "avatar": "🚀"},
            {"nickname": "Kerem_Veri", "avatar": "🔍"},
            {"nickname": "Elif_Algo", "avatar": "⚙️"},
            {"nickname": "Mert_Bilişim", "avatar": "🦊"}
        ]
        existing = {p["nickname"] for p in room["players"].values()}
        avail = [b for b in bot_catalog if b["nickname"] not in existing]
        pick = avail[0] if avail else {"nickname": f"Öğrenci_Bot_{len(room['players']) + 1}", "avatar": "🤖"}
        bot_id = f"bot_{int(time.time() * 1000)}_{uuid.uuid4().hex[:5]}"
        room["players"][bot_id] = create_player_obj(bot_id, pick["nickname"], pick["avatar"], is_bot=True)
        broadcast_room_state(room)

    elif event == "host:start_game":
        pin = str(payload.get("pin") or client.get("roomPin") or "")
        room = rooms.get(pin)
        if room:
            start_question(room, 0)

    elif event == "host:next_step":
        pin = str(payload.get("pin") or client.get("roomPin") or "")
        room = rooms.get(pin)
        if not room:
            return
        if room["state"] == "QUESTION":
            transition_to_reveal(room)
        elif room["state"] == "REVEAL":
            if room["currentQuestionIndex"] >= len(QUESTIONS) - 1:
                transition_to_final_podium(room)
            else:
                transition_to_leaderboard(room)
        elif room["state"] == "LEADERBOARD":
            nxt = room["currentQuestionIndex"] + 1
            if nxt < len(QUESTIONS):
                start_question(room, nxt)
            else:
                transition_to_final_podium(room)

    elif event == "host:reset_game":
        pin = str(payload.get("pin") or client.get("roomPin") or "")
        room = rooms.get(pin)
        if not room:
            return
        clear_room_timers(room)
        room["state"] = "LOBBY"
        room["currentQuestionIndex"] = 0
        room["remainingSeconds"] = QUESTION_DURATION_SEC
        room["specialAwards"] = []
        if payload.get("keepPlayers", True):
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
                    "output": {"correct": 0, "total": 0}
                }
                p["currentAnswer"] = None
                p["badges"] = []
        else:
            room["players"].clear()
        broadcast_room_state(room)

    elif event == "player:check_active_pin":
        emit_to_client(client_id, "player:active_pin", {"pin": latest_active_pin})

    elif event == "player:join":
        raw_pin = str(payload.get("pin", "")).strip()
        nickname = str(payload.get("nickname", "")).strip()
        avatar = payload.get("avatar") or "🕵️"

        if not raw_pin or raw_pin not in rooms:
            emit_to_client(client_id, "player:join_error", {
                "message": "Geçersiz Oyun PIN kodu! Lütfen akıllı tahtadaki 4 haneli PIN kodunu kontrol edin."
            })
            return
        if len(nickname) < 2:
            emit_to_client(client_id, "player:join_error", {
                "message": "Lütfen en az 2 karakterli bir takma ad girin."
            })
            return

        room = rooms[raw_pin]
        existing_player = None
        for p in list(room["players"].values()):
            if not p["isBot"] and p["nickname"].lower() == nickname.lower():
                existing_player = p
                break

        if existing_player:
            del room["players"][existing_player["id"]]
            existing_player["id"] = client_id
            existing_player["avatar"] = avatar or existing_player["avatar"]
            existing_player["connected"] = True
            room["players"][client_id] = existing_player
        else:
            room["players"][client_id] = create_player_obj(client_id, nickname, avatar, is_bot=False)

        client["roomPin"] = raw_pin
        client["role"] = "player"
        client["playerId"] = client_id

        joined_player = room["players"][client_id]
        emit_to_client(client_id, "player:joined", build_player_state_payload(room, joined_player))
        broadcast_room_state(room)

    elif event == "player:submit_answer":
        pin = str(payload.get("pin") or client.get("roomPin") or "")
        room = rooms.get(pin)
        if not room:
            return
        player = room["players"].get(client_id)
        if not player:
            return
        handle_player_answer(room, player, payload.get("optionIndex"))


class GameWebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.client_id = f"ws_{int(time.time() * 1000)}_{uuid.uuid4().hex[:7]}"
        clients[self.client_id] = {
            "id": self.client_id,
            "ws": self,
            "roomPin": None,
            "role": None,
            "playerId": None
        }

    def on_message(self, message):
        try:
            msg = json.loads(message)
            event = msg.get("event")
            data = msg.get("data") or {}
            if event:
                handle_client_event(self.client_id, event, data)
        except Exception:
            pass

    def on_close(self):
        cid = getattr(self, "client_id", None)
        if not cid or cid not in clients:
            return
        client = clients[cid]
        pin = client.get("roomPin")
        room = rooms.get(pin) if pin else None
        if room and client.get("role") == "player":
            player = room["players"].get(cid)
            if player:
                if room["state"] == "LOBBY":
                    del room["players"][cid]
                else:
                    player["connected"] = False
                broadcast_room_state(room)
        del clients[cid]


class InfoHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({
            "name": "GİÇ Dedektifi (Input-Process-Output Game)",
            "activePin": latest_active_pin,
            "lanIp": get_local_ip(),
            "port": PORT,
            "totalQuestions": len(QUESTIONS)
        }))


class HtmlPageHandler(tornado.web.RequestHandler):
    def initialize(self, filename):
        self.filename = filename

    def get(self):
        filepath = os.path.join(PUBLIC_DIR, self.filename)
        if not os.path.exists(filepath):
            self.set_status(404)
            self.write("404 Bulunamadı")
            return
        self.set_header("Content-Type", "text/html; charset=utf-8")
        self.set_header("Cache-Control", "no-cache")
        with open(filepath, "rb") as f:
            self.write(f.read())


def make_app():
    return tornado.web.Application([
        (r"/ws", GameWebSocketHandler),
        (r"/api/info", InfoHandler),
        (r"/host/?", HtmlPageHandler, {"filename": "host.html"}),
        (r"/play/?", HtmlPageHandler, {"filename": "index.html"}),
        (r"/", HtmlPageHandler, {"filename": "index.html"}),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": PUBLIC_DIR}),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(PORT, address="0.0.0.0")
    lan_ip = get_local_ip()
    print("============================================================")
    print("🕵️ GİÇ DEDEKTİFİ (Input-Process-Output Game) Hazır!")
    print(f"🖥️  Host (Akıllı Tahta) Ekranı : http://localhost:{PORT}/host")
    print(f"📱 Öğrenci (Oyuncu) Ekranı    : http://{lan_ip}:{PORT}/play")
    print("============================================================")
    tornado.ioloop.IOLoop.current().start()
