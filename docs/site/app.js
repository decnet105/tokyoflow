// TokyoFlow Interactive Web Audio Demo Engine

const audioPhrases = {
  densha: "まもなく、2番線に山手線内回りがまいります。黄色い点字ブロックの内側までお下がりください。",
  kombini: "お弁当温めますか？レジ袋はご利用ですか？",
  izakaya: "とりあえず生ビール二つ、焼き鳥盛り合わせを塩でお願いします！",
  akiba: "すみません、このフィギュアの未開封品はありますか？"
};

function playWebAudio(key) {
  const text = audioPhrases[key];
  if (!text) return;

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'ja-JP';
    utterance.rate = 0.95;
    utterance.pitch = 1.05;

    // Find Japanese voice
    const voices = window.speechSynthesis.getVoices();
    const jaVoice = voices.find(v => v.lang.startsWith('ja') || v.name.includes('Japanese') || v.name.includes('Otoya') || v.name.includes('Kyoko'));
    if (jaVoice) {
      utterance.voice = jaVoice;
    }

    window.speechSynthesis.speak(utterance);
  } else {
    alert("Audio preview not supported in this browser. Download TokyoFlow iOS app for 4,170+ native human voices!");
  }
}

// Pre-load voices
if ('speechSynthesis' in window) {
  window.speechSynthesis.onvoiceschanged = () => {
    window.speechSynthesis.getVoices();
  };
}
