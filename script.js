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

  // Форма заявки → готовое сообщение в мессенджер
  var form = document.getElementById("bookingForm");
  var errorEl = document.getElementById("formError");
  var hintEl = document.getElementById("formHint");
  var target = "telegram";

  form.querySelectorAll("[data-send]").forEach(function (btn) {
    btn.addEventListener("click", function () { target = btn.getAttribute("data-send"); });
  });

  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).catch(function () {});
    }
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } catch (e) {}
    document.body.removeChild(ta);
    return Promise.resolve();
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var d = new FormData(form);
    var name = (d.get("name") || "").trim();
    var phone = (d.get("phone") || "").trim();
    if (!name || !phone) {
      errorEl.hidden = false;
      (name ? form.phone : form.name).focus();
      return;
    }
    errorEl.hidden = true;

    var lines = [
      "Здравствуйте! Хочу записаться на тюнинг.",
      "Имя: " + name,
      "Телефон: " + phone
    ];
    var boat = (d.get("boat") || "").trim();
    var comment = (d.get("comment") || "").trim();
    if (boat) lines.push("Лодка: " + boat);
    lines.push("Услуга: " + d.get("service"));
    if (comment) lines.push("Комментарий: " + comment);
    var message = lines.join("\n");

    // Открываем окно синхронно, чтобы браузер не заблокировал всплывающее окно
    var url = target === "max" ? links.max : links.telegram;
    var win = url ? window.open(url, "_blank") : null;
    if (win) { try { win.opener = null; } catch (err) {} }
    copy(message).then(function () {
      hintEl.hidden = false;
      if (!win && url) window.location.href = url;
    });
  });
})();
