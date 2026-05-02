// Shared nav controller. Loaded by every page in the bundle.
// Behaviour: open the side rail on tablet+ (≥720px); on mobile, the FAB drives
// the bottom-sheet via the <details> element. IntersectionObserver highlights
// the current section in the rail on scroll.
(function () {
  var nav = document.querySelector("details.sidenav");
  if (!nav) return;

  var mq = window.matchMedia("(min-width: 720px)");
  function sync() {
    if (mq.matches) nav.setAttribute("open", "");
    else nav.removeAttribute("open");
  }
  sync();
  mq.addEventListener
    ? mq.addEventListener("change", sync)
    : mq.addListener(sync);

  if (!("IntersectionObserver" in window)) return;

  var sections = Array.from(document.querySelectorAll("main section[id]"));
  var links = nav.querySelectorAll('nav a[href^="#"]');
  var linkMap = new Map();
  links.forEach(function (a) {
    linkMap.set(a.getAttribute("href").slice(1), a);
  });

  function clearAll() {
    links.forEach(function (a) {
      a.removeAttribute("aria-current");
    });
  }

  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          var a = linkMap.get(e.target.id);
          if (a) {
            clearAll();
            a.setAttribute("aria-current", "true");
          }
        }
      });
    },
    { rootMargin: "-40% 0px -55% 0px", threshold: 0 },
  );
  sections.forEach(function (s) {
    io.observe(s);
  });

  nav.addEventListener("click", function (ev) {
    if (ev.target.tagName === "A" && !mq.matches) nav.removeAttribute("open");
  });
})();
