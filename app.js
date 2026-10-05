// TokyoFlow Interactive Experience Engine
// Zero Emoji Discipline Enforced

const SCENARIO_DATA = {
  zh: {
    densha: {
      level: "JLPT N4-N3 • 交通实境",
      register: "敬语・站台广播",
      districtName: "新宿站 • 2号站台",
      jpText: "まもなく、2番線に山手線がまいります。黄色い点字ブロックの内側までお下がりください。",
      romajiText: "Mamonaku, ni-ban-sen ni Yamanote-sen ga mairimasu.",
      translationText: "山手线电车即将到达2号站台，请退至黄色盲道内侧等候。",
      pitchName: "中高型（高音落在中间）",
      pitchPath: "M 10 20 Q 50 5 100 8 T 190 22",
      dots: [
        { cx: 20, cy: 18, fill: "#fff", stroke: "#BC382C" },
        { cx: 70, cy: 8, fill: "#BC382C" },
        { cx: 130, cy: 12, fill: "#BC382C" },
        { cx: 180, cy: 22, fill: "#fff", stroke: "#BC382C" }
      ],
      playBtnDefault: "试听东京真人原声音频",
      playBtnPlaying: "正在播放东京真人原声..."
    },
    kombini: {
      level: "JLPT N5-N4 • 便利店实境",
      register: "接客・礼貌语",
      districtName: "涩谷中心街 • 7-Eleven",
      jpText: "お弁当温めますか？レジ袋はご利用ですか？",
      romajiText: "Obento atatamemasu ka? Reji-bukuro wa go-riyo desu ka?",
      translationText: "便当需要帮您加热吗？需要使用塑料购物袋吗？",
      pitchName: "平板型（平直无跌落）",
      pitchPath: "M 10 22 Q 40 8 100 8 L 190 8",
      dots: [
        { cx: 20, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 60, cy: 8, fill: "#BC382C" },
        { cx: 120, cy: 8, fill: "#BC382C" },
        { cx: 180, cy: 8, fill: "#BC382C" }
      ],
      playBtnDefault: "试听东京真人原声音频",
      playBtnPlaying: "正在播放东京真人原声..."
    },
    izakaya: {
      level: "JLPT N5-N4 • 昭和居酒屋",
      register: "日常・自然口语",
      districtName: "回忆横丁 • 烤鸡串小巷",
      jpText: "とりあえず生ビール二つ、焼き鳥盛り合わせ塩で！",
      romajiText: "Toriaezu nama biiru futatsu, yakitori moriawase shio de!",
      translationText: "先来两杯生啤酒，再来一份盐烤烤鸡串拼盘！",
      pitchName: "头高型（高音落在首拍）",
      pitchPath: "M 10 6 Q 40 22 100 22 L 190 22",
      dots: [
        { cx: 20, cy: 6, fill: "#BC382C" },
        { cx: 60, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 120, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 180, cy: 22, fill: "#fff", stroke: "#BC382C" }
      ],
      playBtnDefault: "试听东京真人原声音频",
      playBtnPlaying: "正在播放东京真人原声..."
    },
    akiba: {
      level: "JLPT N5-N4 • 动漫模型店",
      register: "兴趣・流行俗语",
      districtName: "无线电会馆 • 秋叶原",
      jpText: "すみません、この限定フィギュアの未開封品は在庫ありますか？",
      romajiText: "Sumimasen, kono gentei figyua no mikaihin wa zaiko arimasu ka?",
      translationText: "请问这款限定手办的未开封新品还有库存吗？",
      pitchName: "尾高型（词尾后发生跌落）",
      pitchPath: "M 10 22 Q 60 8 150 8 T 190 22",
      dots: [
        { cx: 20, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 70, cy: 8, fill: "#BC382C" },
        { cx: 140, cy: 8, fill: "#BC382C" },
        { cx: 185, cy: 22, fill: "#fff", stroke: "#BC382C" }
      ],
      playBtnDefault: "试听东京真人原声音频",
      playBtnPlaying: "正在播放东京真人原声..."
    }
  },
  en: {
    densha: {
      level: "JLPT N4-N3 • TRANSIT",
      register: "Keigo (Honorific)",
      districtName: "Shinjuku Station • Track 2",
      jpText: "まもなく、2番線に山手線がまいります。黄色い点字ブロックの内側までお下がりください。",
      romajiText: "Mamonaku, ni-ban-sen ni Yamanote-sen ga mairimasu.",
      translationText: "The Yamanote Line train will soon arrive at Track 2. Please wait behind the yellow line.",
      pitchName: "Nakadaka (Mid-High Peak)",
      pitchPath: "M 10 20 Q 50 5 100 8 T 190 22",
      dots: [
        { cx: 20, cy: 18, fill: "#fff", stroke: "#BC382C" },
        { cx: 70, cy: 8, fill: "#BC382C" },
        { cx: 130, cy: 12, fill: "#BC382C" },
        { cx: 180, cy: 22, fill: "#fff", stroke: "#BC382C" }
      ],
      playBtnDefault: "Play Tokyo Native Audio",
      playBtnPlaying: "Playing Native Voice..."
    },
    kombini: {
      level: "JLPT N5-N4 • KOMBINI",
      register: "Teineigo (Polite Register)",
      districtName: "Shibuya Center-Gai • 7-Eleven",
      jpText: "お弁当温めますか？レジ袋はご利用ですか？",
      romajiText: "Obento atatamemasu ka? Reji-bukuro wa go-riyo desu ka?",
      translationText: "Would you like your bento warmed? Do you need a plastic shopping bag?",
      pitchName: "Heiban (Flat / Pitch Plateau)",
      pitchPath: "M 10 22 Q 40 8 100 8 L 190 8",
      dots: [
        { cx: 20, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 60, cy: 8, fill: "#BC382C" },
        { cx: 120, cy: 8, fill: "#BC382C" },
        { cx: 180, cy: 8, fill: "#BC382C" }
      ],
      playBtnDefault: "Play Tokyo Native Audio",
      playBtnPlaying: "Playing Native Voice..."
    },
    izakaya: {
      level: "JLPT N5-N4 • IZAKAYA",
      register: "Tameguchi (Casual Living)",
      districtName: "Omoide Yokocho • Yakitori Alley",
      jpText: "とりあえず生ビール二つ、焼き鳥盛り合わせ塩で！",
      romajiText: "Toriaezu nama biiru futatsu, yakitori moriawase shio de!",
      translationText: "First two draft beers, and a salt-grilled yakitori platter please!",
      pitchName: "Atamadaka (Initial Peak)",
      pitchPath: "M 10 6 Q 40 22 100 22 L 190 22",
      dots: [
        { cx: 20, cy: 6, fill: "#BC382C" },
        { cx: 60, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 120, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 180, cy: 22, fill: "#fff", stroke: "#BC382C" }
      ],
      playBtnDefault: "Play Tokyo Native Audio",
      playBtnPlaying: "Playing Native Voice..."
    },
    akiba: {
      level: "JLPT N5-N4 • ANIME & SFX",
      register: "Pop Culture & Slang",
      districtName: "Radio Kaikan • Akihabara",
      jpText: "すみません、この限定フィギュアの未開封品は在庫ありますか？",
      romajiText: "Sumimasen, kono gentei figyua no mikaihin wa zaiko arimasu ka?",
      translationText: "Excuse me, is this limited figure in mint unopened condition in stock?",
      pitchName: "Odaka (Final Pitch Drop)",
      pitchPath: "M 10 22 Q 60 8 150 8 T 190 22",
      dots: [
        { cx: 20, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 70, cy: 8, fill: "#BC382C" },
        { cx: 140, cy: 8, fill: "#BC382C" },
        { cx: 185, cy: 22, fill: "#fff", stroke: "#BC382C" }
      ],
      playBtnDefault: "Play Tokyo Native Audio",
      playBtnPlaying: "Playing Native Voice..."
    }
  }
};

const AUDIO_FILES = {
  densha: "/assets/audio/densha.mp3",
  kombini: "/assets/audio/kombini.mp3",
  izakaya: "/assets/audio/izakaya.mp3",
  akiba: "/assets/audio/akiba.mp3"
};

let currentScenarioKey = 'densha';
let activeAudio = null;

function getPageLanguage() {
  return document.documentElement.lang.startsWith('zh') ? 'zh' : 'en';
}

function updateTokyoClock() {
  const clockEl = document.getElementById('tokyo-clock');
  if (!clockEl) return;
  const now = new Date();
  const options = {
    timeZone: 'Asia/Tokyo',
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  };
  const timeStr = new Intl.DateTimeFormat('en-US', options).format(now);
  clockEl.textContent = 'TOKYO ' + timeStr + ' JST';
}

function switchScenario(key) {
  currentScenarioKey = key;
  const lang = getPageLanguage();
  const data = SCENARIO_DATA[lang][key];
  if (!data) return;

  // Stop any active audio
  if (activeAudio) {
    activeAudio.pause();
    activeAudio.currentTime = 0;
    activeAudio = null;
    document.getElementById('waveformContainer')?.classList.remove('is-playing');
  }

  // Update scenario tabs active state
  document.querySelectorAll('.scenario-tab').forEach(tab => {
    tab.classList.toggle('active', tab.getAttribute('data-scenario') === key);
  });

  // Update screen content
  const levelEl = document.getElementById('appLevel');
  const regEl = document.getElementById('appRegister');
  const distEl = document.getElementById('appDistrictName');
  const jpEl = document.getElementById('appJpText');
  const romajiEl = document.getElementById('appRomajiText');
  const enEl = document.getElementById('appEnText');
  const pitchNameEl = document.getElementById('pitchPatternName');
  const pitchPathEl = document.getElementById('pitchPath');
  const playLabelEl = document.getElementById('appPlayLabel');
  const playIconEl = document.getElementById('appPlayIcon');

  if (levelEl) levelEl.textContent = data.level;
  if (regEl) regEl.textContent = data.register;
  if (distEl) distEl.textContent = data.districtName;
  if (jpEl) jpEl.textContent = data.jpText;
  if (romajiEl) romajiEl.textContent = data.romajiText;
  if (enEl) enEl.textContent = data.translationText;
  if (pitchNameEl) pitchNameEl.textContent = data.pitchName;
  if (pitchPathEl) pitchPathEl.setAttribute('d', data.pitchPath);
  if (playLabelEl) playLabelEl.textContent = data.playBtnDefault;
  if (playIconEl) playIconEl.textContent = '▶';

  // Update dots
  const dot1 = document.getElementById('pitchDot1');
  const dot2 = document.getElementById('pitchDot2');
  const dot3 = document.getElementById('pitchDot3');
  const dot4 = document.getElementById('pitchDot4');
  const dots = [dot1, dot2, dot3, dot4];

  data.dots.forEach((dotData, idx) => {
    if (dots[idx]) {
      dots[idx].setAttribute('cx', dotData.cx);
      dots[idx].setAttribute('cy', dotData.cy);
      dots[idx].setAttribute('fill', dotData.fill);
      if (dotData.stroke) {
        dots[idx].setAttribute('stroke', dotData.stroke);
      }
    }
  });
}

function playActiveScenarioAudio() {
  const audioSrc = AUDIO_FILES[currentScenarioKey];
  const lang = getPageLanguage();
  const data = SCENARIO_DATA[lang][currentScenarioKey];
  const waveContainer = document.getElementById('waveformContainer');
  const playLabelEl = document.getElementById('appPlayLabel');
  const playIconEl = document.getElementById('appPlayIcon');

  if (activeAudio) {
    activeAudio.pause();
    activeAudio.currentTime = 0;
    activeAudio = null;
    if (waveContainer) waveContainer.classList.remove('is-playing');
    if (playLabelEl) playLabelEl.textContent = data.playBtnDefault;
    if (playIconEl) playIconEl.textContent = '▶';
    return;
  }

  activeAudio = new Audio(audioSrc);
  if (waveContainer) waveContainer.classList.add('is-playing');
  if (playLabelEl) playLabelEl.textContent = data.playBtnPlaying;
  if (playIconEl) playIconEl.textContent = '■';

  activeAudio.play().catch(e => {
    console.log('Audio autoplay prevented:', e);
  });

  activeAudio.onended = function() {
    activeAudio = null;
    if (waveContainer) waveContainer.classList.remove('is-playing');
    if (playLabelEl) playLabelEl.textContent = data.playBtnDefault;
    if (playIconEl) playIconEl.textContent = '▶';
  };
}

function filterAcademy(category) {
  // Update button active state
  document.querySelectorAll('.filter-pill').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-filter') === category);
  });

  // Filter video cards
  document.querySelectorAll('.video-card-item').forEach(card => {
    const cardCat = card.getAttribute('data-category');
    if (category === 'all' || cardCat === category) {
      card.style.display = 'flex';
    } else {
      card.style.display = 'none';
    }
  });
}

// Initializations on DOM Load
document.addEventListener('DOMContentLoaded', () => {
  updateTokyoClock();
  setInterval(updateTokyoClock, 1000);
});
