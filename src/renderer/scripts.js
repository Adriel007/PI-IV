import { setupFileHandlers } from "./modules/fileHandlers.js";
import { setupIpcHandlers } from "./modules/ipcHandlers.js";
import { setupTabs, switchTab } from "./modules/tabs.js";

document.addEventListener("DOMContentLoaded", () => {
  switchTab("planilhas");
  setupTabs();
  setupFileHandlers();
  setupIpcHandlers();

  document.getElementById("loading").classList.add("hidden");
  document.getElementById("container").classList.remove("hidden");
});
