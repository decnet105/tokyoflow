// TokyoFlow High-End Interactive Audio & Screen Engine
// Powered by Real Tokyo Native Voice Bank Audio

const SCENARIO_DATA = {
  zh: {
    densha: {
      level: "JLPT A2 • 交通实境",
      register: "敬语・站台广播",
      districtIcon: "📍",
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
      playBtnDefault: "试听真人原声音频",
      playBtnPlaying: "正在播放真人原声..."
    },
    kombini: {
      level: "JLPT A1 • 便利店实境",
      register: "接客・礼貌语",
      districtIcon: "🍱",
      districtName: "涩谷中心街 • 7-Eleven",
      jpText: "お弁当温めますか？レジ袋はご利用ですか？",
      romajiText: "Obentō atatamemasu ka? Reji-bukuro wa go-riyō desu ka?",
      translationText: "便当需要帮您加热吗？需要使用塑料购物袋吗？",
      pitchName: "平板型（平直无跌落）",
      pitchPath: "M 10 22 Q 40 8 100 8 L 190 8",
      dots: [
        { cx: 20, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 60, cy: 8, fill: "#BC382C" },
        { cx: 120, cy: 8, fill: "#BC382C" },
        { cx: 180, cy: 8, fill: "#BC382C" }
      ],
      playBtnDefault: "试听真人原声音频",
      playBtnPlaying: "正在播放真人原声..."
    },
    izakaya: {
      level: "JLPT N3 • 昭和居酒屋",
      register: "日常・自然口语",
      districtIcon: "🍺",
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
      playBtnDefault: "试听真人原声音频",
      playBtnPlaying: "正在播放真人原声..."
    },
    akiba: {
      level: "JLPT N2 • 动漫模型店",
      register: "兴趣・流行俗语",
      districtIcon: "🎮",
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
      playBtnDefault: "试听真人原声音频",
      playBtnPlaying: "正在播放真人原声..."
    }
  },
  en: {
    densha: {
      level: "JLPT A2 • TRANSIT",
      register: "Keigo (Honorific)",
      districtIcon: "📍",
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
      playBtnDefault: "Play Native Audio",
      playBtnPlaying: "Playing Native Audio..."
    },
    kombini: {
      level: "JLPT A1 • CONVENIENCE",
      register: "Teineigo (Polite)",
      districtIcon: "🍱",
      districtName: "Shibuya Center-Gai • 7-Eleven",
      jpText: "お弁当温めますか？レジ袋はご利用ですか？",
      romajiText: "Obentō atatamemasu ka? Reji-bukuro wa go-riyō desu ka?",
      translationText: "Would you like your bento microwaved? Do you require a plastic bag?",
      pitchName: "Heiban (Flat / Pitch Plateau)",
      pitchPath: "M 10 22 Q 40 8 100 8 L 190 8",
      dots: [
        { cx: 20, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 60, cy: 8, fill: "#BC382C" },
        { cx: 120, cy: 8, fill: "#BC382C" },
        { cx: 180, cy: 8, fill: "#BC382C" }
      ],
      playBtnDefault: "Play Native Audio",
      playBtnPlaying: "Playing Native Audio..."
    },
    izakaya: {
      level: "JLPT N3 • SHOWA PUB",
      register: "Tameguchi (Casual)",
      districtIcon: "🍺",
      districtName: "Omoide Yokocho • Yakitori Alley",
      jpText: "とりあえず生ビール二つ、焼き鳥盛り合わせ塩で！",
      romajiText: "Toriaezu nama biiru futatsu, yakitori moriawase shio de!",
      translationText: "Two draft beers to start, and an assorted yakitori platter with salt!",
      pitchName: "Atamadaka (Head-High Initial Drop)",
      pitchPath: "M 10 6 Q 40 22 100 22 L 190 22",
      dots: [
        { cx: 20, cy: 6, fill: "#BC382C" },
        { cx: 60, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 120, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 180, cy: 22, fill: "#fff", stroke: "#BC382C" }
      ],
      playBtnDefault: "Play Native Audio",
      playBtnPlaying: "Playing Native Audio..."
    },
    akiba: {
      level: "JLPT N2 • POP CULTURE",
      register: "Colloquial (Slang)",
      districtIcon: "🎮",
      districtName: "Radio Kaikan • Akihabara",
      jpText: "すみません、この限定フィギュアの未開封品は在庫ありますか？",
      romajiText: "Sumimasen, kono gentei figyua no mikaihin wa zaiko arimasu ka?",
      translationText: "Excuse me, do you have an unopened stock of this limited figure?",
      pitchName: "Odaka (Tail-High Final Drop)",
      pitchPath: "M 10 22 Q 60 8 150 8 T 190 22",
      dots: [
        { cx: 20, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 70, cy: 8, fill: "#BC382C" },
        { cx: 140, cy: 8, fill: "#BC382C" },
        { cx: 185, cy: 22, fill: "#fff", stroke: "#BC382C" }
      ],
      playBtnDefault: "Play Native Audio",
      playBtnPlaying: "Playing Native Audio..."
    }
  }
};

let currentScenarioKey = 'densha';
let isPlayingAudio = false;
let currentAudioInstance = null;

function getLang() {
  const htmlLang = document.documentElement.lang || 'zh';
  return htmlLang.startsWith('en') ? 'en' : 'zh';
}

// Live Tokyo JST Clock
function updateTokyoClock() {
  const clockEl = document.getElementById('tokyo-clock');
  if (!clockEl) return;
  
  const now = new Date();
  const tokyoTime = new Intl.DateTimeFormat('en-US', {
    timeZone: 'Asia/Tokyo',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  }).format(now);

  clockEl.textContent = `TOKYO ${tokyoTime} JST`;
}

setInterval(updateTokyoClock, 1000);
updateTokyoClock();

// Switch Scenario Tab
function switchScenario(key) {
  const lang = getLang();
  const scenario = SCENARIO_DATA[lang][key];
  if (!scenario) return;

  // Stop active audio when switching tabs
  if (currentAudioInstance) {
    currentAudioInstance.pause();
    currentAudioInstance.currentTime = 0;
  }
  isPlayingAudio = false;
  const waveformContainer = document.getElementById('waveformContainer');
  const playIcon = document.getElementById('appPlayIcon');
  const playLabel = document.getElementById('appPlayLabel');
  if (waveformContainer) waveformContainer.classList.remove('is-playing');
  if (playIcon) playIcon.textContent = "▶";
  if (playLabel) playLabel.textContent = scenario.playBtnDefault;

  currentScenarioKey = key;

  // Update tabs highlight
  document.querySelectorAll('.scenario-tab').forEach(tab => {
    tab.classList.toggle('active', tab.getAttribute('data-scenario') === key);
  });

  // Update in-phone UI
  const levelEl = document.getElementById('appLevel');
  const regEl = document.getElementById('appRegister');
  const distIconEl = document.getElementById('appDistrictIcon');
  const distNameEl = document.getElementById('appDistrictName');
  const jpEl = document.getElementById('appJpText');
  const romajiEl = document.getElementById('appRomajiText');
  const enEl = document.getElementById('appEnText');
  const pitchNameEl = document.getElementById('pitchPatternName');

  if (levelEl) levelEl.textContent = scenario.level;
  if (regEl) regEl.textContent = scenario.register;
  if (distIconEl) distIconEl.textContent = scenario.districtIcon;
  if (distNameEl) distNameEl.textContent = scenario.districtName;
  if (jpEl) jpEl.textContent = scenario.jpText;
  if (romajiEl) romajiEl.textContent = scenario.romajiText;
  if (enEl) enEl.textContent = scenario.translationText;
  if (pitchNameEl) pitchNameEl.textContent = scenario.pitchName;

  // Update Pitch Accent SVG
  const path = document.getElementById('pitchPath');
  if (path) path.setAttribute('d', scenario.pitchPath);

  scenario.dots.forEach((dot, idx) => {
    const dotEl = document.getElementById(`pitchDot${idx + 1}`);
    if (dotEl) {
      dotEl.setAttribute('cx', dot.cx);
      dotEl.setAttribute('cy', dot.cy);
      dotEl.setAttribute('fill', dot.fill);
      if (dot.stroke) {
        dotEl.setAttribute('stroke', dot.stroke);
      } else {
        dotEl.removeAttribute('stroke');
      }
    }
  });
}

// Play Real Recorded Native Audio File
function playActiveScenarioAudio() {
  const lang = getLang();
  const scenario = SCENARIO_DATA[lang][currentScenarioKey];
  if (!scenario) return;

  const waveformContainer = document.getElementById('waveformContainer');
  const playIcon = document.getElementById('appPlayIcon');
  const playLabel = document.getElementById('appPlayLabel');

  if (isPlayingAudio && currentAudioInstance) {
    currentAudioInstance.pause();
    currentAudioInstance.currentTime = 0;
    isPlayingAudio = false;
    if (waveformContainer) waveformContainer.classList.remove('is-playing');
    if (playIcon) playIcon.textContent = "▶";
    if (playLabel) playLabel.textContent = scenario.playBtnDefault;
    return;
  }

  // Load actual native voice recording
  const audioPath = `/assets/audio/${currentScenarioKey}.mp3`;
  const audio = new Audio(audioPath);
  currentAudioInstance = audio;

  audio.onplay = () => {
    isPlayingAudio = true;
    if (waveformContainer) waveformContainer.classList.add('is-playing');
    if (playIcon) playIcon.textContent = "⏹";
    if (playLabel) playLabel.textContent = scenario.playBtnPlaying;
  };

  audio.onended = () => {
    isPlayingAudio = false;
    if (waveformContainer) waveformContainer.classList.remove('is-playing');
    if (playIcon) playIcon.textContent = "▶";
    if (playLabel) playLabel.textContent = scenario.playBtnDefault;
  };

  audio.onerror = () => {
    // Fallback if browser audio policy blocks local mp3
    fallbackSpeech(scenario.jpText, scenario);
  };

  audio.play().catch(() => {
    fallbackSpeech(scenario.jpText, scenario);
  });
}

function fallbackSpeech(text, scenario) {
  const waveformContainer = document.getElementById('waveformContainer');
  const playIcon = document.getElementById('appPlayIcon');
  const playLabel = document.getElementById('appPlayLabel');

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'ja-JP';
    utterance.rate = 0.95;

    utterance.onstart = () => {
      isPlayingAudio = true;
      if (waveformContainer) waveformContainer.classList.add('is-playing');
      if (playIcon) playIcon.textContent = "⏹";
      if (playLabel) playLabel.textContent = scenario.playBtnPlaying;
    };

    utterance.onend = () => {
      isPlayingAudio = false;
      if (waveformContainer) waveformContainer.classList.remove('is-playing');
      if (playIcon) playIcon.textContent = "▶";
      if (playLabel) playLabel.textContent = scenario.playBtnDefault;
    };

    window.speechSynthesis.speak(utterance);
  }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  switchScenario('densha');
});
