const setupIpcHandlers = () => {
  // Botão "Análise IA" - pede cálculo real via Python
  document
    .querySelector("#analise-content button.bg-indigo-600")
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

        try {
          Swal.fire({
            title: "Analisando IA...",
            text: "Aguarde enquanto processamos os dados.",
            allowOutsideClick: false,
            didOpen: () => Swal.showLoading(),
          });

          const result = await window.api.analisarDados(csvContent);

          Swal.close();

          plotChartIA(result);
        } catch (error) {
          showAlert(`Falha ao analisar com IA: ${error.message}`, "error");
        }
      };

      reader.readAsText(file);
    });

  // Botão "Gerar Gráficos" - histórico + previsão simples no front
  document
    .querySelector("#analise-content button.bg-yellow-600")
    .addEventListener("click", () => {
      const fileInput = document.getElementById("file-input");
      const file = fileInput.files[0];

      if (!file) {
        showAlert("Nenhum arquivo selecionado.", "error");
        return;
      }

      const reader = new FileReader();
      reader.onload = (event) => {
        const csvContent = event.target.result;
        const data = parseCSV(csvContent);

        if (!validateData(data)) {
          showAlert(
            "Dados inválidos. Verifique as colunas obrigatórias.",
            "error"
          );
          return;
        }

        const processedData = processData(data);
        const predictionData = predictFuture(processedData);
        plotChart(predictionData);
      };

      reader.onerror = () => {
        showAlert("Erro ao ler o arquivo.", "error");
      };

      reader.readAsText(file);
    });
};
