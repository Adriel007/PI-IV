// Configuração inicial
initTheme();
setupThemeToggle();

switchTab("planilhas");
setupTabs();

setupFileHandlers();
setupIpcHandlers();

// Configurações
document.getElementById("save-settings-btn").addEventListener("click", () => {
  const darkModeEnabled = document.getElementById("theme-toggle").checked;
  localStorage.setItem("darkMode", darkModeEnabled);
  showAlert("Configurações salvas.");
});
