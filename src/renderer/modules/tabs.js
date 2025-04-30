// Alternar entre abas
const switchTab = (tabName) => {
  // Esconder todos os conteúdos
  document.getElementById("planilhas-content").classList.add("hidden");
  document.getElementById("analise-content").classList.add("hidden");
  document.getElementById("config-content").classList.add("hidden");

  // Remover borda inferior de todas as abas
  document
    .getElementById("planilhas-tab")
    .classList.remove("border-b-2", "border-red-600");
  document
    .getElementById("analise-tab")
    .classList.remove("border-b-2", "border-red-600");
  document
    .getElementById("config-tab")
    .classList.remove("border-b-2", "border-red-600");

  // Mostrar o conteúdo selecionado e destacar a aba
  document.getElementById(`${tabName}-content`).classList.remove("hidden");
  document
    .getElementById(`${tabName}-tab`)
    .classList.add("border-b-2", "border-red-600");
};

const setupTabs = () => {
  document
    .getElementById("planilhas-tab")
    .addEventListener("click", () => switchTab("planilhas"));
  document
    .getElementById("analise-tab")
    .addEventListener("click", () => switchTab("analise"));
  document
    .getElementById("config-tab")
    .addEventListener("click", () => switchTab("config"));
};
