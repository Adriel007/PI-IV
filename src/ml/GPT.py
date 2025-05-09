import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Função para configurar o Chrome em modo headless
def configure_driver():
    options = Options()
    options.add_argument("--headless=new")  # usar --headless=new para compatibilidade moderna
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")  # define tamanho da janela virtual
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Especifique o caminho do Chrome no Docker
    options.binary_location = "/usr/bin/google-chrome-stable"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Função para navegar até o site e aguardar a presença do campo
def navigate_to_site(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 30)  # Aumenta o tempo de espera

    try:
        # Espera até que o ID 'prompt-textarea' esteja presente na página
        wait.until(EC.presence_of_element_located((By.ID, "prompt-textarea")))
        print("Elemento encontrado!")
    except TimeoutException:
        print("Elemento 'prompt-textarea' não encontrado no tempo limite.")
        # Adicione mais lógica de recuperação, como verificar outro elemento ou tentar novamente


# Função para inserir texto no campo 'contenteditable'
def enter_text(driver, texto):
    driver.execute_script("""
        const el = document.querySelector("[contenteditable='true']");
        el.focus();
        el.textContent = arguments[0];
        el.dispatchEvent(new Event('input', { bubbles: true }));
    """, texto)

# Função para clicar no botão de envio
def click_submit_button(driver):
    wait = WebDriverWait(driver, 15)
    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "composer-submit-button")))
    submit_button.click()

# Função para esperar até que a resposta apareça
def wait_for_response(driver, timeout=15):
    WebDriverWait(driver, timeout).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, ".text-base")) > 1
    )

# Função para extrair mensagens de prompts e respostas
def extract_messages(driver):
    mensagens = driver.execute_script('''
        return Array.from(document.querySelectorAll(".text-base")).map(el => el.textContent);
    ''')
    
    prompts = [mensagens[i] for i in range(0, len(mensagens), 2)]
    respostas = [mensagens[i] for i in range(1, len(mensagens), 2)]
    
    return prompts, respostas

# Função para exibir os resultados
def display_results(prompts, respostas):
    print("Prompts do usuário:")
    for p in prompts:
        print("-", p.strip())

    print("\nRespostas do sistema:")
    for r in respostas:
        print("-", r.strip())

# Função principal para coordenar as ações
def main():
    driver = configure_driver()
    
    try:
        # Acessa o site e aguarda o carregamento
        navigate_to_site(driver, "https://chatgpt.com")
        
        # Insere o texto
        texto = "Olá, isto é um teste!"
        enter_text(driver, texto)
        
        # Clica no botão de envio
        click_submit_button(driver)
        
        # Espera pela resposta
        wait_for_response(driver)
        
        # Extrai as mensagens
        prompts, respostas = extract_messages(driver)
        
        # Exibe os resultados
        display_results(prompts, respostas)
    
    finally:
        driver.quit()

# Executa o script
if __name__ == "__main__":
    main()
