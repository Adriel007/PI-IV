import {
  parseCSV,
  validateData,
  processData,
  predictFuture,
} from "./dataProcessing.js";
import { showAlert } from "./alerts.js";
import { plotChartIA, plotChartSingle, showModelInfo } from "./charts.js";

const setupIpcHandlers = () => {
  // Botão "Análise IA"
  document
    .querySelector("#analise-content button.bg-yellow-600")
    .addEventListener("click", async () => {
      const fileInput = document.getElementById("file-input");
      const file = fileInput.files[0];

      // EXAMPLE ////////////////////////////////////////
      const fileAreaInput = document.getElementById("multi-file-input");
      if (fileAreaInput.files.length > 0) {
        const fileArea = fileAreaInput.files[0];
        const multiReader = new FileReader();

        multiReader.onload = (event) => {
          // Something with LLM
        };

        multiReader.readAsText(fileArea);
      }
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

        const processedData = processData(data);

        try {
          Swal.fire({
            title: "Processando...",
            text: "Gerando previsões com IA...",
            allowOutsideClick: false,
            didOpen: () => Swal.showLoading(),
          });

          plotChartSingle(data);

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

export { setupIpcHandlers };
