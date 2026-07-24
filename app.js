(function () {
  const STORAGE_KEY = 'dhamma-journal-v2';
  const MEMO_KEY = 'dhamma-memos-v1';
  const COLLECTION_KEY = 'dhamma-collection-v1';
  const CHAPTER_KEY_PREFIX = 'dhamma-chapter-v1-';
  const BACKUP_VERSION = 1;
  const WEEKDAY_NAMES = ['日', '月', '火', '水', '木', '金', '土'];

  const state = {
    collections: [],
    currentCollection: null,
    index: null,
    data: null,
    sharedPracticePath: null,
    scenes: null,
    pathSceneIndex: null,
    selectedPathId: null,
    listShowingPairs: false,
    currentChapter: 1,
    categoryById: new Map(),
    pairsByCategory: new Map(),
    currentCategoryId: null,
    currentIndex: 0,
    journal: loadJournal(),
    memos: loadMemos(),
    memoSaveTimer: null,
    memoStatusTimer: null,
    backupStatusTimer: null,
    importReplaceAll: false,
    copyStatusTimer: null,
  };

  const els = {
    dateLabel: document.getElementById('dateLabel'),
    collectionSelect: document.getElementById('collectionSelect'),
    chapterLabel: document.getElementById('chapterLabel'),
    mapNote: document.getElementById('mapNote'),
    chapterSelect: document.getElementById('chapterSelect'),
    chapterViewIntro: document.getElementById('chapterViewIntro'),
    categoryBadge: document.getElementById('categoryBadge'),
    verseLabel: document.getElementById('verseLabel'),
    observeText: document.getElementById('observeText'),
    actionText: document.getElementById('actionText'),
    quoteText: document.getElementById('quoteText'),
    quoteVerifyLinks: document.getElementById('quoteVerifyLinks'),
    modernVerifyLinks: document.getElementById('modernVerifyLinks'),
    chineseBlock: document.getElementById('chineseBlock'),
    chineseHint: document.getElementById('chineseHint'),
    chineseText: document.getElementById('chineseText'),
    chineseLocus: document.getElementById('chineseLocus'),
    chineseVerifyLinks: document.getElementById('chineseVerifyLinks'),
    chineseCopyBtn: document.getElementById('chineseCopyBtn'),
    navHint: document.getElementById('navHint'),
    categoryGrid: document.getElementById('categoryGrid'),
    sceneResults: document.getElementById('sceneResults'),
    sceneResultsTitle: document.getElementById('sceneResultsTitle'),
    sceneResultsList: document.getElementById('sceneResultsList'),
    chapterGrid: document.getElementById('chapterGrid'),
    pairList: document.getElementById('pairList'),
    pairListToolbar: document.getElementById('pairListToolbar'),
    pairListHeading: document.getElementById('pairListHeading'),
    pairListBackBtn: document.getElementById('pairListBackBtn'),
    logList: document.getElementById('logList'),
    pairCard: document.getElementById('pairCard'),
    pairMemo: document.getElementById('pairMemo'),
    memoStatus: document.getElementById('memoStatus'),
    prevBtn: document.getElementById('prevBtn'),
    nextBtn: document.getElementById('nextBtn'),
    exportBackupBtn: document.getElementById('exportBackupBtn'),
    importMergeBtn: document.getElementById('importMergeBtn'),
    importReplaceBtn: document.getElementById('importReplaceBtn'),
    importBackupInput: document.getElementById('importBackupInput'),
    backupStatus: document.getElementById('backupStatus'),
    copyStatus: document.getElementById('copyStatus'),
    crossroadCard: document.getElementById('crossroadCard'),
    crossroadKicker: document.getElementById('crossroadKicker'),
    crossroadTitle: document.getElementById('crossroadTitle'),
    originTrackLabel: document.getElementById('originTrackLabel'),
    pathTrackLabel: document.getElementById('pathTrackLabel'),
    originTrack: document.getElementById('originTrack'),
    pathTrack: document.getElementById('pathTrack'),
    nidanaKey: document.getElementById('nidanaKey'),
    pathKey: document.getElementById('pathKey'),
    nidanaHere: document.getElementById('nidanaHere'),
    pathHere: document.getElementById('pathHere'),
    crossroadFlow: document.getElementById('crossroadFlow'),
    crossObserve: document.getElementById('crossObserve'),
    crossAction: document.getElementById('crossAction'),
    sourceJumpBtn: document.getElementById('sourceJumpBtn'),
    views: {
      today: document.getElementById('view-today'),
      categories: document.getElementById('view-categories'),
      chapters: document.getElementById('view-chapters'),
      log: document.getElementById('view-log'),
    },
    tabs: document.querySelectorAll('.tab'),
  };

  function loadJournal() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    } catch {
      return {};
    }
  }

  function saveJournal() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state.journal));
  }

  function loadMemos() {
    try {
      return JSON.parse(localStorage.getItem(MEMO_KEY) || '{}');
    } catch {
      return {};
    }
  }

  function saveMemos() {
    localStorage.setItem(MEMO_KEY, JSON.stringify(state.memos));
  }

  function memoStorageKey(pairId) {
    return `${state.currentCollection.id}:${pairId}`;
  }

  function getMemo(pairId) {
    return state.memos[memoStorageKey(pairId)] || '';
  }

  function setMemo(pairId, text) {
    const key = memoStorageKey(pairId);
    const trimmed = text.trim();
    if (trimmed) {
      state.memos[key] = trimmed;
    } else {
      delete state.memos[key];
    }
    saveMemos();
  }

  function showMemoStatus() {
    if (!els.memoStatus) return;
    els.memoStatus.hidden = false;
    clearTimeout(state.memoStatusTimer);
    state.memoStatusTimer = setTimeout(() => {
      if (els.memoStatus) els.memoStatus.hidden = true;
    }, 1500);
  }

  async function copyText(text) {
    if (!text) return false;
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.select();
      const ok = document.execCommand('copy');
      document.body.removeChild(ta);
      return ok;
    }
  }

  function copyPayload(mode) {
    const pair = currentPair();
    if (!pair) return '';

    if (mode === 'observe') {
      const parts = [pair.observe, pair.action].filter(Boolean);
      return parts.join('\n\n');
    }
    if (mode === 'action') return pair.action || '';
    if (mode === 'quote') return pair.quote || '';
    if (mode === 'chinese') {
      const chinese = pair.alignment && pair.alignment.chinese;
      if (!chinese || chinese.status !== 'mapped') return '';
      const parts = [chinese.text, chinese.satLocus && `掲載箇所: ${chinese.satLocus}`, chinese.t210]
        .filter(Boolean);
      return parts.join('\n');
    }
    return '';
  }

  function showCopyStatus(message, isError) {
    if (!els.copyStatus) return;
    els.copyStatus.textContent = message;
    els.copyStatus.hidden = false;
    els.copyStatus.style.color = isError ? '#b45309' : '';
    clearTimeout(state.copyStatusTimer);
    state.copyStatusTimer = setTimeout(() => {
      if (els.copyStatus) els.copyStatus.hidden = true;
    }, 1800);
  }

  async function copyPairField(mode) {
    const text = copyPayload(mode);
    if (!text) {
      showCopyStatus('コピーする文がありません', true);
      return;
    }
    const ok = await copyText(text);
    if (ok) {
      const labels = { observe: '現代語訳', action: '行動', quote: '経典の言葉', chinese: '漢文' };
      showCopyStatus(`${labels[mode] || '文'}をコピーしました`);
    } else {
      showCopyStatus('コピーできませんでした', true);
    }
  }

  function flushMemoSave() {
    const pair = currentPair();
    if (!pair || !els.pairMemo) return;
    clearTimeout(state.memoSaveTimer);
    setMemo(pair.id, els.pairMemo.value);
  }

  function renderMemo(pairId) {
    if (!els.pairMemo) return;
    els.pairMemo.value = getMemo(pairId);
    if (els.memoStatus) els.memoStatus.hidden = true;
  }

  function scheduleMemoSave() {
    const pair = currentPair();
    if (!pair || !els.pairMemo) return;
    clearTimeout(state.memoSaveTimer);
    state.memoSaveTimer = setTimeout(() => {
      setMemo(pair.id, els.pairMemo.value);
      showMemoStatus();
    }, 400);
  }

  function chapterStorageKey() {
    return `${CHAPTER_KEY_PREFIX}${state.currentCollection.id}`;
  }

  function dataUrl(relativePath) {
    return `data/${relativePath}`;
  }

  async function fetchJson(relativePath) {
    const url = dataUrl(relativePath);
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error(`読み込み失敗 (${res.status}): ${relativePath}`);
    }
    try {
      return await res.json();
    } catch {
      throw new Error(`JSON形式エラー: ${relativePath}`);
    }
  }

  function chapterFileUrl(file) {
    if (state.currentCollection.id === 'dhammapada') {
      return dataUrl(file);
    }
    return dataUrl(`${state.currentCollection.id}/${file}`);
  }

  function todayKey() {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  }

  function formatDateLabel() {
    const d = new Date();
    return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日（${WEEKDAY_NAMES[d.getDay()]}）`;
  }

  function dayOfYear() {
    const d = new Date();
    const start = new Date(d.getFullYear(), 0, 0);
    return Math.floor((d - start) / 86400000);
  }

  function defaultChapterId() {
    const saved = Number(localStorage.getItem(chapterStorageKey()));
    const max = state.index.chapters.length;
    if (saved >= 1 && saved <= max) return saved;
    return (dayOfYear() % max) + 1;
  }

  function categoryForToday() {
    const cats = sceneFactors();
    if (!cats.length) {
      const weekday = new Date().getDay();
      return (state.data && state.data.categories || []).find((c) => c.weekday === weekday)
        || (state.data && state.data.categories && state.data.categories[0])
        || { id: 'view', name: '正見' };
    }
    const day = Math.floor(Date.now() / 86400000);
    return cats[day % cats.length];
  }

  function chapterHasPath(pathId) {
    const all = (state.data && state.data.pairs) || [];
    return all.some((p) => pairMatchesPath(p, pathId));
  }

  /** 今日の八正道を優先。その章に該当ペアがなければ、章内にある支へフォールバック */
  function resolvePathForChapter() {
    const preferred = categoryForToday();
    if (chapterHasPath(preferred.id)) return preferred;
    const fallback = sceneFactors().find((cat) => chapterHasPath(cat.id));
    return fallback || preferred;
  }

  function applyPathForChapter() {
    const cat = resolvePathForChapter();
    state.selectedPathId = cat.id;
    state.currentCategoryId = cat.id;
    state.currentIndex = pairIndexForToday(cat.id);
  }

  /** 一覧優先: 章の全ペアを通し番号で見る（八正道分類は後から） */
  function applyChapterBrowse(preferredPairId) {
    state.selectedPathId = null;
    const all = (state.data && state.data.pairs) || [];
    if (preferredPairId) {
      const idx = all.findIndex((p) => p.id === preferredPairId);
      state.currentIndex = idx >= 0 ? idx : 0;
      const pair = all[state.currentIndex];
      state.currentCategoryId = pair ? pair.category : null;
      return;
    }
    if (!all.length) {
      state.currentIndex = 0;
      state.currentCategoryId = null;
      return;
    }
    const day = Math.floor(Date.now() / 86400000);
    state.currentIndex = day % all.length;
    state.currentCategoryId = all[state.currentIndex].category;
  }

  function sceneFactors() {
    if (state.scenes && Array.isArray(state.scenes.factors) && state.scenes.factors.length) {
      return state.scenes.factors.slice().sort((a, b) => (a.order || 0) - (b.order || 0));
    }
    if (state.data && Array.isArray(state.data.categories)) return state.data.categories;
    return [];
  }

  function pathIdToLabel(pathId) {
    const factor = sceneFactors().find((f) => f.id === pathId);
    return factor ? factor.name : pathId;
  }

  function pairMatchesPath(pair, pathId) {
    if (!pair || !pathId) return true;
    if (pair.category === pathId) return true;
    const label = pathIdToLabel(pathId);
    return Array.isArray(pair.pathFactors) && pair.pathFactors.includes(label);
  }

  function currentPairs() {
    const all = (state.data && state.data.pairs) || [];
    if (state.selectedPathId) {
      return all.filter((p) => pairMatchesPath(p, state.selectedPathId));
    }
    // 一覧優先: 八正道フィルタなしのときは章の全ペア
    return all;
  }

  function practicePath() {
    if (state.data && state.data.practicePath) return state.data.practicePath;
    return state.sharedPracticePath || null;
  }

  function practiceNodeForToday() {
    const path = practicePath();
    if (!path || !Array.isArray(path.nodes) || !path.nodes.length) return null;
    if (path.focusNodeId) {
      const focused = path.nodes.find((n) => n.id === path.focusNodeId);
      if (focused) return focused;
    }
    const weekday = new Date().getDay();
    return path.nodes.find((n) => n.weekday === weekday) || path.nodes[0];
  }

  const PATH_LABEL_TO_ID = {
    正見: 'view',
    正思惟: 'intention',
    正語: 'speech',
    正業: 'action',
    正命: 'livelihood',
    正精進: 'effort',
    正念: 'mindfulness',
    正定: 'concentration',
  };

  function pathFactorIdsFromLabels(labels) {
    if (!Array.isArray(labels)) return [];
    return labels
      .map((label) => PATH_LABEL_TO_ID[label] || null)
      .filter(Boolean);
  }

  /** 現在のペアの縁起×八正道を優先。なければ章の focus / 曜日 */
  function practiceNodeForPair(pair) {
    const path = practicePath();
    if (!path || !Array.isArray(path.nodes) || !path.nodes.length) return null;

    if (pair && pair.nidanaId) {
      const base = path.nodes.find((n) => n.id === pair.nidanaId);
      if (base) {
        const pathFactors = Array.isArray(pair.pathFactors) && pair.pathFactors.length
          ? pair.pathFactors
          : base.pathFactors;
        return Object.assign({}, base, {
          pathFactors,
          pathFactorIds: pathFactorIdsFromLabels(pathFactors),
          pathReason: pair.pathReason || base.pathLabel,
        });
      }
    }
    return practiceNodeForToday();
  }

  /** 根拠ペアID: 章内の明示sources → nidanaタグ → 曜日カテゴリの順で解決 */
  function sourceIdsForNode(node) {
    if (!node || !state.data) return [];

    if (Array.isArray(node.sources) && node.sources.length) {
      const found = node.sources.filter((id) => findPairLocation(id));
      if (found.length) return found;
    }

    const tagged = (state.data.pairs || [])
      .filter((p) => p.nidanaId === node.id)
      .map((p) => p.id);
    if (tagged.length) return tagged;

    const category = (state.data.categories || []).find((c) => c.weekday === node.weekday)
      || state.categoryById.get(node.categoryId);
    if (!category) return [];
    return (state.pairsByCategory.get(category.id) || []).map((p) => p.id);
  }

  const ORIGIN_SHORT = {
    contact: '触',
    feeling: '受',
    craving: '欲',
    clinging: '取',
    suffering: '苦',
    release: '離',
    review: '夜',
    // 初転法輪：四諦トラック
    dukkha: '苦',
    samudaya: '集',
    nirodha: '滅',
    magga: '道',
  };

  const PATH_SHORT = {
    view: '見',
    intention: '思',
    speech: '語',
    action: '業',
    livelihood: '命',
    effort: '精',
    mindfulness: '念',
    concentration: '定',
  };

  function renderTrack(container, items, activeIds, shortMap) {
    if (!container) return;
    const active = new Set(activeIds || []);
    container.innerHTML = '';
    items.forEach((item) => {
      const li = document.createElement('li');
      li.className = 'track-item' + (active.has(item.id) ? ' active' : '');
      const label = (shortMap && shortMap[item.id]) || item.label;
      li.innerHTML = `<span class="track-dot" aria-hidden="true"></span><span class="track-name">${label}</span>`;
      if (item.label && label !== item.label) {
        li.title = item.label;
      }
      container.appendChild(li);
    });
  }

  function hidePracticePath() {
    if (els.crossroadCard) els.crossroadCard.hidden = true;
  }

  function renderPracticePath() {
    const path = practicePath();
    const pair = currentPair();
    const node = practiceNodeForPair(pair);
    if (!path || !node || !els.crossroadCard) {
      hidePracticePath();
      return;
    }

    const isFirstTurning = state.currentCollection && state.currentCollection.id === 'dhammacakka';
    const originItems = path.originNodes || path.nodes.map((n) => ({ id: n.id, label: n.nidanaLabel || n.label }));
    const pathItems = path.pathFactors || [];
    const activeOrigin = [node.id];
    // practiceNodeForPair がペアの八正道を node に反映済み
    const activePath = (node.pathFactorIds && node.pathFactorIds.length)
      ? node.pathFactorIds
      : (pathFactorIdsFromLabels(node.pathFactors) || []);

    if (els.crossroadKicker) {
      els.crossroadKicker.textContent = isFirstTurning ? '四諦 × 八正道' : '縁起 × 八正道';
    }
    if (els.originTrackLabel) {
      els.originTrackLabel.textContent = isFirstTurning ? '四諦' : '縁起';
    }
    if (els.pathTrackLabel) {
      els.pathTrackLabel.textContent = '八正道';
    }
    if (els.nidanaKey) {
      els.nidanaKey.textContent = isFirstTurning ? 'いまの四諦' : '自身の縁起の段階';
    }
    if (els.pathKey) {
      els.pathKey.textContent = isFirstTurning ? '道諦（八正道）' : '自身の八正道の対応';
    }
    if (els.crossroadCard) {
      els.crossroadCard.setAttribute(
        'aria-label',
        isFirstTurning ? '四諦と八正道' : '縁起と八正道'
      );
    }
    if (els.originTrack) {
      els.originTrack.setAttribute('aria-label', isFirstTurning ? '四諦の流れ' : '縁起の流れ');
    }

    if (els.crossroadTitle) {
      const short = path.shortTitle || '';
      els.crossroadTitle.textContent = short || '';
    }

    renderTrack(els.originTrack, originItems, activeOrigin, ORIGIN_SHORT);
    renderTrack(els.pathTrack, pathItems, activePath, PATH_SHORT);

    els.crossroadCard.hidden = false;
    if (els.nidanaHere) els.nidanaHere.textContent = node.nidanaLabel || node.label || '';
    if (els.pathHere) {
      const factors = (pair && pair.pathFactors && pair.pathFactors.length)
        ? pair.pathFactors
        : (node.pathFactors || []);
      els.pathHere.textContent = factors.join('・');
    }
    if (els.crossroadFlow) {
      const reason = pair && pair.pathReason
        ? pair.pathReason
        : (node.pathReason || node.pathLabel || '');
      els.crossroadFlow.textContent = reason;
    }
  }

  function findPairLocation(pairId) {
    if (!state.data || !Array.isArray(state.data.pairs)) return null;
    const pair = state.data.pairs.find((p) => p.id === pairId);
    if (!pair) return null;
    const list = state.pairsByCategory.get(pair.category) || [];
    const index = list.findIndex((p) => p.id === pairId);
    if (index < 0) return null;
    return { pair, categoryId: pair.category, index };
  }

  function jumpToSourcePair() {
    const node = practiceNodeForToday();
    const sourceIds = sourceIdsForNode(node);
    if (!sourceIds.length) return;

    const current = currentPair();
    const currentId = current && current.id;
    let nextId = sourceIds[0];
    const pos = sourceIds.indexOf(currentId);
    if (pos >= 0) {
      nextId = sourceIds[(pos + 1) % sourceIds.length];
    }

    const located = findPairLocation(nextId);
    if (!located) return;

    flushMemoSave();
    state.currentCategoryId = located.categoryId;
    state.currentIndex = located.index;
    renderCategories();
    renderPair();
    if (els.pairCard) {
      els.pairCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function pairIndexForToday(categoryId) {
    const pairs = state.selectedPathId
      ? currentPairs()
      : (state.pairsByCategory.get(categoryId) || []);
    if (!pairs.length) return 0;
    const week = Math.floor(Date.now() / (7 * 24 * 60 * 60 * 1000));
    return week % pairs.length;
  }

  function rebuildCategoryMaps() {
    state.categoryById.clear();
    state.pairsByCategory.clear();
    const cats = (state.data && state.data.categories) || sceneFactors();
    cats.forEach((cat) => {
      state.categoryById.set(cat.id, cat);
      state.pairsByCategory.set(cat.id, []);
    });
    ((state.data && state.data.pairs) || []).forEach((pair) => {
      const list = state.pairsByCategory.get(pair.category);
      if (list) list.push(pair);
      // 八正道の複数支にまたがる偈は、各支のバケツにも入れる
      (pair.pathFactors || []).forEach((label) => {
        const fid = PATH_LABEL_TO_ID[label];
        if (!fid || fid === pair.category) return;
        const bucket = state.pairsByCategory.get(fid);
        if (bucket && !bucket.includes(pair)) bucket.push(pair);
      });
    });
  }

  function chapterUnitLabel() {
    return state.currentCollection.chapterLabel || '章';
  }

  function formatChapterSubtitle(meta, data) {
    const unit = chapterUnitLabel();
    const short = data.shortTitle || meta.shortTitle || '';
    const num = meta.sutta ?? meta.id;
    return `第${num}${unit} · ${short}`;
  }

  function updateHeader() {
    const meta = state.index.chapters.find((c) => c.id === state.currentChapter);
    if (!meta || !state.data) return;

    els.chapterLabel.textContent = formatChapterSubtitle(meta, state.data);

    if (els.mapNote) {
      const note = state.data.mapNote || meta.mapNote || '';
      if (note) {
        els.mapNote.textContent = note;
        els.mapNote.hidden = false;
      } else {
        els.mapNote.textContent = '';
        els.mapNote.hidden = true;
      }
    }

    if (els.chapterViewIntro) {
      const count = state.index.chapters.length;
      const unit = chapterUnitLabel();
      if (state.currentCollection.id === 'tipitaka') {
        els.chapterViewIntro.textContent =
          `三藏·五部の全体地図（${count}${unit}）。第1章から順に読むと、一切経の位置が見えます。`;
      } else if (state.currentCollection.id === 'digha') {
        els.chapterViewIntro.textContent =
          `長部34経全体。第1${unit}から第${count}${unit}まで順に読めます。長い説法の集です。`;
      } else if (state.currentCollection.id === 'majjhima') {
        els.chapterViewIntro.textContent =
          `中部152経全体。第1${unit}から第${count}${unit}まで順に読めます。各${unit}は7場面の観察→行動ペアです。`;
      } else if (state.currentCollection.id === 'anguttara') {
        els.chapterViewIntro.textContent =
          `増支部11集全体。一の法から十一の法まで ${count}${unit}。各${unit}35ペアで「今日これ一つ」を選びます。`;
      } else if (state.currentCollection.id === 'samyutta') {
        els.chapterViewIntro.textContent =
          `相応部56相応全体。第1${unit}から第${count}${unit}まで順に読めます。各${unit}35ペアで縁起·蘊·道を学びます。`;
      } else if (state.currentCollection.id === 'khuddaka') {
        els.chapterViewIntro.textContent =
          `小部15経典全体。法句·感興語·本生·譬喩等 ${count}${unit}。各${unit}35ペアで読みます。`;
      } else if (state.currentCollection.id === 'suttanipata') {
        els.chapterViewIntro.textContent =
          `経集5品全体。蛇喩品から彼岸道品まで ${count}${unit}。各${unit}35ペアで読みます。`;
      } else if (state.currentCollection.id === 'dhammacakka') {
        els.chapterViewIntro.textContent =
          `初転法輪（SN56.11）。二辺·中道から四諦·三転まで ${count}${unit}。四諦通しで読みます。`;
      } else {
        els.chapterViewIntro.textContent =
          `全${count}${unit}。${unit}を選ぶと「今日のダンマ」でその${unit}が開きます。`;
      }
    }
  }

  async function loadChapter(chapterId) {
    const meta = state.index.chapters.find((c) => c.id === chapterId);
    if (!meta) return;
    state.data = await fetchJson(
      state.currentCollection.id === 'dhammapada'
        ? meta.file
        : `${state.currentCollection.id}/${meta.file}`
    );
    state.currentChapter = chapterId;
    localStorage.setItem(chapterStorageKey(), String(chapterId));
    rebuildCategoryMaps();
    updateHeader();
    if (els.chapterSelect) els.chapterSelect.value = String(chapterId);
    renderPracticePath();
  }

  function pairRefLabel(pair) {
    if (pair.ref) return pair.ref;
    if (pair.verse != null) return `偈 ${pair.verse}`;
    return '';
  }

  function currentPair() {
    const pairs = currentPairs();
    return pairs[state.currentIndex] || null;
  }

  function normalizeVerifyLinkList(value) {
    if (!value) return [];
    const list = Array.isArray(value) ? value : [value];
    return list.filter((item) => item && item.url);
  }

  function setVerifyLinks(container, items) {
    if (!container) return;
    const list = normalizeVerifyLinkList(items);
    if (!list.length) {
      container.hidden = true;
      container.innerHTML = '';
      return;
    }
    container.hidden = false;
    container.innerHTML = '';
    list.forEach((item, index) => {
      if (index > 0) {
        const sep = document.createElement('span');
        sep.className = 'verify-sep';
        sep.setAttribute('aria-hidden', 'true');
        sep.textContent = '·';
        container.appendChild(sep);
      }
      const a = document.createElement('a');
      a.href = item.url;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.className = 'verify-link';
      a.textContent = item.label || '参考';
      container.appendChild(a);
    });
  }

  function renderSourceLinks(pair) {
    const chapterLinks = state.data && state.data.source && state.data.source.verifyLinks
      ? state.data.source.verifyLinks
      : null;
    const align = pair && pair.alignment ? pair.alignment : null;

    const paliLink = (align && align.pali) || (chapterLinks && (chapterLinks.pali || chapterLinks.classical || chapterLinks.original));
    const modernLink = (align && align.modern) || (chapterLinks && chapterLinks.modern);

    setVerifyLinks(
      els.quoteVerifyLinks,
      paliLink
        ? [{
          label: (align && align.pali && align.pali.source) || (paliLink.label) || 'アラナ精舎',
          url: paliLink.url,
        }]
        : []
    );
    setVerifyLinks(
      els.modernVerifyLinks,
      modernLink
        ? [{
          label: (align && align.modern && align.modern.source) || (modernLink.label) || 'true-buddhism',
          url: modernLink.url,
        }]
        : []
    );

    renderChineseAlignment(align && align.chinese, chapterLinks && chapterLinks.chinese);
  }

  function renderChineseAlignment(chinese, chapterChinese) {
    if (!els.chineseBlock) return;

    if (!chinese) {
      const fallback = normalizeVerifyLinkList(chapterChinese);
      els.chineseBlock.hidden = fallback.length === 0;
      if (els.chineseHint) els.chineseHint.textContent = '';
      if (els.chineseText) {
        els.chineseText.hidden = true;
        els.chineseText.textContent = '';
      }
      if (els.chineseLocus) {
        els.chineseLocus.hidden = true;
        els.chineseLocus.textContent = '';
      }
      if (els.chineseCopyBtn) els.chineseCopyBtn.hidden = true;
      setVerifyLinks(els.chineseVerifyLinks, fallback);
      return;
    }

    els.chineseBlock.hidden = false;

    if (els.chineseHint) {
      if (chinese.status === 'mapped') {
        els.chineseHint.textContent = chinese.note
          || 'パーリ偈と内容対応する漢訳（偈単位）。';
      } else {
        els.chineseHint.textContent = chinese.note
          || 'このパーリ偈に対応する漢訳（T210）は見つかりません。';
      }
    }

    if (els.chineseText) {
      if (chinese.status === 'mapped' && chinese.text) {
        els.chineseText.hidden = false;
        els.chineseText.textContent = chinese.text;
      } else {
        els.chineseText.hidden = true;
        els.chineseText.textContent = '';
      }
    }

    if (els.chineseCopyBtn) {
      els.chineseCopyBtn.hidden = !(chinese.status === 'mapped' && chinese.text);
    }

    if (els.chineseLocus) {
      const locus = chinese.satLocus || '';
      const t210 = chinese.t210 ? `（${chinese.t210}）` : '';
      const pin = chinese.pin ? `${chinese.pin} ` : '';
      const line = [pin + locus + t210].filter(Boolean).join('').trim();
      if (line) {
        els.chineseLocus.hidden = false;
        els.chineseLocus.textContent = `掲載箇所: ${line}`;
      } else {
        els.chineseLocus.hidden = true;
        els.chineseLocus.textContent = '';
      }
    }

    const linkItems = [];
    if (chinese.satUrl) {
      linkItems.push({
        label: chinese.status === 'mapped'
          ? 'SATで該当箇所を見る'
          : 'SAT 法句経・雙要品',
        url: chinese.satUrl,
      });
    }
    if (chinese.mapTableUrl) {
      linkItems.push({
        label: '偈対応表（蘇錦坤）',
        url: chinese.mapTableUrl,
      });
    }
    setVerifyLinks(els.chineseVerifyLinks, linkItems);
  }

  function renderPair() {
    const pair = currentPair();
    const pairs = currentPairs();
    const category = state.categoryById.get(state.currentCategoryId)
      || sceneFactors().find((f) => f.id === state.selectedPathId)
      || sceneFactors().find((f) => pair && f.id === pair.category);

    if (!pair) {
      const pathName = (category && category.name) || pathIdToLabel(state.selectedPathId) || '';
      if (els.categoryBadge) {
        els.categoryBadge.textContent = pathName;
      }
      if (els.verseLabel) els.verseLabel.textContent = '';
      if (els.quoteText) {
        els.quoteText.textContent = pathName
          ? `この章には「${pathName}」に対応するペアがありません。`
          : 'この章に対応するペアは、まだありません。';
      }
      if (els.observeText) els.observeText.textContent = '';
      if (els.actionText) els.actionText.textContent = '';
      if (els.navHint) els.navHint.textContent = `0 / 0`;
      hidePracticePath();
      renderSourceLinks(null);
      return;
    }

    els.categoryBadge.textContent = (category && category.name)
      || pathIdToLabel(state.selectedPathId)
      || (pair.pathFactors && pair.pathFactors[0])
      || '';
    els.verseLabel.textContent = pairRefLabel(pair);
    els.observeText.textContent = pair.observe;
    els.actionText.textContent = pair.action;
    els.quoteText.textContent = pair.quote;
    renderSourceLinks(pair);

    const memoNote = getMemo(pair.id) ? ' · メモあり' : '';
    const sceneNote = state.selectedPathId ? ` · ${pathIdToLabel(state.selectedPathId)}` : '';
    els.navHint.textContent = `${state.currentIndex + 1} / ${pairs.length}${sceneNote} · スワイプ可${memoNote}`;

    renderPracticePath();
    renderMemo(pair.id);
  }

  function markLabel(value) {
    if (value === 'ok') return '○';
    if (value === 'partial') return '△';
    if (value === 'ng') return '×';
    return '—';
  }

  function findPair(pairId, chapterId, collectionId) {
    if (
      collectionId === state.currentCollection.id
      && chapterId === state.currentChapter
      && state.data
    ) {
      return state.data.pairs.find((p) => p.id === pairId);
    }
    return null;
  }

  function collectionName(collectionId) {
    const col = state.collections.find((c) => c.id === collectionId);
    return col ? col.name : collectionId;
  }

  function collectChapterPrefs() {
    const chapters = {};
    for (let i = 0; i < localStorage.length; i += 1) {
      const key = localStorage.key(i);
      if (!key || !key.startsWith(CHAPTER_KEY_PREFIX)) continue;
      const colId = key.slice(CHAPTER_KEY_PREFIX.length);
      const num = Number(localStorage.getItem(key));
      if (num >= 1) chapters[colId] = num;
    }
    return chapters;
  }

  function buildBackup() {
    flushMemoSave();
    return {
      version: BACKUP_VERSION,
      exportedAt: new Date().toISOString(),
      app: 'dhamma',
      journal: state.journal,
      memos: state.memos,
      collection: localStorage.getItem(COLLECTION_KEY),
      chapters: collectChapterPrefs(),
    };
  }

  function isValidBackup(data) {
    if (!data || typeof data !== 'object') return false;
    return !!(data.journal || data.memos || data.collection || data.chapters);
  }

  function showBackupStatus(message, isError) {
    if (!els.backupStatus) return;
    els.backupStatus.textContent = message;
    els.backupStatus.hidden = false;
    els.backupStatus.style.color = isError ? '#b45309' : '';
    clearTimeout(state.backupStatusTimer);
    state.backupStatusTimer = setTimeout(() => {
      if (els.backupStatus) els.backupStatus.hidden = true;
    }, 4000);
  }

  function exportBackup() {
    const data = buildBackup();
    const blob = new Blob([`${JSON.stringify(data, null, 2)}\n`], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `dhamma-backup-${todayKey()}.json`;
    link.click();
    URL.revokeObjectURL(url);
    showBackupStatus('バックアップをダウンロードしました');
  }

  function applyBackup(data, replaceAll) {
    if (!isValidBackup(data)) {
      throw new Error('ダンマアプリのバックアップファイルではありません');
    }

    const journal = data.journal && typeof data.journal === 'object' ? data.journal : {};
    const memos = data.memos && typeof data.memos === 'object' ? data.memos : {};

    if (replaceAll) {
      state.journal = { ...journal };
      state.memos = { ...memos };
      Object.keys(localStorage).forEach((key) => {
        if (key.startsWith(CHAPTER_KEY_PREFIX)) localStorage.removeItem(key);
      });
    } else {
      state.journal = { ...state.journal, ...journal };
      state.memos = { ...state.memos, ...memos };
    }

    saveJournal();
    saveMemos();

    if (data.collection) {
      localStorage.setItem(COLLECTION_KEY, String(data.collection));
    }

    if (data.chapters && typeof data.chapters === 'object') {
      Object.entries(data.chapters).forEach(([colId, chapterId]) => {
        const num = Number(chapterId);
        if (num >= 1) {
          localStorage.setItem(`${CHAPTER_KEY_PREFIX}${colId}`, String(num));
        }
      });
    }
  }

  async function importBackupFile(file, replaceAll) {
    const text = await file.text();
    let data;
    try {
      data = JSON.parse(text);
    } catch {
      throw new Error('JSONを読み取れませんでした');
    }

    applyBackup(data, replaceAll);

    const colId = data.collection || state.currentCollection.id;
    const known = state.collections.some((c) => c.id === colId);
    if (known) {
      await loadCollection(colId);
    }

    showView('today');
    showBackupStatus(replaceAll ? 'すべて置き換えて復元しました' : 'マージして復元しました');
  }

  function renderLog() {
    const keys = Object.keys(state.journal).sort().reverse().slice(0, 14);
    els.logList.innerHTML = '';

    if (!keys.length) {
      els.logList.innerHTML = '<li class="log-item"><p class="log-summary">まだ記録がありません。</p></li>';
      return;
    }

    keys.forEach((key) => {
      const entry = state.journal[key];
      const pair = findPair(entry.pairId, entry.chapter, entry.collection || 'dhammapada');
      const cat = pair ? state.categoryById.get(pair.category) : null;
      const colLabel = collectionName(entry.collection || 'dhammapada');
      const li = document.createElement('li');
      li.className = 'log-item';
      li.innerHTML = `
        <p class="log-date">${key} · ${colLabel}${cat ? ` · ${cat.short}` : ''}</p>
        <p class="log-summary">${pair ? pair.observe : entry.pairId}</p>
        <p class="log-marks">観察 ${markLabel(entry.observe)} / 行動 ${markLabel(entry.action)}</p>
      `;
      els.logList.appendChild(li);
    });
  }

  function renderCategories() {
    els.categoryGrid.innerHTML = '';
    if (els.sceneResults) els.sceneResults.hidden = true;
    if (els.sceneResultsList) els.sceneResultsList.innerHTML = '';

    sceneFactors().forEach((cat) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'cat-btn';
      if (state.selectedPathId === cat.id) btn.classList.add('active-chapter');
      btn.textContent = cat.name;
      const entries = sceneEntriesFor(cat.id);
      if (!entries.length) {
        btn.classList.add('cat-btn-empty');
        btn.title = 'この支のペアはまだありません';
      }
      btn.addEventListener('click', () => {
        state.selectedPathId = cat.id;
        state.currentCategoryId = cat.id;
        renderCategories();
        renderSceneResults(cat);
      });
      els.categoryGrid.appendChild(btn);
    });
  }

  function sceneEntriesFor(pathId) {
    const entries = state.pathSceneIndex
      && state.pathSceneIndex.entries
      && state.pathSceneIndex.entries[pathId];
    return Array.isArray(entries) ? entries : [];
  }

  function renderSceneResults(cat) {
    if (!els.sceneResults || !els.sceneResultsList) return;
    const entries = sceneEntriesFor(cat.id);
    els.sceneResults.hidden = false;
    if (els.sceneResultsTitle) {
      els.sceneResultsTitle.textContent = `${cat.name}の部・章`;
    }
    els.sceneResultsList.innerHTML = '';

    if (!entries.length) {
      const empty = document.createElement('p');
      empty.className = 'scene-empty';
      empty.textContent = 'この支のペアはまだありません（八正道分類はこれから整備します）。';
      els.sceneResultsList.appendChild(empty);
      return;
    }

    const byCollection = new Map();
    entries.forEach((entry) => {
      const key = entry.collectionId;
      if (!byCollection.has(key)) {
        byCollection.set(key, {
          collectionId: entry.collectionId,
          collectionName: entry.collectionName || entry.collectionId,
          chapters: [],
        });
      }
      byCollection.get(key).chapters.push(entry);
    });

    byCollection.forEach((group) => {
      const block = document.createElement('div');
      block.className = 'scene-collection';
      const heading = document.createElement('p');
      heading.className = 'scene-collection-name';
      heading.textContent = `部：${group.collectionName}`;
      block.appendChild(heading);

      group.chapters.forEach((ch) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'cat-btn scene-chapter-btn';
        btn.textContent = `第${ch.chapterId}章 ${ch.shortTitle}\n（${ch.pairCount}ペア）`;
        btn.addEventListener('click', async () => {
          flushMemoSave();
          state.selectedPathId = cat.id;
          state.currentCategoryId = cat.id;
          if (state.currentCollection.id !== ch.collectionId) {
            await loadCollection(ch.collectionId);
          } else if (state.currentChapter !== ch.chapterId) {
            await loadChapter(ch.chapterId);
          }
          state.selectedPathId = cat.id;
          state.currentCategoryId = cat.id;
          state.currentIndex = 0;
          showView('today');
          renderPair();
        });
        block.appendChild(btn);
      });
      els.sceneResultsList.appendChild(block);
    });
  }

  function renderCollectionSelect() {
    if (!els.collectionSelect) return;
    els.collectionSelect.innerHTML = '';
    state.collections.forEach((col) => {
      const opt = document.createElement('option');
      opt.value = col.id;
      opt.textContent = `${col.name}（${col.subtitle}）`;
      els.collectionSelect.appendChild(opt);
    });
    els.collectionSelect.value = state.currentCollection.id;
  }

  function renderChapterSelect() {
    if (!els.chapterSelect) return;
    const unit = chapterUnitLabel();
    els.chapterSelect.innerHTML = '';
    state.index.chapters.forEach((ch) => {
      const opt = document.createElement('option');
      opt.value = String(ch.id);
      const num = ch.sutta ?? ch.id;
      opt.textContent = `第${num}${unit} ${ch.shortTitle}`;
      els.chapterSelect.appendChild(opt);
    });
    els.chapterSelect.value = String(state.currentChapter);
  }

  function truncateText(text, maxLen) {
    const s = String(text || '').replace(/\s+/g, ' ').trim();
    if (s.length <= maxLen) return s;
    return `${s.slice(0, maxLen)}…`;
  }

  function showChapterPicker() {
    state.listShowingPairs = false;
    if (els.chapterGrid) els.chapterGrid.hidden = false;
    if (els.pairList) {
      els.pairList.hidden = true;
      els.pairList.innerHTML = '';
    }
    if (els.pairListToolbar) els.pairListToolbar.hidden = true;
    if (els.chapterViewIntro) els.chapterViewIntro.hidden = false;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function renderPairList() {
    if (!els.pairList) return;
    const meta = state.index.chapters.find((c) => c.id === state.currentChapter);
    const unit = chapterUnitLabel();
    const num = meta ? (meta.sutta ?? meta.id) : state.currentChapter;
    const short = (state.data && state.data.shortTitle) || (meta && meta.shortTitle) || '';
    const pairs = (state.data && state.data.pairs) || [];

    state.listShowingPairs = true;
    if (els.chapterGrid) els.chapterGrid.hidden = true;
    if (els.chapterViewIntro) els.chapterViewIntro.hidden = true;
    if (els.pairListToolbar) els.pairListToolbar.hidden = false;
    if (els.pairListHeading) {
      els.pairListHeading.textContent = `第${num}${unit} ${short}（${pairs.length}）`;
    }

    els.pairList.hidden = false;
    els.pairList.innerHTML = '';
    if (!pairs.length) {
      const empty = document.createElement('li');
      empty.className = 'scene-empty';
      empty.textContent = 'この章のペアはまだありません。';
      els.pairList.appendChild(empty);
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }

    pairs.forEach((pair, index) => {
      const li = document.createElement('li');
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'pair-list-item';
      const metaRow = document.createElement('p');
      metaRow.className = 'pair-list-meta';
      const ref = pairRefLabel(pair) || `No.${index + 1}`;
      const factors = (pair.pathFactors && pair.pathFactors.length)
        ? pair.pathFactors.join('・')
        : (pathIdToLabel(pair.category) || '');
      metaRow.textContent = factors ? `${ref} · ${factors}` : ref;

      const observe = document.createElement('p');
      observe.className = 'pair-list-observe';
      observe.textContent = truncateText(pair.observe, 72);

      const quote = document.createElement('p');
      quote.className = 'pair-list-quote';
      quote.textContent = truncateText(pair.quote, 64);

      btn.appendChild(metaRow);
      btn.appendChild(observe);
      btn.appendChild(quote);
      btn.addEventListener('click', () => openPairFromList(pair.id));
      li.appendChild(btn);
      els.pairList.appendChild(li);
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  /** 一覧の章を押す → 今日のダンマでその章を表示 */
  async function openChapterOnToday(chapterId) {
    flushMemoSave();
    await loadChapter(chapterId);
    applyChapterBrowse();
    renderChapterSelect();
    state.listShowingPairs = false;
    showView('today');
    renderPair();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function openPairFromList(pairId) {
    flushMemoSave();
    applyChapterBrowse(pairId);
    showView('today');
    renderPair();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function renderChapterGrid() {
    if (!els.chapterGrid) return;
    showChapterPicker();
    els.chapterGrid.innerHTML = '';
    const unit = chapterUnitLabel();
    state.index.chapters.forEach((ch) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'cat-btn';
      if (ch.id === state.currentChapter) btn.classList.add('active-chapter');
      const num = ch.sutta ?? ch.id;
      btn.textContent = `第${num}${unit}\n${ch.shortTitle}`;
      btn.addEventListener('click', () => {
        openChapterOnToday(ch.id);
      });
      els.chapterGrid.appendChild(btn);
    });
  }

  function showView(name) {
    Object.entries(els.views).forEach(([key, view]) => {
      if (!view) return;
      const active = key === name;
      view.hidden = !active;
      view.classList.toggle('active', active);
    });
    els.tabs.forEach((tab) => {
      tab.classList.toggle('active', tab.dataset.view === name);
    });
    if (name === 'log') renderLog();
    if (name === 'chapters') {
      if (state.listShowingPairs && state.data) renderPairList();
      else renderChapterGrid();
    }
    if (name === 'categories') renderCategories();
  }

  function movePair(delta) {
    flushMemoSave();
    const pairs = currentPairs();
    if (!pairs.length) return;
    state.currentIndex = (state.currentIndex + delta + pairs.length) % pairs.length;
    renderPair();
  }

  async function loadCollection(collectionId) {
    const col = state.collections.find((c) => c.id === collectionId);
    if (!col) return;

    state.currentCollection = col;
    localStorage.setItem(COLLECTION_KEY, collectionId);

    state.index = await fetchJson(col.indexFile);

    const chapterId = defaultChapterId();
    await loadChapter(chapterId);
    applyChapterBrowse();

    renderCollectionSelect();
    renderChapterSelect();
    renderCategories();
    renderChapterGrid();
    renderPair();
  }

  function bindSwipe() {
    let startX = 0;
    let startY = 0;

    els.pairCard.addEventListener('touchstart', (e) => {
      const t = e.changedTouches[0];
      startX = t.clientX;
      startY = t.clientY;
    }, { passive: true });

    els.pairCard.addEventListener('touchend', (e) => {
      const t = e.changedTouches[0];
      const dx = t.clientX - startX;
      const dy = t.clientY - startY;
      if (Math.abs(dx) < 50 || Math.abs(dx) < Math.abs(dy)) return;
      movePair(dx < 0 ? 1 : -1);
    }, { passive: true });
  }

  function bindEvents() {
    els.prevBtn.addEventListener('click', () => movePair(-1));
    els.nextBtn.addEventListener('click', () => movePair(1));

    els.tabs.forEach((tab) => {
      tab.addEventListener('click', () => showView(tab.dataset.view));
    });

    if (els.collectionSelect) {
      els.collectionSelect.addEventListener('change', async () => {
        flushMemoSave();
        await loadCollection(els.collectionSelect.value);
        showView('today');
      });
    }

    if (els.chapterSelect) {
      els.chapterSelect.addEventListener('change', async () => {
        flushMemoSave();
        await loadChapter(Number(els.chapterSelect.value));
        applyChapterBrowse();
        renderCategories();
        renderChapterGrid();
        renderPair();
      });
    }

    if (els.pairListBackBtn) {
      els.pairListBackBtn.addEventListener('click', () => {
        renderChapterGrid();
      });
    }

    if (els.sourceJumpBtn) {
      els.sourceJumpBtn.addEventListener('click', jumpToSourcePair);
    }

    if (els.pairMemo) {
      els.pairMemo.addEventListener('input', scheduleMemoSave);
      els.pairMemo.addEventListener('blur', () => {
        flushMemoSave();
        showMemoStatus();
      });
    }

    if (els.pairCard) {
      els.pairCard.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-copy]');
        if (!btn) return;
        e.preventDefault();
        copyPairField(btn.dataset.copy);
      });
    }

    if (els.exportBackupBtn) {
      els.exportBackupBtn.addEventListener('click', exportBackup);
    }

    if (els.importMergeBtn && els.importBackupInput) {
      els.importMergeBtn.addEventListener('click', () => {
        state.importReplaceAll = false;
        els.importBackupInput.click();
      });
    }

    if (els.importReplaceBtn && els.importBackupInput) {
      els.importReplaceBtn.addEventListener('click', () => {
        const ok = window.confirm(
          '端末のメモ・振り返り・章の選択をすべて消し、ファイルの内容に置き換えます。よろしいですか？'
        );
        if (!ok) return;
        state.importReplaceAll = true;
        els.importBackupInput.click();
      });
    }

    if (els.importBackupInput) {
      els.importBackupInput.addEventListener('change', async () => {
        const file = els.importBackupInput.files && els.importBackupInput.files[0];
        const replaceAll = state.importReplaceAll;
        els.importBackupInput.value = '';
        if (!file) return;
        try {
          await importBackupFile(file, replaceAll);
        } catch (err) {
          showBackupStatus(err.message || '取り込みに失敗しました', true);
        }
      });
    }

    bindSwipe();
  }

  async function init() {
    els.dateLabel.textContent = formatDateLabel();

    const [collectionsData, sharedPath, scenes, pathSceneIndex] = await Promise.all([
      fetchJson('collections.json'),
      fetchJson('practice/path.json'),
      fetchJson('scenes.json'),
      fetchJson('path-scene-index.json'),
    ]);
    state.sharedPracticePath = sharedPath;
    state.scenes = scenes;
    state.pathSceneIndex = pathSceneIndex;
    state.collections = collectionsData.collections.sort(
      (a, b) => (a.sortOrder ?? 99) - (b.sortOrder ?? 99)
    );

    const savedCollection = localStorage.getItem(COLLECTION_KEY);
    const defaultCollection = state.collections.find((c) => c.id === savedCollection)
      || state.collections.find((c) => c.id === 'dhammapada')
      || state.collections[0];

    await loadCollection(defaultCollection.id);
    bindEvents();
  }

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  }

  init().catch((err) => {
    console.error(err);
    const detail = err && err.message ? `<br><small style="color:#6b7280">${err.message}</small>` : '';
    document.body.innerHTML =
      `<p style="padding:1.5rem;line-height:1.6">データを読み込めませんでした。サーバー経由で開いてください。${detail}</p>`;
  });
})();
