// Gerenciamento de tema escuro/claro
const initTheme = () => {
  // Verificar preferência salva ou do sistema
  const savedMode = localStorage.getItem("darkMode");
  const systemPrefersDark =
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches;

  const darkMode =
    savedMode === null ? systemPrefersDark : savedMode === "true";

  // Aplicar tema
  if (darkMode) {
    document.body.classList.add("dark");
    document.getElementById("theme-toggle").checked = true;
    document
      .querySelector("#toggle-theme-btn i")
      .classList.replace("bi-moon-fill", "bi-sun-fill");
  } else {
    document.body.classList.remove("dark");
    document.getElementById("theme-toggle").checked = false;
    document
      .querySelector("#toggle-theme-btn i")
      .classList.replace("bi-sun-fill", "bi-moon-fill");
  }

  // Salvar no localStorage
  localStorage.setItem("darkMode", darkMode.toString());
};

const setupThemeToggle = () => {
  const toggleTheme = () => {
    const isDark = document.body.classList.toggle("dark");
    localStorage.setItem("darkMode", isDark.toString());

    const icon = document.querySelector("#toggle-theme-btn i");
    if (isDark) {
      icon.classList.replace("bi-moon-fill", "bi-sun-fill");
      document.getElementById("theme-toggle").checked = true;
    } else {
      icon.classList.replace("bi-sun-fill", "bi-moon-fill");
      document.getElementById("theme-toggle").checked = false;
    }
  };

  // Configurar eventos
  document
    .getElementById("toggle-theme-btn")
    .addEventListener("click", toggleTheme);
  document
    .getElementById("theme-toggle")
    .addEventListener("change", toggleTheme);
};
