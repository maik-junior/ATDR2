#!/usr/bin/env python
# coding: utf-8

# <p style="text-align: center; font-size: 30px; color: navy; font-weight: bold;">
#     Assessment - Coleta de Dados com Python via APIs e WebScraping <br>
#     Maik Júnior dos Santos
# </p>

# ## Parte 1: Docs e Regex

# ### Exercício 1:
# Baixe seu perfil no Linkedin em PDF e utilize o PyPDF2 para construir uma função que retorne a string do texto completo do documento.

# In[1]:


#==> Iportando biblioteca
from PyPDF2 import PdfReader


# In[2]:


#==> lendo .pdf
pdf = PdfReader('../file/Profile.pdf')


# In[3]:


#==> Funcao extrai dados do arquivo pdf
def le_pdf(documento):
    text = '\n\n'.join([x.extract_text() for x in documento.pages])
    return text

#==> Chamando funcao
texto = le_pdf(pdf)
texto = ' '.join(texto.split())
texto


# ---

# ### Exercício 2:
# Utilize Regex (módulo `re` nativo do Python) para criar uma função que, a partir do texto extraído, retorne um dicionário com as seguintes informações: 
# - Seu número de telefone;
# - Seu endereço de email; 
# - O link do seu perfil no Linkedin.

# In[4]:


#==> Importando biblioteca
import re
import csv


# In[5]:


#==> Recuperando nome
nome1 = re.search(r'maik', texto)
nome1[0]


# In[6]:


#== > Recuperando numero de telefone
telefone1 = re.search(r'9\d{4}-?\d{4}', texto)
telefone1[0]


# In[7]:


#== > Recuperando email
email1 = re.search(r'\s*[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.\s*[a-zA-Z]{2,}\s*', texto)
email1[0]


# In[8]:


#== > Recuperando link perfil
perfil1 = re.search(r'www\.linkedin\.com\/in\/[a-zA-Z0-9-]+', texto)
perfil1[0]


# ---

# ### Exercício 3:
# Aplique as funções geradas nas questões 1 e 2 para fazer o mesmo com o PDF em anexo (perfil do professor) e crie um CSV com as informações extraídas (colunas: nome, telefone, email e perfil) utilizando o módulo `csv` nativo do Python. Obs.: ao final os padrões utilizados no Regex devem abarcar os conteúdos dos dois PDFs.

# In[9]:


#==> lendo .pdf
pdf2 = PdfReader('../file/ViniciusBS_Perfil_2024_08_12.pdf')


# In[10]:


#==> Chamando funcao
texto2 = le_pdf(pdf2)
texto2 = ' '.join(texto2.split())


# In[11]:


#==> Recuperando informacoes
nome1 = re.search(r'maik', texto)[0]
telefone1 = re.search(r'9\d{4}-?\d{4}', texto)[0]
email1 = re.search(r'\s*[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.\s*[a-zA-Z]{2,}\s*', texto)[0]
perfil1 = re.search(r'www\.linkedin\.com\/in\/[a-zA-Z0-9-]+', texto)[0]

nome2 = re.search(r'vinicius', texto2)[0]
telefone2 = re.search(r'9\d{4}-?\d{4}', texto2)[0]
email2 = re.search(r'\s*[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.\s*[a-zA-Z]{2,}\s*', texto2)[0]
perfil2 = re.search(r'www\.linkedin\.com\/in\/[a-zA-Z0-9-]+', texto2)[0]


# In[12]:


#==> Dicionario
dados = {'Nome': [nome1,nome2],'Telefone': [telefone1,telefone2],'Email': [email1,email2],'Linkedin': [perfil1,perfil2]}

#==> Escrevendo .csv
with open('../file/perfis.csv', mode='w', newline='', encoding='utf-8') as arquivo_csv:
    escritor = csv.DictWriter(arquivo_csv, fieldnames=dados.keys()) 
    escritor.writeheader()
    for linha in zip(*dados.values()):
        escritor.writerow(dict(zip(dados.keys(), linha)))


# In[65]:


pd.read_csv('../file/perfis.csv')


# ---

# ## Parte 2: APIs

# ### Exercício 4:
# Explore o “playground” da API do SimilarWeb encontrada no RapidAPI ([link](https://rapidapi.com/Glavier/api/similarweb12/playground/)) e inscreva-se no plano gratuito. Então, crie um código para obter os dados dos 10 primeiros sites listados em “top-websites”, salvando-os em um dataframe do Pandas e, por fim, em um arquivo CSV usando o próprio Pandas.

# In[13]:


#==> Importando bibliotecas
import requests
import json
import pandas as pd


# In[14]:


#==> Requisicao
url = "https://similarweb12.p.rapidapi.com/v3/top-websites/"

headers = {
	"x-rapidapi-key": "471fd59fe1mshb443388ad14bfc4p1c1b01jsn763e6bb76f1d",
	"x-rapidapi-host": "similarweb12.p.rapidapi.com"
}

resposta = requests.get(url, headers=headers)

#==> Resultado dataframe
df = pd.DataFrame(resposta.json()['sites'])


# In[15]:


#==> Criando .csv
df[:10].to_csv('../file/top_sites.csv',index=False)


# In[16]:


#==> Lendo .csv
pd.read_csv('../file/top_sites.csv')


# ---

# ## Parte 3: XPath

# ### Exercício 5:
# Utilize o arquivo XML em anexo e a biblioteca `lxml` com caminhos relativos de XPath para:
# - Selecionar os nomes de todos *estudantes* que estejam no 2º ano ou acima dele;
# - Selecionar o nome do *professor* de Estruturas de Dados (course: "Data Structures");
# - Selecionar os títulos de todos os *cursos* ofertados pelo departamento de Ciência da Computação (department: Computer Science);
# - Selecionar os nomes de todos os *departamentos* que sejam pertencentes à Escola de Engenharia (college: Engineering).

# In[17]:


#==> Importando biblioteca
from lxml import etree


# In[18]:


#==> Lendo .xml
root = etree.parse('../file/AT.xml')


# In[19]:


#==> 1


# In[20]:


root.xpath("//student[@year > 2]/text()")


# In[21]:


#==> 2


# In[22]:


# root.xpath("//title/text()")

# root.xpath("//professor/text()")

root.xpath("//course[title='Data Structures']/professor/text()")


# In[23]:


#==> 3


# In[24]:


root.xpath("//department[@name='Computer Science']//title/text()")


# In[25]:


#==> 4
root.xpath("//college[@name='Engineering']/department/@name")


# ---

# ## Parte 4: CSS

# ### Exercício 6:
# Utilize o arquivo XML em anexo e a biblioteca `lxml` com seletores de CSS para:
# - Selecionar os títulos de todos os cursos cujos professores possuem estabilidade (tenure);
# - Selecionar os títulos de todos os cursos que possuem horário de início pela manhã (AM). **Dica:** cuidado com nomes antigos de pseudo-classes; caso algum não funcione, tente o nome antigo.

# In[26]:


#==> Importando biblioteca
from lxml import html
from lxml import etree
from lxml.cssselect import CSSSelector as sel


# In[27]:


#==> 1


# In[28]:


#==> Lendo .xml
tree = etree.parse('../file/AT.xml')

#==> Filtro
selecao = sel('professor[tenure="true"]')

#==> Recuperando nomes
[v.text for v in selecao(tree)]


# In[29]:


#==> 2


# In[30]:


#==> Lendo .xml
tree = etree.parse('../file/AT.xml')


# In[31]:


#==> Selecionando cursos
selector = sel('course')


# In[32]:


#==> Seletor
cursos = selector(tree)


# In[33]:


#==> Recuperando cursos
[curso.cssselect('title')[0].text for curso in cursos if curso.cssselect('schedule time') and "AM" in curso.cssselect('schedule time')[0].text]


# ---

# ## Parte 5: WebCrawling

# ### Exercício 7:
# Examine um site de sua escolha na lista de sites fornecida em anexo e descubra o padrão de URL para paginação que ele aceita. Então, utilize-o para obter uma lista de links de notícias requisitando as 2 primeiras páginas e raspando os links de cada uma através de um único seletor de CSS aplicado via `BeautifulSoup`.

# In[34]:


#==> Importando biblioteca
import requests
import random
import time
from bs4 import BeautifulSoup as bs


# In[35]:


header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}

#==> Recuperando dados unicos
def uniques(seq: list | tuple) -> list | tuple:
    out = []
    for x in seq:
        if x not in out:
            out.append(x)
    return out if isinstance(seq, list) else tuple(out)

#==> Fazendo requisicao
def requests_page_interval(url: str | bytes) -> str:
    time.sleep(random.randint(1,2))
    resposta = requests.get(url, headers=header, timeout=30)
    return resposta.text

dominio = 'https://diariodoestadomt.com.br/'

#==> Recuperando links
def web_crawler(url_pattern: str, selector: str, range_config: tuple) -> list:
    links = []
    for num in range(*range_config):
        pagina = requests_page_interval(url_pattern.format(num))
        soup = bs(pagina, 'lxml')
        urls = [tag.get('href') for tag in soup.select(selector)]
        urls_completas = [link if link.startswith('http') else dominio + link for link in urls]
        links.extend(urls_completas)
    return links


# In[36]:


links = web_crawler('https://diariodoestadomt.com.br/noticias/{}', 'a.news', (0, 2))


# In[37]:


#==> Links das paginas
links


# ---

# ## Parte 6: WebScraping

# ### Exercício 8:
# Faça um loop para os 3 primeiros links da lista obtida na questão anterior requisitando o HTML de cada página com a biblioteca que preferir (`urllib`, `requests`, etc.) e aplicando funções baseadas em `BeautifulSoup` para capturar e por fim salvar em um mesmo arquivo JSON, junto à URL de cada notícia e ao datetime do momento da requisição de cada página:
# - O objeto datetime (timezone-aware) da data e hora da publicação da notícia;
# - O título da notícia;
# - O corpo do texto da notícia;
# - O subtítulo da notícia (se houver);
# - O autor ou autores da notícia (se houver).

# In[38]:


#==> Importando bibliotecas
import requests
from bs4 import BeautifulSoup as bs
import random
import time
import json


# In[39]:


#==> Info cliente
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}


# In[40]:


#==> Lista
webscraping = []

#==> Iterando em links para recuperar dados
for i, v in enumerate(links[1:4]):
    resposta = requests.get(v, headers=headers, timeout=120)
    time_requisicao = resposta.headers.get('Date')

    #==> Gravando resposta
    with open(f'../file/{v[-9:]}.html', 'w', encoding='utf-8') as f:
        f.write(resposta.text)
    
    #==> Lendo .html
    with open(f'../file/{v[-9:]}.html', 'r', encoding='utf-8') as r: 
        noticia = r.read()

    #==> Rcuperando .html
    soup = bs(noticia, 'html.parser')

    noticias = {
        'url': v,
        'requisicao_datetime': time_requisicao,
        'timezone-aware': soup.find('h2').find_next_sibling('p').find_next_sibling('p').text.strip(),
        'noticia_titulo': soup.find('title').text.strip(),
        'noticia_corpo': ''.join([p.get_text().strip().replace('\n', '') for p in soup.find_all('p')][4:-10]),
        'noticia_subtitulo': 'NA',
        'noticia_autor': ''.join([p.get_text().strip().replace('\n', '') for p in soup.find_all('p')][-10]),
    }

    #==> Adicionando a lista
    webscraping.append(noticias)


# In[41]:


#==> Criando .json
with open('../file/noticias.json', 'w', encoding='utf-8') as arquivo:
    json.dump(webscraping, arquivo, ensure_ascii=False, indent=4)


# In[42]:


#==> Criando .json
with open('../file/noticias.json', 'r', encoding='utf-8') as r:
    noticias_json = json.load(r)


# In[43]:


noticias_json


# ---

# ## Parte 7: Scrapy

# ### Exercício 9:
# Escolha um dos sites da lista fornecida (que não tenha sido escolhido nas anteriores) para montar um projeto no Scrapy que abarque tanto o Crawling quanto o Scraping, a fim de rodá-lo tal como na questão anterior.

# In[44]:


#==> Importando biblioteca
import scrapy
import json
import pprint 


# In[45]:


#==> Criando projeto scrapping 
# !scrapy startproject at_scrapy


# In[46]:


#==> Executando comando no bash


# In[47]:


# %%bash
# cd /home/maik/_repos/ATDR2/src/at_scrapy/at_scrapy/spiders
# scrapy genspider rondonia_noticias rondoniadinamica.com/ultimas-noticias


# In[48]:


#==> Executando comando no bash


# In[49]:


# %%bash
# cd /home/maik/_repos/ATDR2/src/at_scrapy/at_scrapy/spiders
# scrapy crawl rondonia_noticias -o rondonia_noticias.json


# In[50]:


#==> Executando comando no bash


# In[51]:


# %%bash
# cd /home/maik/_repos/ATDR2/src/at_scrapy/at_scrapy/spiders
# scrapy crawl rondonia_noticias -o rondonia_noticias.json


# In[52]:


#==> Lendo .json
with open('/home/maik/_repos/ATDR2/src/at_scrapy/at_scrapy/spiders/rondonia_noticias.json', 'r', encoding='utf-8') as f:
    dados = json.load(f) 
    
dados


# ---

# ## Parte 8: Selenium

# ### Exercício 10:
# Extraia uma lista de empregos do site [**Indeed**](https://br.indeed.com). Extraia os títulos dos empregos da primeira página de resultados ao pesquisar por "Data Scientist" na área da capital de seu estado. O site usa JavaScript para carregar as listas dinamicamente, o que significa que você não pode recuperar esses dados simplesmente usando solicitações ou `BeautifulSoup`. Escreva um script em Python usando Selenium para extrair os títulos dos empregos desta página junto a outras informações que você considere relevante.

# In[53]:


#==> Importando biblioteca
from selenium import webdriver
from selenium.webdriver.common.by import By


# In[54]:


#==> Instanciando
driver = webdriver.Firefox() 


# In[55]:


#==> Acessando site
driver.get('https://br.indeed.com/')


# In[56]:


#==> Identificando elementos
keyword_input = driver.find_element(By.CSS_SELECTOR, '#text-input-what')
region_input = driver.find_element(By.CSS_SELECTOR, '#text-input-where')


# In[57]:


#==> Limpando campos
keyword_input.clear()
region_input.clear()

#==> Enviando dados
keyword_input.send_keys('Data Scientist')
region_input.send_keys('Parana')


# In[58]:


#==> Idendificando/clicando no botao
submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type=submit]')
submit_button.click()


# In[59]:


#==> Recuperando vagas
cards = driver.find_elements(By.CSS_SELECTOR, 'div.job_seen_beacon')


# In[60]:


#==> Iterando nas vagas
for card in cards:
    title = card.find_element(By.CSS_SELECTOR, 'h2 > a > span').text
    company = card.find_element(By.CSS_SELECTOR, '[data-testid="company-name"]').text
    presentation_div = driver.find_element(By.CSS_SELECTOR, 'div[role="presentation"].css-1u8dvic').text
    print(title, company, presentation_div,  sep=' | ', end='\n\n')


# In[61]:


driver.quit()


# ---

# [**Repositorio - Clique Aqui!**](https://github.com/maik-junior/ATDR2)




