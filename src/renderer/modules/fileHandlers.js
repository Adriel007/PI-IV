const setupFileHandlers = () => {
  document
    .getElementById("connect-remote-btn")
    .addEventListener("click", () => {
      Swal.fire(
        "Atenção",
        "Conexão com planilhas remotas ainda não implementada.",
        "info"
      );
    });

  document.getElementById("load-local-btn").addEventListener("click", () => {
    const fileInput = document.getElementById("file-input");
    const file = fileInput.files[0];

    if (!file) {
      showAlert("Nenhum arquivo selecionado.", "error");
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      const fileContent = event.target.result;
      console.log("Conteúdo do arquivo:", fileContent);
      showAlert("Arquivo carregado com sucesso!");
    };

    reader.onerror = () => {
      showAlert("Erro ao ler o arquivo.", "error");
    };

    reader.readAsText(file);
  });

  document.getElementById("remove-btn").addEventListener("click", () => {
    const fileInput = document.getElementById("file-input");
    fileInput.value = "";
    showAlert("Arquivo removido com sucesso!");
  });

  document.getElementById("toggle-upload-btn").addEventListener("click", () => {
    const uploadArea = document.getElementById("upload-area");
    uploadArea.classList.toggle("hidden");
  });
};
