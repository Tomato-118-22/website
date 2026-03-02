// JSON読み込み
let mapT2S = {};
let mapS2T = {};
let isSimplified = false; // false = 繁体, true = 簡体

// 両方のマップを読み込む
Promise.all([
    fetch("../../../static/zndquake/hanzi_map_t2s.json?v=" + Date.now()).then(r => r.json()),
    fetch("../../../static/zndquake/hanzi_map_s2t.json?v=" + Date.now()).then(r => r.json())
]).then(([t2s, s2t]) => {
    mapT2S = t2s;
    mapS2T = s2t;
}).catch(err => {
    console.error("無法加載變換貼圖。无法加载变换贴图。", err);
});

// 単語対応変換
function convertText(text, map) {
    let result = text;
    const keys = Object.keys(map).sort((a, b) => b.length - a.length);
    for (const key of keys) {
        result = result.split(key).join(map[key]);
    }
    return result;
}

// ページ全体を変換
function convertAllText() {
    const map = isSimplified ? mapS2T : mapT2S;
  
    const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        {
            acceptNode(node) {
                if (!node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
                const p = node.parentNode;
                if (p && (p.tagName === "SCRIPT" || p.tagName === "STYLE")) {
                    return NodeFilter.FILTER_REJECT;
                }
                return NodeFilter.FILTER_ACCEPT;
            }
        }
    );

    let node;
    while ((node = walker.nextNode())) {
        node.nodeValue = convertText(node.nodeValue, map);
    }

    document.title = convertText(document.title, map);
}

// トグル処理
document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("toggleBtn");
  
    btn.addEventListener("click", () => {
        console.log("使用中のmap:", mapT2S);
        convertAllText();
        isSimplified = !isSimplified;
        btn.textContent = isSimplified ? "转换为简体字" : "轉換成繁體字";
    });
});