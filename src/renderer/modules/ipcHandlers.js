const setupIpcHandlers = () => {
  // Botão "Análise IA"
  document
    .querySelector("#analise-content button.bg-yellow-600")
    .addEventListener("click", async () => {
      const fileInput = document.getElementById("file-input");
      const file = fileInput.files[0];

      // EXAMPLE ////////////////////////////////////////
      const fileAreaInput = document.getElementById("multi-file-input");
      const fileArea = fileAreaInput.files[0];
      const multiReader = new FileReader();

      multiReader.onload = (event) => {
        const csvContent = event.target.result;
        const data = parseCSVSpecial(csvContent);

        const wordCloud = wordCloudData(
          data,
          "Motivo da escolha do curso (esta questão admite mais de uma resposta):"
        );

        cloudWord(wordCloud);
      };

      multiReader.readAsText(fileArea);
      //////////////////////////////////////////////////

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

        const processedData = processData(data); // ← processa antes!

        try {
          Swal.fire({
            title: "Processando...",
            text: "Gerando previsões com IA...",
            allowOutsideClick: false,
            didOpen: () => Swal.showLoading(),
          });

          plotChartSingle(data);
          plotChart(processedData);

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
