/**
 * GİÇ Dedektifi (Input-Process-Output Game)
 * 9. Sınıf Bilgisayar Bilimi Dersi - Gerçek Zamanlı Çok Oyunculu Eğitim Uygulaması
 *
 * Works with Express + Socket.io AND native Node.js HTTP + WebSocket (/ws) on port 3000.
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const os = require('os');

const PORT = process.env.PORT || 3000;
const QUESTION_DURATION_SEC = 20;
const QUESTION_DURATION_MS = QUESTION_DURATION_SEC * 1000;

// ============================================================================
// QUESTION DATASET (9th-Grade Computer Science Input-Process-Output Scenarios)
// ============================================================================
const QUESTIONS = [
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
];

// ============================================================================
// ROOM & GAME STATE MANAGEMENT (4-DIGIT PIN)
// ============================================================================
const rooms = new Map();
let latestActivePin = null;

function generatePin() {
  let pin;
  do {
    pin = String(Math.floor(1000 + Math.random() * 9000));
  } while (rooms.has(pin));
  return pin;
}

function getLocalIpAddress() {
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name] || []) {
      if (iface.family === 'IPv4' && !iface.internal) {
        return iface.address;
      }
    }
  }
  return 'localhost';
}

function createRoom(requestedPin) {
  const pin = (requestedPin && /^\d{4}$/.test(String(requestedPin))) ? String(requestedPin) : generatePin();
  const room = {
    pin,
    state: 'LOBBY', // LOBBY | QUESTION | REVEAL | LEADERBOARD | FINAL_PODIUM
    hostClientId: null,
    currentQuestionIndex: 0,
    questionStartTime: null,
    remainingSeconds: QUESTION_DURATION_SEC,
    timerInterval: null,
    botTimeouts: [],
    players: new Map(),
    specialAwards: [],
    createdAt: Date.now()
  };
  rooms.set(pin, room);
  latestActivePin = pin;
  return room;
}

function createPlayerObj({ id, nickname, avatar, isBot = false }) {
  return {
    id,
    nickname: nickname.trim().slice(0, 18),
    avatar: avatar || '🕵️',
    isBot,
    connected: true,
    score: 0,
    streak: 0,
    maxStreak: 0,
    fireMode: false, // 3 consecutive correct answers -> Alev Modu (+20% bonus on next question)
    correctCount: 0,
    answeredCount: 0,
    totalResponseTimeMs: 0,
    correctResponseTimeMs: 0,
    categoryStats: {
      input: { correct: 0, total: 0 },
      process: { correct: 0, total: 0 },
      output: { correct: 0, total: 0 }
    },
    currentAnswer: null,
    badges: []
  };
}

function clearRoomTimers(room) {
  if (room.timerInterval) {
    clearInterval(room.timerInterval);
    room.timerInterval = null;
  }
  if (room.botTimeouts && room.botTimeouts.length) {
    room.botTimeouts.forEach(t => clearTimeout(t));
    room.botTimeouts = [];
  }
}

function getSortedLeaderboard(room) {
  const list = Array.from(room.players.values());
  list.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    if (b.correctCount !== a.correctCount) return b.correctCount - a.correctCount;
    return a.correctResponseTimeMs - b.correctResponseTimeMs;
  });
  return list.map((p, idx) => ({
    id: p.id,
    rank: idx + 1,
    nickname: p.nickname,
    avatar: p.avatar,
    isBot: p.isBot,
    score: p.score,
    streak: p.streak,
    maxStreak: p.maxStreak,
    fireMode: p.fireMode,
    correctCount: p.correctCount,
    answeredCount: p.answeredCount,
    avgSpeedSec: p.correctCount > 0 ? Number((p.correctResponseTimeMs / p.correctCount / 1000).toFixed(2)) : null,
    badges: p.badges || []
  }));
}

function computeEndGameBadges(room) {
  const players = Array.from(room.players.values());
  if (players.length === 0) return { specialAwards: [] };

  players.forEach(p => {
    p.badges = [];
    const ioCorrect = p.categoryStats.input.correct + p.categoryStats.output.correct;
    const procCorrect = p.categoryStats.process.correct;
    const avgCorrectMs = p.correctCount > 0 ? (p.correctResponseTimeMs / p.correctCount) : 99999;

    if (ioCorrect >= 4) {
      p.badges.push({
        id: 'VERI_DEDEKTIFI',
        title: 'Veri Dedektifi',
        icon: '🔍',
        desc: 'Girdi ve Çıktı verilerini ustalıkla çözdü!'
      });
    }
    if (procCorrect >= 2) {
      p.badges.push({
        id: 'SUREC_MIMARI',
        title: 'Süreç Mimarı',
        icon: '⚙️',
        desc: 'İşlem (Process) aşamalarını hatasız analiz etti!'
      });
    }
    if (p.correctCount >= 3 && avgCorrectMs <= 8500) {
      p.badges.push({
        id: 'TURBO_HIZLI',
        title: 'Turbo Hızlı',
        icon: '⚡',
        desc: `Şimşek hızında doğru yanıtlar verdi! (Ort. ${(avgCorrectMs / 1000).toFixed(1)} sn)`
      });
    }
    if (p.badges.length === 0) {
      p.badges.push({
        id: 'GIC_DEDEKTIFI',
        title: 'GİÇ Dedektifi',
        icon: '🕵️',
        desc: 'Tüm görevleri tamamlayarak dedektiflik eğitimini bitirdi!'
      });
    }
  });

  const byIO = [...players].sort((a, b) => {
    const aIO = a.categoryStats.input.correct + a.categoryStats.output.correct;
    const bIO = b.categoryStats.input.correct + b.categoryStats.output.correct;
    return bIO !== aIO ? bIO - aIO : b.score - a.score;
  })[0];

  const byProcess = [...players].sort((a, b) => {
    const aP = a.categoryStats.process.correct;
    const bP = b.categoryStats.process.correct;
    return bP !== aP ? bP - aP : b.score - a.score;
  })[0];

  const bySpeed = [...players]
    .filter(p => p.correctCount > 0)
    .sort((a, b) => (a.correctResponseTimeMs / a.correctCount) - (b.correctResponseTimeMs / b.correctCount))[0] || players[0];

  const specialAwards = [
    {
      id: 'VERI_DEDEKTIFI',
      title: 'Veri Dedektifi',
      icon: '🔍',
      subtitle: 'Girdi & Çıktı Uzmanı',
      winner: byIO ? { nickname: byIO.nickname, avatar: byIO.avatar, stat: `${byIO.categoryStats.input.correct + byIO.categoryStats.output.correct} Doğru` } : null
    },
    {
      id: 'SUREC_MIMARI',
      title: 'Süreç Mimarı',
      icon: '⚙️',
      subtitle: 'İşlem (Process) Ustası',
      winner: byProcess ? { nickname: byProcess.nickname, avatar: byProcess.avatar, stat: `${byProcess.categoryStats.process.correct} Doğru` } : null
    },
    {
      id: 'TURBO_HIZLI',
      title: 'Turbo Hızlı',
      icon: '⚡',
      subtitle: 'En Hızlı Dedektif',
      winner: bySpeed ? {
        nickname: bySpeed.nickname,
        avatar: bySpeed.avatar,
        stat: bySpeed.correctCount > 0
          ? `${(bySpeed.correctResponseTimeMs / bySpeed.correctCount / 1000).toFixed(2)} sn ort.`
          : `${bySpeed.score} Puan`
      } : null
    }
  ];

  return { specialAwards };
}

function buildHostStatePayload(room) {
  const q = QUESTIONS[room.currentQuestionIndex] || QUESTIONS[0];
  const leaderboard = getSortedLeaderboard(room);
  const totalPlayers = room.players.size;
  let answeredCount = 0;
  const optionCounts = [0, 0, 0, 0];

  room.players.forEach(p => {
    if (p.currentAnswer !== null) {
      answeredCount++;
      if (p.currentAnswer.optionIndex >= 0 && p.currentAnswer.optionIndex < 4) {
        optionCounts[p.currentAnswer.optionIndex]++;
      }
    }
  });

  const isRevealOrLater = room.state === 'REVEAL' || room.state === 'LEADERBOARD' || room.state === 'FINAL_PODIUM';
  const unlockedAnswer = q.options[q.correctIndex];

  const stages = {
    input: q.mystery === 'input' ? (isRevealOrLater ? unlockedAnswer : '?') : q.input,
    process: q.mystery === 'process' ? (isRevealOrLater ? unlockedAnswer : '?') : q.process,
    output: q.mystery === 'output' ? (isRevealOrLater ? unlockedAnswer : '?') : q.output
  };

  return {
    pin: room.pin,
    lanIp: getLocalIpAddress(),
    port: PORT,
    state: room.state,
    questionIndex: room.currentQuestionIndex,
    totalQuestions: QUESTIONS.length,
    remainingSeconds: room.remainingSeconds,
    totalSeconds: QUESTION_DURATION_SEC,
    totalPlayers,
    answeredCount,
    players: leaderboard,
    top5: leaderboard.slice(0, 5),
    question: {
      id: q.id,
      title: q.title,
      theme: q.theme,
      mystery: q.mystery, // 'input' | 'process' | 'output'
      question: q.question,
      stages,
      options: q.options,
      correctIndex: isRevealOrLater ? q.correctIndex : null,
      optionCounts: isRevealOrLater ? optionCounts : null
    },
    specialAwards: room.state === 'FINAL_PODIUM' ? (room.specialAwards || []) : []
  };
}

function buildPlayerStatePayload(room, player) {
  const q = QUESTIONS[room.currentQuestionIndex] || QUESTIONS[0];
  const leaderboard = getSortedLeaderboard(room);
  const rankInfo = leaderboard.find(item => item.id === player.id);
  const rank = rankInfo ? rankInfo.rank : leaderboard.length;
  const isRevealOrLater = room.state === 'REVEAL' || room.state === 'LEADERBOARD' || room.state === 'FINAL_PODIUM';

  return {
    pin: room.pin,
    state: room.state,
    questionIndex: room.currentQuestionIndex,
    totalQuestions: QUESTIONS.length,
    remainingSeconds: room.remainingSeconds,
    totalSeconds: QUESTION_DURATION_SEC,
    player: {
      id: player.id,
      nickname: player.nickname,
      avatar: player.avatar,
      score: player.score,
      streak: player.streak,
      maxStreak: player.maxStreak,
      fireMode: player.fireMode,
      rank,
      totalPlayers: room.players.size,
      correctCount: player.correctCount,
      answeredCount: player.answeredCount,
      badges: player.badges || [],
      currentAnswer: player.currentAnswer
    },
    question: {
      id: q.id,
      title: q.title,
      theme: q.theme,
      mystery: q.mystery,
      question: q.question,
      options: q.options,
      correctIndex: isRevealOrLater ? q.correctIndex : null,
      correctOptionText: isRevealOrLater ? q.options[q.correctIndex] : null
    },
    top3: room.state === 'FINAL_PODIUM' ? leaderboard.slice(0, 3) : []
  };
}

// ============================================================================
// REAL-TIME TRANSPORT ABSTRACTION (Socket.io & Native WebSocket)
// ============================================================================
const clients = new Map();

function emitToClient(clientId, event, data) {
  const client = clients.get(clientId);
  if (client && typeof client.sendEvent === 'function') {
    client.sendEvent(event, data);
  }
}

function broadcastRoomState(room) {
  if (!room) return;
  if (room.hostClientId) {
    emitToClient(room.hostClientId, 'game:state_update', buildHostStatePayload(room));
  }
  room.players.forEach(player => {
    if (!player.isBot) {
      emitToClient(player.id, 'player:state_update', buildPlayerStatePayload(room, player));
    }
  });
}

function broadcastTimerTick(room) {
  if (!room) return;
  const elapsed = room.questionStartTime ? (Date.now() - room.questionStartTime) : 0;
  const remainingMs = Math.max(0, QUESTION_DURATION_MS - elapsed);
  room.remainingSeconds = Math.ceil(remainingMs / 1000);

  const payload = {
    remainingSeconds: room.remainingSeconds,
    remainingMs,
    totalSeconds: QUESTION_DURATION_SEC
  };

  if (room.hostClientId) {
    emitToClient(room.hostClientId, 'game:timer_tick', payload);
  }
  room.players.forEach(player => {
    if (!player.isBot) {
      emitToClient(player.id, 'game:timer_tick', payload);
    }
  });
}

// ============================================================================
// GAME STATE MACHINE & SCORING (1000->500 Linear Decay + 3x Streak +20% Bonus)
// ============================================================================
function startQuestion(room, questionIndex) {
  clearRoomTimers(room);
  room.currentQuestionIndex = questionIndex;
  room.state = 'QUESTION';
  room.questionStartTime = Date.now();
  room.remainingSeconds = QUESTION_DURATION_SEC;

  room.players.forEach(player => {
    player.currentAnswer = null;
  });

  broadcastRoomState(room);
  scheduleBotAnswers(room);

  room.timerInterval = setInterval(() => {
    const elapsed = Date.now() - room.questionStartTime;
    const remainingMs = Math.max(0, QUESTION_DURATION_MS - elapsed);
    room.remainingSeconds = Math.ceil(remainingMs / 1000);
    broadcastTimerTick(room);

    if (remainingMs <= 0) {
      transitionToReveal(room);
    }
  }, 250);
}

function scheduleBotAnswers(room) {
  const q = QUESTIONS[room.currentQuestionIndex];
  if (!q) return;

  room.players.forEach(player => {
    if (!player.isBot) return;
    const delayMs = Math.floor(1800 + Math.random() * 11500);
    const timeoutId = setTimeout(() => {
      if (room.state !== 'QUESTION' || player.currentAnswer !== null) return;
      const isRight = Math.random() < 0.72;
      let chosenIndex = q.correctIndex;
      if (!isRight) {
        const wrongOptions = [0, 1, 2, 3].filter(i => i !== q.correctIndex);
        chosenIndex = wrongOptions[Math.floor(Math.random() * wrongOptions.length)];
      }
      handlePlayerAnswer(room, player, chosenIndex);
    }, delayMs);
    room.botTimeouts.push(timeoutId);
  });
}

function handlePlayerAnswer(room, player, optionIndex) {
  if (!room || room.state !== 'QUESTION') return;
  if (player.currentAnswer !== null) return;

  const q = QUESTIONS[room.currentQuestionIndex];
  if (!q) return;

  const idx = Number(optionIndex);
  if (Number.isNaN(idx) || idx < 0 || idx > 3) return;

  const elapsedMs = Math.min(QUESTION_DURATION_MS, Math.max(0, Date.now() - room.questionStartTime));
  const timeRemainingRatio = Math.max(0, (QUESTION_DURATION_MS - elapsedMs) / QUESTION_DURATION_MS);
  const isCorrect = idx === q.correctIndex;

  player.answeredCount++;
  player.totalResponseTimeMs += elapsedMs;

  if (player.categoryStats[q.mystery]) {
    player.categoryStats[q.mystery].total++;
  }

  let speedScore = 0;
  let streakBonus = 0;
  let pointsEarned = 0;
  const wasInFireMode = player.fireMode; // Active from 3+ streak on previous questions

  if (isCorrect) {
    // Score decays linearly from 1000 down to 500 based on answer speed within 20s window
    speedScore = Math.round(500 + 500 * timeRemainingRatio);

    // If player already triggered Alev Modu (3 consecutive correct answers), +20% bonus on next question
    if (wasInFireMode) {
      streakBonus = Math.round(speedScore * 0.20);
    }
    pointsEarned = speedScore + streakBonus;

    player.streak += 1;
    if (player.streak > player.maxStreak) {
      player.maxStreak = player.streak;
    }
    player.fireMode = player.streak >= 3;

    player.score += pointsEarned;
    player.correctCount += 1;
    player.correctResponseTimeMs += elapsedMs;
    if (player.categoryStats[q.mystery]) {
      player.categoryStats[q.mystery].correct++;
    }
  } else {
    player.streak = 0;
    player.fireMode = false;
  }

  player.currentAnswer = {
    optionIndex: idx,
    elapsedMs,
    elapsedSec: Number((elapsedMs / 1000).toFixed(2)),
    isCorrect,
    speedScore,
    streakBonus,
    pointsEarned,
    hadFireBonus: wasInFireMode && isCorrect
  };

  let answeredCount = 0;
  room.players.forEach(p => {
    if (p.currentAnswer !== null) answeredCount++;
  });

  if (!player.isBot) {
    emitToClient(player.id, 'player:answer_ack', {
      optionIndex: idx,
      answeredCount,
      totalPlayers: room.players.size
    });
  }

  if (room.hostClientId) {
    emitToClient(room.hostClientId, 'host:answer_progress', {
      answeredCount,
      totalPlayers: room.players.size,
      playerId: player.id,
      nickname: player.nickname
    });
  }

  // Automatically trigger Reveal Mode when all students have answered
  if (room.players.size > 0 && answeredCount >= room.players.size) {
    clearRoomTimers(room);
    setTimeout(() => {
      if (room.state === 'QUESTION') {
        transitionToReveal(room);
      }
    }, 550);
  }
}

function transitionToReveal(room) {
  if (!room || room.state === 'REVEAL') return;
  clearRoomTimers(room);
  room.state = 'REVEAL';
  room.remainingSeconds = 0;

  const q = QUESTIONS[room.currentQuestionIndex];
  room.players.forEach(player => {
    if (player.currentAnswer === null) {
      player.streak = 0;
      player.fireMode = false;
      if (q && player.categoryStats[q.mystery]) {
        player.categoryStats[q.mystery].total++;
      }
      player.currentAnswer = {
        optionIndex: -1,
        elapsedMs: QUESTION_DURATION_MS,
        elapsedSec: QUESTION_DURATION_SEC,
        isCorrect: false,
        speedScore: 0,
        streakBonus: 0,
        pointsEarned: 0,
        timedOut: true
      };
    }
  });

  broadcastRoomState(room);
}

function transitionToLeaderboard(room) {
  if (!room) return;
  clearRoomTimers(room);
  room.state = 'LEADERBOARD';
  broadcastRoomState(room);
}

function transitionToFinalPodium(room) {
  if (!room) return;
  clearRoomTimers(room);
  room.state = 'FINAL_PODIUM';
  const { specialAwards } = computeEndGameBadges(room);
  room.specialAwards = specialAwards;
  broadcastRoomState(room);
}

// ============================================================================
// CLIENT EVENT ROUTER
// ============================================================================
function handleClientEvent(clientId, event, payload = {}) {
  const client = clients.get(clientId);
  if (!client) return;

  switch (event) {
    case 'host:create_room': {
      let room = payload.pin && rooms.get(String(payload.pin));
      if (!room) {
        room = createRoom(payload.pin);
      }
      room.hostClientId = clientId;
      client.roomPin = room.pin;
      client.role = 'host';
      latestActivePin = room.pin;
      broadcastRoomState(room);
      break;
    }

    case 'host:add_bot': {
      const room = rooms.get(String(payload.pin || client.roomPin));
      if (!room || room.state !== 'LOBBY') return;
      const botCatalog = [
        { nickname: 'Ada_9A', avatar: '🤖' },
        { nickname: 'Efe_Kod', avatar: '⚡' },
        { nickname: 'Zeynep_9B', avatar: '🚀' },
        { nickname: 'Kerem_Veri', avatar: '🔍' },
        { nickname: 'Elif_Algo', avatar: '⚙️' },
        { nickname: 'Mert_Bilişim', avatar: '🦊' }
      ];
      const existingNames = new Set(Array.from(room.players.values()).map(p => p.nickname));
      const available = botCatalog.filter(b => !existingNames.has(b.nickname));
      const pick = available.length > 0
        ? available[0]
        : { nickname: `Öğrenci_Bot_${room.players.size + 1}`, avatar: '🤖' };

      const botId = `bot_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
      room.players.set(botId, createPlayerObj({
        id: botId,
        nickname: pick.nickname,
        avatar: pick.avatar,
        isBot: true
      }));
      broadcastRoomState(room);
      break;
    }

    case 'host:start_game': {
      const room = rooms.get(String(payload.pin || client.roomPin));
      if (!room) return;
      startQuestion(room, 0);
      break;
    }

    case 'host:next_step': {
      const room = rooms.get(String(payload.pin || client.roomPin));
      if (!room) return;

      if (room.state === 'QUESTION') {
        transitionToReveal(room);
      } else if (room.state === 'REVEAL') {
        if (room.currentQuestionIndex >= QUESTIONS.length - 1) {
          transitionToFinalPodium(room);
        } else {
          transitionToLeaderboard(room);
        }
      } else if (room.state === 'LEADERBOARD') {
        const nextIdx = room.currentQuestionIndex + 1;
        if (nextIdx < QUESTIONS.length) {
          startQuestion(room, nextIdx);
        } else {
          transitionToFinalPodium(room);
        }
      }
      break;
    }

    case 'host:reset_game': {
      const room = rooms.get(String(payload.pin || client.roomPin));
      if (!room) return;
      clearRoomTimers(room);
      room.state = 'LOBBY';
      room.currentQuestionIndex = 0;
      room.remainingSeconds = QUESTION_DURATION_SEC;
      room.specialAwards = [];

      if (payload.keepPlayers !== false) {
        room.players.forEach(p => {
          p.score = 0;
          p.streak = 0;
          p.maxStreak = 0;
          p.fireMode = false;
          p.correctCount = 0;
          p.answeredCount = 0;
          p.totalResponseTimeMs = 0;
          p.correctResponseTimeMs = 0;
          p.categoryStats = {
            input: { correct: 0, total: 0 },
            process: { correct: 0, total: 0 },
            output: { correct: 0, total: 0 }
          };
          p.currentAnswer = null;
          p.badges = [];
        });
      } else {
        room.players.clear();
      }
      broadcastRoomState(room);
      break;
    }

    case 'player:check_active_pin': {
      emitToClient(clientId, 'player:active_pin', { pin: latestActivePin || null });
      break;
    }

    case 'player:join': {
      const rawPin = String(payload.pin || '').trim();
      const nickname = String(payload.nickname || '').trim();
      const avatar = payload.avatar || '🕵️';

      if (!rawPin || !rooms.has(rawPin)) {
        emitToClient(clientId, 'player:join_error', {
          message: 'Geçersiz Oyun PIN kodu! Lütfen akıllı tahtadaki 4 haneli PIN kodunu kontrol edin.'
        });
        return;
      }
      if (!nickname || nickname.length < 2) {
        emitToClient(clientId, 'player:join_error', {
          message: 'Lütfen en az 2 karakterli bir takma ad girin.'
        });
        return;
      }

      const room = rooms.get(rawPin);
      let existingPlayer = null;
      room.players.forEach(p => {
        if (!p.isBot && p.nickname.toLowerCase() === nickname.toLowerCase()) {
          existingPlayer = p;
        }
      });

      if (existingPlayer) {
        room.players.delete(existingPlayer.id);
        existingPlayer.id = clientId;
        existingPlayer.avatar = avatar || existingPlayer.avatar;
        existingPlayer.connected = true;
        room.players.set(clientId, existingPlayer);
      } else {
        room.players.set(clientId, createPlayerObj({
          id: clientId,
          nickname,
          avatar,
          isBot: false
        }));
      }

      client.roomPin = rawPin;
      client.role = 'player';
      client.playerId = clientId;

      const joinedPlayer = room.players.get(clientId);
      emitToClient(clientId, 'player:joined', buildPlayerStatePayload(room, joinedPlayer));
      broadcastRoomState(room);
      break;
    }

    case 'player:submit_answer': {
      const pin = String(payload.pin || client.roomPin || '');
      const room = rooms.get(pin);
      if (!room) return;
      const player = room.players.get(clientId);
      if (!player) return;
      handlePlayerAnswer(room, player, payload.optionIndex);
      break;
    }

    default:
      break;
  }
}

function handleClientDisconnect(clientId) {
  const client = clients.get(clientId);
  if (!client) return;
  const room = client.roomPin ? rooms.get(client.roomPin) : null;
  if (room && client.role === 'player') {
    const player = room.players.get(clientId);
    if (player) {
      if (room.state === 'LOBBY') {
        room.players.delete(clientId);
      } else {
        player.connected = false;
      }
      broadcastRoomState(room);
    }
  }
  clients.delete(clientId);
}

// ============================================================================
// HTTP SERVER & ROUTES (/host, /play, /, /api/info)
// ============================================================================
const PUBLIC_DIR = path.join(__dirname, 'public');
const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.ico': 'image/x-icon'
};

function serveFile(res, filePath) {
  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('404 Bulunamadı');
      return;
    }
    const ext = path.extname(filePath).toLowerCase();
    res.writeHead(200, {
      'Content-Type': MIME_TYPES[ext] || 'application/octet-stream',
      'Cache-Control': 'no-cache'
    });
    res.end(content);
  });
}

function httpRequestHandler(req, res) {
  const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = parsedUrl.pathname;

  if (pathname === '/api/info') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({
      name: 'GİÇ Dedektifi (Input-Process-Output Game)',
      activePin: latestActivePin,
      lanIp: getLocalIpAddress(),
      port: PORT,
      totalQuestions: QUESTIONS.length
    }));
    return;
  }

  if (pathname === '/host' || pathname === '/host/') {
    serveFile(res, path.join(PUBLIC_DIR, 'host.html'));
    return;
  }

  if (pathname === '/play' || pathname === '/play/' || pathname === '/') {
    serveFile(res, path.join(PUBLIC_DIR, 'index.html'));
    return;
  }

  const safeSuffix = path.normalize(pathname).replace(/^(\.\.[/\\])+/, '');
  const filePath = path.join(PUBLIC_DIR, safeSuffix);
  if (filePath.startsWith(PUBLIC_DIR) && fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    serveFile(res, filePath);
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('404 Not Found');
}

let server;
try {
  const express = require('express');
  const { Server: SocketIOServer } = require('socket.io');

  const app = express();
  app.get('/api/info', (req, res) => {
    res.json({
      name: 'GİÇ Dedektifi (Input-Process-Output Game)',
      activePin: latestActivePin,
      lanIp: getLocalIpAddress(),
      port: PORT,
      totalQuestions: QUESTIONS.length
    });
  });
  app.get(['/host', '/host/'], (req, res) => res.sendFile(path.join(PUBLIC_DIR, 'host.html')));
  app.get(['/play', '/play/', '/'], (req, res) => res.sendFile(path.join(PUBLIC_DIR, 'index.html')));
  app.use(express.static(PUBLIC_DIR));

  server = http.createServer(app);
  const io = new SocketIOServer(server, { cors: { origin: '*' } });

  io.on('connection', socket => {
    const clientId = socket.id;
    clients.set(clientId, {
      id: clientId,
      sendEvent: (event, data) => socket.emit(event, data)
    });
    socket.onAny((event, payload) => handleClientEvent(clientId, event, payload));
    socket.on('disconnect', () => handleClientDisconnect(clientId));
  });
} catch (_) {
  server = http.createServer(httpRequestHandler);
}

server.on('upgrade', (req, socket) => {
  const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  if (parsedUrl.pathname !== '/ws') return;

  const key = req.headers['sec-websocket-key'];
  if (!key) {
    socket.destroy();
    return;
  }

  const acceptKey = crypto
    .createHash('sha1')
    .update(key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11', 'binary')
    .digest('base64');

  socket.write([
    'HTTP/1.1 101 Switching Protocols',
    'Upgrade: websocket',
    'Connection: Upgrade',
    `Sec-WebSocket-Accept: ${acceptKey}`,
    '\r\n'
  ].join('\r\n'));

  const clientId = `ws_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`;

  function sendWsFrame(obj) {
    if (socket.destroyed || !socket.writable) return;
    const payloadBuf = Buffer.from(JSON.stringify(obj), 'utf8');
    const len = payloadBuf.length;
    let headerBuf;
    if (len < 126) {
      headerBuf = Buffer.alloc(2);
      headerBuf[0] = 0x81;
      headerBuf[1] = len;
    } else if (len < 65536) {
      headerBuf = Buffer.alloc(4);
      headerBuf[0] = 0x81;
      headerBuf[1] = 126;
      headerBuf.writeUInt16BE(len, 2);
    } else {
      headerBuf = Buffer.alloc(10);
      headerBuf[0] = 0x81;
      headerBuf[1] = 127;
      headerBuf.writeBigUInt64BE(BigInt(len), 2);
    }
    socket.write(Buffer.concat([headerBuf, payloadBuf]));
  }

  clients.set(clientId, {
    id: clientId,
    sendEvent: (event, data) => sendWsFrame({ event, data })
  });

  let buffer = Buffer.alloc(0);
  socket.on('data', chunk => {
    buffer = Buffer.concat([buffer, chunk]);
    while (buffer.length >= 2) {
      const firstByte = buffer[0];
      const secondByte = buffer[1];
      const opcode = firstByte & 0x0f;
      const isMasked = (secondByte & 0x80) !== 0;
      let payloadLen = secondByte & 0x7f;
      let offset = 2;

      if (payloadLen === 126) {
        if (buffer.length < 4) return;
        payloadLen = buffer.readUInt16BE(2);
        offset = 4;
      } else if (payloadLen === 127) {
        if (buffer.length < 10) return;
        payloadLen = Number(buffer.readBigUInt64BE(2));
        offset = 10;
      }

      const maskLen = isMasked ? 4 : 0;
      if (buffer.length < offset + maskLen + payloadLen) return;

      const maskKey = isMasked ? buffer.slice(offset, offset + 4) : null;
      offset += maskLen;
      const frameData = Buffer.from(buffer.slice(offset, offset + payloadLen));
      buffer = buffer.slice(offset + payloadLen);

      if (opcode === 0x8) {
        socket.end();
        return;
      }
      if (opcode === 0x9) {
        socket.write(Buffer.from([0x8a, 0x00]));
        continue;
      }
      if (opcode === 0x1) {
        if (isMasked && maskKey) {
          for (let i = 0; i < frameData.length; i++) {
            frameData[i] ^= maskKey[i % 4];
          }
        }
        try {
          const msg = JSON.parse(frameData.toString('utf8'));
          if (msg && msg.event) {
            handleClientEvent(clientId, msg.event, msg.data || {});
          }
        } catch (_) {}
      }
    }
  });

  socket.on('close', () => handleClientDisconnect(clientId));
  socket.on('error', () => handleClientDisconnect(clientId));
});

server.listen(PORT, '0.0.0.0', () => {
  const lanIp = getLocalIpAddress();
  console.log('============================================================');
  console.log('🕵️ GİÇ DEDEKTİFİ (Input-Process-Output Game) Hazır!');
  console.log(`🖥️  Host (Akıllı Tahta) Ekranı : http://localhost:${PORT}/host`);
  console.log(`📱 Öğrenci (Oyuncu) Ekranı    : http://${lanIp}:${PORT}/play`);
  console.log('============================================================');
});
