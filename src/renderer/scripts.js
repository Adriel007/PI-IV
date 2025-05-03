document.addEventListener("DOMContentLoaded", () => {
  const scripts = [
    "alerts",
    "charts",
    "dataProcessing",
    "theme",
    "tabs",
    "fileHandlers",
    "ipcHandlers",
    "config",
  ];

  const loadScript = (src) => {
    return new Promise((resolve, reject) => {
      const scriptElement = document.createElement("script");
      scriptElement.src = `./modules/${src}.js`;
      scriptElement.defer = true;
      scriptElement.onload = resolve;
      scriptElement.onerror = () =>
        reject(new Error(`Erro ao carregar ${src}.js`));
      document.body.appendChild(scriptElement);
    });
  };

  // Aguarda o carregamento de todos os scripts
  Promise.all(scripts.map(loadScript))
    .then(() => {
      // Após o carregamento bem-sucedido de todos os scripts
      document.getElementById("loading").classList.add("hidden");
      document.getElementById("container").classList.remove("hidden");
    })
    .catch((error) => {
      console.error("Erro ao carregar scripts:", error);
      Swal.fire({
        title: "Erro",
        text: "Erro ao carregar scripts da aplicação.",
        icon: "error",
        confirmButtonText: "OK",
      });
    });
});
