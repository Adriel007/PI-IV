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
  scripts.forEach((script) => {
    const scriptElement = document.createElement("script");
    scriptElement.src = `./modules/${script}.js`;
    document.body.appendChild(scriptElement);
  });

  document.getElementById("loading").classList.add("hidden");
  document.getElementById("container").classList.remove("hidden");
});
