const setupSection = document.querySelector('#setup');
const gameSection = document.querySelector('#game');
const endingSection = document.querySelector('#ending');

const partnerInput = document.querySelector('#partnerName');
const startBtn = document.querySelector('#startBtn');
const restartBtn = document.querySelector('#restartBtn');

const dayEl = document.querySelector('#day');
const affectionEl = document.querySelector('#affection');
const energyEl = document.querySelector('#energy');
const sceneTitleEl = document.querySelector('#sceneTitle');
const sceneTextEl = document.querySelector('#sceneText');
const choicesEl = document.querySelector('#choices');
const logEl = document.querySelector('#log');

const endingTitleEl = document.querySelector('#endingTitle');
const endingTextEl = document.querySelector('#endingText');

const scenes = [
  {
    title: 'はじまりの朝',
    text: (name) => `${name}と初めての冒険デート。待ち合わせ前、あなたは最初の行動を選ぶ。`,
    choices: [
      { text: '花を一輪買っていく (+2好感度)', affection: 2, energy: -1, log: '「え、かわいい…！」と笑顔に。' },
      { text: 'ゲームセンター直行 (+1元気)', affection: 0, energy: 1, log: 'テンション高めでスタート！' },
      { text: '寝坊して5分遅刻 (-1好感度)', affection: -1, energy: 0, log: 'ちょっとだけ不機嫌な空気に…。' },
    ],
  },
  {
    title: 'ランチクエスト',
    text: (name) => `${name}が「お腹すいた〜」と言っている。お昼の選択は？`,
    choices: [
      { text: '事前リサーチした人気カフェへ (+2好感度)', affection: 2, energy: -1, log: '「予約までしてくれたの!?」と感動。' },
      { text: '近くのチェーン店でサクッと (+0)', affection: 0, energy: 0, log: '無難においしく食べた。' },
      { text: '自分の食べたい店を優先 (-2好感度)', affection: -2, energy: 0, log: '少し寂しそうな顔をした。' },
    ],
  },
  {
    title: '午後のサイドクエスト',
    text: (name) => `${name}と散歩中、急に雨。どうする？`,
    choices: [
      { text: '傘を買って相合傘 (+2好感度, -1元気)', affection: 2, energy: -1, log: '距離がグッと近づいた。' },
      { text: '雨宿りしながら会話を楽しむ (+1好感度)', affection: 1, energy: 0, log: '普段言えない話ができた。' },
      { text: 'テンションが下がって無言 (-1好感度)', affection: -1, energy: 0, log: '空気が少し重くなった。' },
    ],
  },
  {
    title: '夕暮れイベント',
    text: (name) => `夜景スポットが見えてきた。${name}は少し疲れているみたい。`,
    choices: [
      { text: '休憩して温かい飲み物を買う (+2好感度)', affection: 2, energy: 1, log: '「気が利くね」って褒められた。' },
      { text: 'このまま目的地へ急ぐ (+0好感度)', affection: 0, energy: -1, log: '到着は早いけど、ちょっと疲れた。' },
      { text: '「大丈夫？」と手を握る (+1好感度)', affection: 1, energy: 0, log: '照れながらも嬉しそう。' },
    ],
  },
  {
    title: 'ラストバトル（告白タイム）',
    text: (name) => `${name}との一日も終盤。最後に伝える言葉は？`,
    choices: [
      { text: '「これからも一緒にクエストしよう」 (+2好感度)', affection: 2, energy: 0, log: '最高の笑顔でうなずいてくれた。' },
      { text: '「今日はありがとう！」 (+1好感度)', affection: 1, energy: 0, log: '優しい空気で締めくくれた。' },
      { text: '「また連絡するね」 (+0好感度)', affection: 0, energy: 0, log: '無難なエンディングに。' },
    ],
  },
];

const state = {
  day: 1,
  affection: 0,
  energy: 8,
  partnerName: 'ヒロイン',
};

function resetState() {
  state.day = 1;
  state.affection = 0;
  state.energy = 8;
  state.partnerName = partnerInput.value.trim() || 'ヒロイン';
}

function updateStatus() {
  dayEl.textContent = state.day;
  affectionEl.textContent = state.affection;
  energyEl.textContent = state.energy;
}

function renderScene() {
  const sceneIndex = state.day - 1;
  const scene = scenes[sceneIndex];

  if (!scene || state.energy <= 0 || state.day > scenes.length) {
    renderEnding();
    return;
  }

  sceneTitleEl.textContent = scene.title;
  sceneTextEl.textContent = scene.text(state.partnerName);
  choicesEl.innerHTML = '';
  logEl.textContent = '';

  scene.choices.forEach((choice) => {
    const button = document.createElement('button');
    button.textContent = choice.text;
    button.addEventListener('click', () => choose(choice));
    choicesEl.appendChild(button);
  });

  updateStatus();
}

function choose(choice) {
  state.affection += choice.affection;
  state.energy += choice.energy;
  state.energy = Math.min(10, state.energy);
  logEl.textContent = choice.log;

  setTimeout(() => {
    state.day += 1;
    renderScene();
  }, 700);
}

function renderEnding() {
  gameSection.classList.add('hidden');
  endingSection.classList.remove('hidden');

  if (state.energy <= 0) {
    endingTitleEl.textContent = '💤 バッドエンド：スタミナ切れ';
    endingTextEl.textContent = `${state.partnerName}との冒険は楽しかったけど、体力が尽きてしまった。次はペース配分を大切に！`;
    return;
  }

  if (state.affection >= 8) {
    endingTitleEl.textContent = '👑 トゥルーエンド：恋人ランクS';
    endingTextEl.textContent = `${state.partnerName}は「次のデートも絶対行こうね」と微笑んだ。最高のプレゼント成功！`;
  } else if (state.affection >= 4) {
    endingTitleEl.textContent = '🌸 グッドエンド：恋の仲間';
    endingTextEl.textContent = `${state.partnerName}との距離は確実に縮まった。次のクエストで恋人ランクを目指そう。`;
  } else {
    endingTitleEl.textContent = '🌙 ノーマルエンド：これからの物語';
    endingTextEl.textContent = `${state.partnerName}との冒険はここから。次はもっと気持ちを伝えてみよう。`;
  }
}

startBtn.addEventListener('click', () => {
  resetState();
  setupSection.classList.add('hidden');
  endingSection.classList.add('hidden');
  gameSection.classList.remove('hidden');
  renderScene();
});

restartBtn.addEventListener('click', () => {
  setupSection.classList.remove('hidden');
  gameSection.classList.add('hidden');
  endingSection.classList.add('hidden');
  partnerInput.focus();
});
