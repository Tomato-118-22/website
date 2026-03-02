// 言語切り替えメニューの表示・非表示を切り替える関数
function toggleMenu() {
  const menu = document.getElementById("menu");
  if (menu.style.display === "block") {
    menu.style.display = "none";
  } else {
    menu.style.display = "block";
  }
}

// クリックでメニュー以外をクリックしたときにメニューを非表示にする処理
document.addEventListener("click", function(event) {
  const menu = document.getElementById("menu");
  const button = document.querySelector(".menu-button");
  if (event.target !== menu && event.target !== button && !menu.contains(event.target)) {
    menu.style.display = "none";
  }
});