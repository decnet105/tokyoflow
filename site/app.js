// TokyoFlow High-End Interactive Audio & Screen Engine

const SCENARIOS = {
  densha: {
    level: "JLPT A2 • TRANSIT",
    register: "敬語 (Keigo)",
    districtIcon: "📍",
    districtName: "Shinjuku Station • Track 2",
    jpText: "まもなく、2番線に山手線がまいります。黄色い点字ブロックの内側までお下がりください。",
    romajiText: "Mamonaku, ni-ban-sen ni Yamanote-sen ga mairimasu.",
    enText: "The Yamanote Line train will soon arrive at Track 2. Please wait behind the yellow line.",
    pitchName: "中高型 (Nakadaka)",
    pitchPath: "M 10 20 Q 50 5 100 8 T 190 22",
    dots: [
      { cx: 20, cy: 18, fill: "#fff", stroke: "#f43f5e" },
      { cx: 70, cy: 8, fill: "#f43f5e" },
      { cx: 130, cy: 12, fill: "#f43f5e" },
      { cx: 180, cy: 22, fill: "#fff", stroke: "#f43f5e" }
    ],
    speechText: "まもなく、にばんせんにやまのてせんがまいります。きいろいてんじぶろっくのうちがわまでおさがりください。"
  },
  kombini: {
    level: "JLPT A1 • CONVENIENCE",
    register: "接客・丁寧語 (Teineigo)",
    districtIcon: "🍱",
    districtName: "Shibuya Center-Gai • 7-Eleven",
    jpText: "お弁当温めますか？レジ袋はご利用ですか？",
    romajiText: "Obentō atatamemasu ka? Reji-bukuro wa go-riyō desu ka?",
    enText: "Would you like your bento microwaved? Do you require a plastic bag?",
    pitchName: "平板型 (Heiban)",
    pitchPath: "M 10 22 Q 40 8 100 8 L 190 8",
    dots: [
      { cx: 20, cy: 22, fill: "#fff", stroke: "#f43f5e" },
      { cx: 60, cy: 8, fill: "#f43f5e" },
      { cx: 120, cy: 8, fill: "#f43f5e" },
      { cx: 180, cy: 8, fill: "#f43f5e" }
    ],
    speechText: "おべんとうあたためますか？れじぶくろはごりようですか？"
  },
  izakaya: {
    level: "JLPT N3 • SHOWA PUB",
    register: "日常・タメ口 (Tameguchi)",
    districtIcon: "🍺",
    districtName: "Omoide Yokocho • Yakitori Alley",
    jpText: "とりあえず生ビール二つ、焼き鳥盛り合わせ塩で！",
    romajiText: "Toriaezu nama biiru futatsu, yakitori moriawase shio de!",
    enText: "Two draft beers to start, and an assorted yakitori platter with salt!",
    pitchName: "頭高型 (Atamadaka)",
    pitchPath: "M 10 6 Q 40 22 100 22 L 190 22",
    dots: [
      { cx: 20, cy: 6, fill: "#f43f5e" },
      { cx: 60, cy: 22, fill: "#fff", stroke: "#f43f5e" },
      { cx: 120, cy: 22, fill: "#fff", stroke: "#f43f5e" },
      { cx: 180, cy: 22, fill: "#fff", stroke: "#f43f5e" }
    ],
    speechText: "とりあえずなまびーるふたつ、やきとりもりあわせしおで！"
  },
  akiba: {
    level: "JLPT N2 • POP CULTURE",
    register: "趣味・口語 (Colloquial)",
    districtIcon: "🎮",
    districtName: "Radio Kaikan • Akihabara",
    jpText: "すみません、この限定フィギュアの未開封品は在庫ありますか？",
    romajiText: "Sumimasen, kono gentei figyua no mikaihin wa zaiko arimasu ka?",
    enText: "Excuse me, do you have an unopened stock of this limited figure?",
    pitchName: "尾高型 (Odaka)",
    pitchPath: "M 10 22 Q 60 8 150 8 T 190 22",
    dots: [
      { cx: 20, cy: 22, fill: "#fff", stroke: "#f43f5e" },
      { cx: 70, cy: 8, fill: "#f43f5e" },
      { cx: 140, cy: 8, fill: "#f43f5e" },
      { cx: 185, cy: 22, fill: "#fff", stroke: "#f43f5e" }
    ],
    speechText: "すみません、このげんていふぃぎゅあのみかいふうひんはざいこありますか？"
  }
};

let currentScenarioKey = 'densha';
let isPlayingAudio = false;

// Initialize Live Tokyo Clock
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
  const scenario = SCENARIOS[key];
  if (!scenario) return;

  currentScenarioKey = key;

  // Update tabs
  document.querySelectorAll('.scenario-tab').forEach(tab => {
    tab.classList.toggle('active', tab.getAttribute('data-scenario') === key);
  });

  // Update in-phone UI
  document.getElementById('appLevel').textContent = scenario.level;
  document.getElementById('appRegister').textContent = scenario.register;
  document.getElementById('appDistrictIcon').textContent = scenario.districtIcon;
  document.getElementById('appDistrictName').textContent = scenario.districtName;
  document.getElementById('appJpText').textContent = scenario.jpText;
  document.getElementById('appRomajiText').textContent = scenario.romajiText;
  document.getElementById('appEnText').textContent = scenario.enText;
  document.getElementById('pitchPatternName').textContent = scenario.pitchName;

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

// Play Audio for Active Scenario
function playActiveScenarioAudio() {
  const scenario = SCENARIOS[currentScenarioKey];
  if (!scenario) return;

  const waveformContainer = document.getElementById('waveformContainer');
  const playIcon = document.getElementById('appPlayIcon');
  const playLabel = document.getElementById('appPlayLabel');

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(scenario.speechText || scenario.jpText);
    utterance.lang = 'ja-JP';
    utterance.rate = 0.95;
    utterance.pitch = currentScenarioKey === 'densha' ? 1.05 : 1.0;

    // Search for Japanese Voice
    const voices = window.speechSynthesis.getVoices();
    const jaVoice = voices.find(v => v.lang.startsWith('ja') || v.name.includes('Japanese') || v.name.includes('Kyoko') || v.name.includes('Otoya') || v.name.includes('Nanami'));
    if (jaVoice) {
      utterance.voice = jaVoice;
    }

    utterance.onstart = () => {
      isPlayingAudio = true;
      if (waveformContainer) waveformContainer.classList.add('is-playing');
      if (playIcon) playIcon.textContent = "⏹";
      if (playLabel) playLabel.textContent = "Playing Cadence...";
    };

    utterance.onend = () => {
      isPlayingAudio = false;
      if (waveformContainer) waveformContainer.classList.remove('is-playing');
      if (playIcon) playIcon.textContent = "▶";
      if (playLabel) playLabel.textContent = "Play Native Audio";
    };

    utterance.onerror = () => {
      isPlayingAudio = false;
      if (waveformContainer) waveformContainer.classList.remove('is-playing');
      if (playIcon) playIcon.textContent = "▶";
      if (playLabel) playLabel.textContent = "Play Native Audio";
    };

    window.speechSynthesis.speak(utterance);
  } else {
    alert("Web Audio speech synthesis preview is not supported by your current browser. Download TokyoFlow iOS app for full 4,170+ native human voices!");
  }
}

// Preload speech synthesis voices
if ('speechSynthesis' in window) {
  window.speechSynthesis.onvoiceschanged = () => {
    window.speechSynthesis.getVoices();
  };
}
