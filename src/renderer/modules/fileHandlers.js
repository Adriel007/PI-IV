import { showAlert } from "./alerts.js";

const setupFileHandlers = () => {
  document.getElementById("connect-remote-btn").onclick = () => {
    Swal.fire(
      "Atenção",
      "Conexão com planilhas remotas ainda não implementada.",
      "info"
    );
  };

  document.getElementById("load-local-btn").onclick = () => {
    const fileInput = document.getElementById("file-input");
    const file = fileInput.files[0];

    // EXAMPLE ////////////////////////////////////////
    const fileAreaInput = document.getElementById("multi-file-input");
    if (fileAreaInput.files.length > 0) {
      const fileArea = fileAreaInput.files[0];
      const multiReader = new FileReader();

      multiReader.readAsText(fileArea);
    }
    //////////////////////////////////////////////////

    if (!file) {
      showAlert("Nenhum arquivo selecionado.", "error");
      return;
    }
    const reader = new FileReader();
    reader.onload = (event) => {
      // const fileContent = event.target.result;
      showAlert("Arquivo carregado com sucesso!");
    };

    reader.onerror = () => {
      showAlert("Erro ao ler o arquivo.", "error");
    };

    reader.readAsText(file);
  };

  document.getElementById("remove-btn").onclick = () => {
    const fileInput = document.getElementById("file-input");
    fileInput.value = "";
    showAlert("Arquivo removido com sucesso!");
  };

  const uploadAreaBtn = document.getElementById("toggle-upload-btn");
  uploadAreaBtn.onclick = () => {
    const uploadArea = document.getElementById("multi-upload-area");
    const icon = uploadAreaBtn.querySelector("i");

    if (icon.classList.contains("bi-eye-slash")) {
      icon.classList.remove("bi-eye-slash");
      icon.classList.add("bi-eye");
      uploadArea.classList.toggle("hidden");
    } else {
      icon.classList.add("bi-eye-slash");
      icon.classList.remove("bi-eye");
      uploadArea.classList.add("hidden");
    }
  };
};

export { setupFileHandlers };
