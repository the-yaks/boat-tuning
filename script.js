(function () {
  var C = window.SITE_CONFIG || {};
  var tgUrl = C.telegram ? "https://t.me/" + C.telegram.replace(/^@/, "") : null;

  var links = {
    phone: C.phoneDial ? "tel:" + C.phoneDial : null,
    telegram: tgUrl,
    max: C.maxUrl || null
  };
  var texts = {
    phone: C.phoneDisplay,
    telegram: C.telegram ? "@" + C.telegram.replace(/^@/, "") : null,
    max: C.maxLabel,
    address: C.address,
    hours: C.hours
  };

  document.querySelectorAll("[data-contact]").forEach(function (el) {
    var key = el.getAttribute("data-contact");
    if (links[key]) el.setAttribute("href", links[key]);
    if (key === "phone" && el.classList.contains("header__phone") && texts.phone) {
      el.textContent = texts.phone;
    }
  });
  // Неразрывные пробелы: короткие слова и числа не остаются в конце строки
  function typo(t) {
    if (!t) return t;
    t = t.replace(/(^|[\s(«])([А-Яа-яЁёA-Za-z]{1,2}|для|без|под|над|при|про)\s+/g, "$1$2\u00a0");
    t = t.replace(/(^|[\s(«])([А-Яа-яЁёA-Za-z]{1,2}|для|без|под|над|при|про)\s+/g, "$1$2\u00a0");
    t = t.replace(/\s+([—–])/g, "\u00a0$1").replace(/(\d)\s+/g, "$1\u00a0").replace(/(г|ул|д)\.\s+/g, "$1.\u00a0");
    return t;
  }
  if (texts.phone) texts.phone = texts.phone.replace(/\s+/g, "\u00a0");
  ["telegram", "max", "address", "hours"].forEach(function (k) { texts[k] = typo(texts[k]); });

  document.querySelectorAll("[data-contact-text]").forEach(function (el) {
    var key = el.getAttribute("data-contact-text");
    if (texts[key]) el.textContent = texts[key];
  });

  // Год в футере
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  // Мобильное меню
  var burger = document.getElementById("burger");
  var nav = document.getElementById("nav");
  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("is-open");
    burger.classList.toggle("is-open", open);
    burger.setAttribute("aria-expanded", open);
  });
  nav.addEventListener("click", function (e) {
    if (e.target.tagName === "A") {
      nav.classList.remove("is-open");
      burger.classList.remove("is-open");
      burger.setAttribute("aria-expanded", "false");
    }
  });

  // Тень у шапки при прокрутке
  var header = document.querySelector(".header");
  window.addEventListener("scroll", function () {
    header.classList.toggle("is-scrolled", window.scrollY > 10);
  }, { passive: true });
})();
