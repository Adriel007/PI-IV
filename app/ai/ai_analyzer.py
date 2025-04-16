import openai
from typing import Dict, Any
import os
from dotenv import load_dotenv
class AIAnalyzer:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Inicializa o analisador de IA.
        
        Args:
            api_key (str): API key para o serviço de IA
            model (str): Nome do modelo a ser usado
        """
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key
    def analyze_data(self,str, Any], prompt: str = None) -> str:
        """
        Analisa os dados usando o modelo de IA configurado.
        
        Args:
            data (Dict[str, Any]): Dados para análise
            prompt (str, optional): Prompt personalizado para a análise
            
        Returns:
            str: Resultado da análise
        """
        try:
            default_prompt = """
            Analise os seguintes dados de evasão escolar e forneça:
            1. Principais tendências identificadas
            2. Possíveis causas de evasão
            3. Recomendações para redução da evasão
            
            Dados:
            {data}
            """
            
            final_prompt = prompt if prompt else default_prompt.format(data=str(data))
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise educacional."},
                    {"role": "user", "content": final_prompt}
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Erro na análise de IA: {str(e)}")