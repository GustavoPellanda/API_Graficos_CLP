<h1 align="center"> API de Gráficos do CLP </h1>

<p>API_CLP é um programa que busca as variáveis disponíveis de um CLP e cria uma rota de transmissão de seus valores para um template web.</p>
<p>Em conjunto com display_grafico, a finalidade deste programa é que uma variável escolhida pelo usuário tenha um histórico de seus valores exibidos em uma página web de forma gráfica.</p>

<h2>Conteúdos</h2>
  <ul>
    <li><a href="#Funcionamento">Funcionamento</a></li>
    <li><a href="#Utilização">Utilização</a></li>
    <li><a href="#Tecnologias Utilizadas">Tecnologias Utilizadas</a></li>
    <li><a href="#Gráficos Resultantes">Gráficos Resultantes</a></li>
  </ul>

<h2>Funcionamento</h2>
<p>O programa API_CLP faz requisições getvar.csv para um web server definido por seu IP. O web server para o qual essa aplicação foi criada é um CLP, que responde essa requisição com um arquivo CSV contendo todas as variáveis que ele têm disponíveis no momento e os respectivos valores armazenados nelas. 

Inicialmente, as variáveis que possuem valor numérico são filtradas e enviadas ao primeiro template web, index.html, que as organiza em uma tabela. Dessa forma, o usuário pode escolher a variável que deseja exibir de forma gráfica. A escolha retorna um POST para API_CLP.

O código então busca pela variável escolhida, que pode ser encontrada a partir de seu ID, e salva suas informações como instâncias da classe Variavel_CLP. Por fim, é criada uma rota de dados Flask que transmite Variavel_CLP para o segundo template web, display_grafico.

O template display_grafico.html faz requisições fetch para a rotas de dados Flask para obter Variavel_CLP. O histórico de valores é plotado em um gráfico, assim como uma média dos últimos valores obtidos. O gráfico é criado a partir da biblioteca Chart JS.</p>

<h2>Utilização</h2>
   <p>Basta definir o IP do web server e rodar o programa. Os templates HTML devem estar salvos em uma pasta "templates".</p>

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

