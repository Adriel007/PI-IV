const setupIpcHandlers = () => {
  // Botão "Análise IA" - pede cálculo real via Python
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

        const processedData = processData(data);

        try {
          Swal.fire({
            title: "Processando...",
            text: "Gerando previsões",
            allowOutsideClick: false,
            didOpen: () => Swal.showLoading(),
          });

          const predictionData = await predictFuture(processedData);
          plotChart(predictionData);

          Swal.close();

          // Mostra informações do modelo se disponível
          if (predictionData.modelInfo) {
            const modelInfo = predictionData.modelInfo;
            if (!modelInfo) return;

            // Cria um texto formatado com as informações do modelo
            let infoText = `<strong>Modelo utilizado:</strong> ${
              modelInfo.bestModel || "N/A"
            }`;

            if (modelInfo.metrics) {
              infoText += `<br><br><strong>Métricas:</strong>`;
              for (const [modelName, metrics] of Object.entries(
                modelInfo.metrics
              )) {
                infoText += `<br>• ${modelName}: RMSE = ${
                  metrics.cv_rmse?.toFixed(2) || "N/A"
                }`;
              }
            }

            // Mostra as informações usando SweetAlert2
            Swal.fire({
              title: "Informações do Modelo",
              html: infoText,
              icon: "info",
              confirmButtonText: "OK",
            });
          }
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
