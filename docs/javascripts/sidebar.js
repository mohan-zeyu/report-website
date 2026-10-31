(() => {
  const sidebar = document.querySelector(".md-sidebar--primary");
  const toggle = document.querySelector(".wiki-sidebar-toggle");
  if (!sidebar || !toggle) return;

  const root = document.documentElement;
  const desktop = window.matchMedia("(min-width: 76.25em)");
  sidebar.id = "wiki-sidebar";

  function isOpen() {
    return !root.classList.contains("wiki-sidebar-collapsed");
  }

  function update() {
    const open = isOpen();
    const label = open ? "Hide sidebar" : "Show sidebar";
    toggle.setAttribute("aria-label", label);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.title = label;
    sidebar.inert = desktop.matches && !open;
  }

  function setOpen(open) {
    root.classList.toggle("wiki-sidebar-collapsed", !open);
    update();
    window.dispatchEvent(new Event("resize"));
  }

  toggle.addEventListener("click", () => setOpen(!isOpen()));
  desktop.addEventListener("change", update);

  update();
  toggle.hidden = false;
})();
