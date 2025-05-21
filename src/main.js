const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const { spawn, execSync } = require("child_process");

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: true,
    },
  });

  win.loadFile("src/renderer/index.html");
}

app.whenReady().then(createWindow);

// 📡 IPC para fazer análise IA com Python
ipcMain.handle("analisar-dados", async (event, csvContent) => {
  return new Promise((resolve, reject) => {
    let pythonCmd;
    try {
      pythonCmd = getPythonCommand();
    } catch (err) {
      return reject(err);
    }

    const pythonProcess = spawn(pythonCmd, ["src/ml/analysis.py"], {
      stdio: ["pipe", "pipe", "pipe"],
    });

    let data = "";
    let error = "";

    pythonProcess.stdout.on("data", (chunk) => {
      data += chunk.toString();
    });

    pythonProcess.stderr.on("data", (chunk) => {
      error += chunk.toString();
    });

    pythonProcess.on("close", (code) => {
      if (code === 0) {
        resolve(JSON.parse(data));
      } else {
        reject(new Error(error || `Processo Python saiu com código ${code}`));
      }
    });

    pythonProcess.stdin.write(csvContent);
    pythonProcess.stdin.end();
  });
});

function getPythonCommand() {
  const commands = ["python3", "python", "py"];
  for (const cmd of commands) {
    try {
      const version = execSync(`${cmd} --version`, {
        stdio: "pipe",
      }).toString();
      if (version.toLowerCase().includes("python")) {
        return cmd;
      }
    } catch (e) {
      // comando não disponível, tenta o próximo
    }
  }
  throw new Error("Python não encontrado no sistema.");
}
