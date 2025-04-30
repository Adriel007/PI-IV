const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  connectRemoteSpreadsheet: () =>
    ipcRenderer.invoke("connect-remote-spreadsheet"),
  loadLocalSpreadsheet: () => ipcRenderer.invoke("load-local-spreadsheet"),
  removeSpreadsheet: () => ipcRenderer.invoke("remove-spreadsheet"),
  downloadTemplate: () => ipcRenderer.invoke("download-template"),
  saveSettings: () => ipcRenderer.invoke("save-settings"),
});
