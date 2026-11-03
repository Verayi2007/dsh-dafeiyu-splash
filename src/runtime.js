/* ==========================================================================
   开屏运行时：把一段自包含的 DOM 挂进任意宿主节点，按时间轴收幕或跳过。
   DFY_CSS / DFY_BODY 由构建脚本注入（同一份源码同时供预览页与插件使用）。
   ========================================================================== */

var DFY_OPTS = (typeof window !== "undefined" && window.__DAFEIYU_SPLASH__) || {};

function dfyCreateSplash(host, options) {
  var opts = options || {};
  var doc = host.ownerDocument || document;
  var win = doc.defaultView || window;

  var duration = typeof opts.duration === "number" ? opts.duration : 4600;
  var fadeMs = 560;

  var root = doc.createElement("div");
  root.className = "dfy-splash";
  root.setAttribute("data-dafeiyu-splash", "playing");
  root.innerHTML = "<style>" + DFY_CSS + "</style>" + DFY_BODY;

  /* 文案可被逐次覆盖（宿主可以换成自己的名字） */
  var titleEl = root.querySelector(".dfy-title");
  var subEl = root.querySelector(".dfy-sub");
  var hintEl = root.querySelector(".dfy-hint");
  if (opts.title && titleEl) titleEl.textContent = String(opts.title);
  if (opts.subtitle !== undefined && subEl) {
    if (opts.subtitle) subEl.textContent = String(opts.subtitle);
    else subEl.style.display = "none";
  }
  if (opts.hint !== undefined && hintEl) {
    if (opts.hint) hintEl.textContent = String(opts.hint);
    else hintEl.style.display = "none";
  }

  var done = false;
  var timerOut = 0;
  var timerGone = 0;
  var listeners = [];

  function cleanup() {
    win.clearTimeout(timerOut);
    win.clearTimeout(timerGone);
    for (var i = 0; i < listeners.length; i++) {
      var l = listeners[i];
      try {
        l.target.removeEventListener(l.type, l.fn, l.capture);
      } catch (e) {
        /* ignore */
      }
    }
    listeners = [];
  }

  function destroy() {
    if (done) return;
    done = true;
    cleanup();
    root.setAttribute("data-dafeiyu-splash", "done");
    if (root.parentNode) root.parentNode.removeChild(root);
    if (typeof opts.onDone === "function") {
      try {
        opts.onDone();
      } catch (e) {
        /* ignore */
      }
    }
  }

  function leave() {
    if (done) return;
    root.classList.add("dfy-out");
    root.setAttribute("data-dafeiyu-splash", "leaving");
    win.clearTimeout(timerOut);
    win.clearTimeout(timerGone);
    timerGone = win.setTimeout(destroy, fadeMs);
  }

  function skip() {
    if (done || root.classList.contains("dfy-out")) return;
    if (typeof opts.onSkip === "function") {
      try {
        opts.onSkip();
      } catch (e) {
        /* ignore */
      }
    }
    leave();
  }

  function listen(target, type, fn) {
    target.addEventListener(type, fn, { capture: true, passive: true });
    listeners.push({ target: target, type: type, fn: fn, capture: true });
  }

  ["pointerdown", "keydown", "wheel", "touchstart"].forEach(function (type) {
    listen(win, type, skip);
  });

  host.appendChild(root);

  /* 预览页专用：window.__DFY_FREEZE__ = 毫秒 时，把整段动画定格到那一帧，
     同步做完（在首帧绘制之前），这样截图一定是想要的那一帧。 */
  if (typeof win.__DFY_FREEZE__ === "number" && win.__DFY_FREEZE__ > 0) {
    try {
      void root.offsetWidth;
      var anims = doc.getAnimations ? doc.getAnimations() : [];
      for (var i = 0; i < anims.length; i++) {
        try {
          anims[i].currentTime = win.__DFY_FREEZE__;
          anims[i].pause();
        } catch (e) {
          /* ignore */
        }
      }
      root.style.transition = "none";
    } catch (e) {
      /* ignore */
    }
  }

  timerOut = win.setTimeout(leave, duration);
  return { destroy: destroy, skip: skip, root: root };
}
