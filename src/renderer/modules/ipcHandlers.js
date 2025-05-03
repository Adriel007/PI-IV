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

        descritiveAnalysis(data);

        const processedData = processData(data); // ← processa antes!

        try {
          Swal.fire({
            title: "Processando...",
            text: "Gerando previsões com IA...",
            allowOutsideClick: false,
            didOpen: () => Swal.showLoading(),
          });

          const predictionData = await predictFuture(processedData);

          plotChartIA(predictionData);

          showModelInfo(predictionData.modelInfo);
        } catch (error) {
          showAlert(`Erro ao gerar previsões: ${error.message}`, "error");
        }
      };

      reader.onerror = () => {
        showAlert("Erro ao ler o arquivo.", "error");
      };

      reader.readAsText(file);
    });
};
