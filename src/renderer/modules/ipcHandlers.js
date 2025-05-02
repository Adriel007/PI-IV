const setupIpcHandlers = () => {
  // Botão "Análise IA"
  document
    .querySelector("#analise-content button.bg-yellow-600")
    .addEventListener("click", async () => {
      const fileInput = document.getElementById("file-input");
      const file = fileInput.files[0];

      if (!file) {
        showAlert("Nenhum arquivo selecionado.", "error");
        return;
      }

      const reader = new FileReader();
      reader.onload = async (event) => {
        const csvContent = event.target.result;
        const data = parseCSV(csvContent);

        if (!validateData(data)) {
          showAlert(
            "Dados inválidos. Verifique as colunas obrigatórias.",
            "error"
          );
          return;
        }

        try {
          Swal.fire({
            title: "Processando...",
            text: "Gerando previsões com IA...",
            allowOutsideClick: false,
            didOpen: () => Swal.showLoading(),
          });

          // Chamada real ao backend (via Python)
          const result = await window.electronAPI.analisarDados(csvContent);
          const parsed = JSON.parse(result);

          plotChartIA(parsed);

          showModelInfo({
            bestModel: parsed.best_model,
            metrics: parsed.model_metrics,
          });

          Swal.close();
        } catch (error) {
          Swal.close();
          showAlert(`Erro ao gerar previsões: ${error.message}`, "error");
        }
      };

      reader.onerror = () => {
        showAlert("Erro ao ler o arquivo.", "error");
      };

      reader.readAsText(file);
    });
};
