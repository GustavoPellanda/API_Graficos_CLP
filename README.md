<h1 align="center"> API de Gráficos do CLP </h1>

<p> API_CLP é um programa que recebe um CSV com as variáveis disponíveis de um CLP, busca por uma em específico a partir de seu índice, salva os valores obtidos os transmite para um template web.</p>
<p>O programa API_CLP incialmente faz requisição getvar.csv para um web server definido por seu IP. O web server para o qual essa aplicação foi criada é um CLP, que responde essa requisição com um arquivo CSV contendo todas as variáveis que ele têm disponíveis no momento e os respectivos valores armazenados nelas. O código então busca pela variável de temperatura, que pode ser encontrada a partir de seu ID, e salva suas informações na classe Variavel_CLP. Por fim, é criada uma rota de dados Flask que transmite Variavel_CLP para um template web.</p>
<p>O template web index.html faz requisições fetch para a rotas de dados Flask para obter Variavel_CLP. O histórico de valores é plotado em um gráfico, assim como uma média dos últimos valores obtidos. O gráfico é criado a partir da biblioteca Chart JS.</p>


<h2>Conteúdos</h2>
  <ul>
    <li><a href="#Utilização">Utilização</a></li>
     <li><a href="#Tecnologias Utilizadas">Tecnologias Utilizadas</a></li>
    <li><a href="#Gráficos Resultantes">Gráficos Resultantes</a></li>
  </ul>

<h2>Utilização</h2>
   <p>Basta definir o IP do web server e o índice da variável que será buscada e rodar o programa. index.html deve estar salvo em uma pasta "templates".</p>

<h2>Tecnologias Utilizadas</h2>
<ul>
  <li>Python</li>
  <li>Flask</li>
  <li>HTML</li>
  <li>Javascript</li>
  <li>Chart.js</li>
</ul>

<h2>Gráficos Resultantes</h2>
  <p>Exemplo de um dos gráficos resultantes.</p>
  <img src="https://user-images.githubusercontent.com/129123498/232354503-43513c55-be3b-4e57-9794-b18a929f22ee.png" alt="Gráfico sendo exibido na web">
  <p>Curva de aquecimento:</p>
  <img src="https://user-images.githubusercontent.com/129123498/232528317-81cd9710-df14-4214-8c89-683e408d6119.png" alt="Gráfico sendo exibido na web">
  <img src="https://user-images.githubusercontent.com/129123498/232528310-944c3923-e2d6-4bce-a806-e9dddced4945.png" alt="Gráfico sendo exibido na web">

