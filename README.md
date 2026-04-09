# QueryPilot AI

**Transforme perguntas em linguagem natural em consultas SQL seguras, auditáveis e executáveis.**

QueryPilot AI é uma API inteligente voltada para ambientes corporativos que precisam consultar dados com rapidez, segurança e rastreabilidade. O projeto combina **FastAPI**, **Agno**, **PostgreSQL**, **SQLAlchemy** e **Alembic** para criar um agente capaz de entender a intenção do usuário, planejar a consulta, gerar SQL, validar o impacto e executar a operação com controle.

A proposta deste projeto é ir muito além de um simples gerador de SQL. Ele foi pensado como um produto real para times de dados, operações, suporte, financeiro, vendas e gestão, reduzindo tempo gasto com consultas manuais e ajudando pessoas não técnicas a extrair informações úteis do banco com menos atrito.

---

## Visão geral

Em muitas empresas, o acesso aos dados ainda depende de analistas ou desenvolvedores para criar consultas sob demanda. Isso gera gargalos, atrasos e consultas mal formuladas. O QueryPilot AI resolve esse problema com um fluxo orientado por IA:

1. O usuário faz uma pergunta em linguagem natural.
2. O agente interpreta o objetivo de negócio.
3. O agente consulta o contexto do banco e identifica tabelas, relações e colunas relevantes.
4. O agente monta um plano de execução.
5. O agente gera o SQL.
6. O usuário valida o SQL.
7. O sistema valida a consulta.
8. O sistema executa com segurança.
9. O resultado é retornado em formato tabular.

O projeto foi desenhado para ser demonstrável em entrevistas, mas com profundidade suficiente para parecer uma solução que poderia ser adotada por uma empresa de verdade.

---

## Problema que o projeto resolve

Empresas normalmente enfrentam estes problemas:

- consultas repetitivas consumindo tempo do time técnico;
- usuários de negócio sem autonomia para explorar dados;
- risco de consultas erradas afetando performance ou integridade;
- dificuldade de auditar quem consultou o quê;
- respostas lentas para dúvidas operacionais e estratégicas;
- dependência excessiva de SQL manual para decisões simples.

O QueryPilot AI ataca exatamente esse cenário, oferecendo uma camada inteligente para consulta de dados com controle e governança.

---

## Proposta de valor

O projeto entrega valor em três frentes:

### 1. Produtividade

Reduz o tempo necessário para obter respostas do banco de dados.

### 2. Segurança

Evita consultas perigosas, sem controle ou fora do padrão esperado.

### 3. Inteligência

Não apenas gera SQL: interpreta intenção, sugere melhoria e explica o resultado.

---

## Features principais

### 1. Consulta em linguagem natural

O usuário pode escrever perguntas como:

- “Quais foram os clientes mais lucrativos no último trimestre?”
- “Mostre os tickets com maior tempo médio de resolução.”
- “Liste os pedidos atrasados por região.”
- “Quais produtos tiveram queda de faturamento no mês atual?”

O agente interpreta a frase, identifica a intenção e transforma isso em uma consulta SQL contextualizada.

### 2. Entendimento do schema do banco

O agente conhece a estrutura do PostgreSQL e usa isso para gerar consultas mais corretas.

Inclui:

- leitura de tabelas, colunas e tipos;
- identificação de chaves primárias e estrangeiras;
- mapeamento de relacionamentos;
- reconhecimento de nomes semânticos do domínio;
- apoio para joins corretos e filtros consistentes.

Essa feature é essencial para evitar SQL genérico ou desconectado da realidade do banco.

### 3. Geração de SQL em múltiplas etapas

Em vez de gerar a query diretamente, o agente trabalha em fluxo estruturado:

- interpretação da pergunta;
- definição da intenção de negócio;
- seleção de tabelas candidatas;
- construção do plano de consulta;
- geração do SQL final;
- validação antes da execução.

Isso melhora a qualidade da resposta e mostra maturidade arquitetural.

### 4. Modo seguro de execução

O sistema pode operar com regras de segurança para evitar dano acidental.

Exemplos de proteção:

- permitir apenas `SELECT` por padrão;
- exigir confirmação para `INSERT`, `UPDATE` e `DELETE`;
- bloquear consultas sem `WHERE` em tabelas críticas;
- forçar `LIMIT` em consultas amplas;
- impedir queries potencialmente destrutivas;
- registrar todas as execuções.

Essa feature é excelente para mostrar preocupação real com produção.

### 5. Validação automática da consulta

Antes de executar, o sistema valida a query e identifica riscos.

Pode analisar:

- sintaxe SQL;
- tabelas inexistentes;
- colunas inválidas;
- joins suspeitos;
- ausência de filtros;
- potencial alto volume de retorno;
- possíveis ambiguidades.

Isso reduz falhas e melhora a confiabilidade da aplicação.

### 6. Explicação humana da resposta

Além do SQL e do resultado bruto, o agente pode gerar uma explicação simples do que foi encontrado.

Exemplo de saída:

- o que a consulta fez;
- quais dados foram usados;
- qual foi o resultado principal;
- qual insight de negócio pode ser extraído;
- quais próximos passos fazem sentido.

Essa camada é muito valiosa para perfis não técnicos.

### 7. Histórico completo de consultas

O sistema salva cada interação para auditoria e rastreabilidade.

Armazena, por exemplo:

- pergunta original;
- SQL gerado;
- SQL executado;
- data e hora;
- tempo de execução;
- usuário solicitante;
- status da execução;
- resposta retornada;
- eventuais erros.

Isso faz o projeto parecer uma solução enterprise.

### 8. Perfis de uso por papel

O comportamento do agente pode mudar conforme o perfil do usuário.

Exemplos:

- **Gestor**: recebe resumos e agregações;
- **Analista**: recebe mais detalhe e granularidade;
- **Operação**: vê dados acionáveis e alertas;
- **Financeiro**: foca em valores, atrasos e reconciliação.

Essa feature ajuda a mostrar visão de produto e contexto corporativo.

---

## Features avançadas

### 9. Modo de preview antes de executar

O usuário visualiza o SQL gerado antes da execução final.

Esse fluxo pode mostrar:

- consulta em linguagem natural;
- SQL proposto;
- tabelas afetadas;
- tipo de operação;
- nível de risco;
- confirmação manual.

Isso demonstra controle e transparência.

### 13. Logs estruturados e rastreabilidade

Cada passo do agente pode gerar logs estruturados.

Isso ajuda a observar:

- intenções recebidas;
- decisões do agente;
- query final;
- erros de validação;
- tempo de execução;
- resposta do banco.

Excelente para debugar e para mostrar maturidade técnica.

### 14. Métricas de uso

O projeto pode exibir indicadores como:

- número de consultas por usuário;
- perguntas mais frequentes;
- taxa de sucesso da geração de SQL;
- tempo médio de resposta;
- consultas bloqueadas por segurança;
- tipos de pergunta mais comuns.

Essas métricas transformam o projeto em algo observável.

### 15. Feedback do usuário

Após cada resposta, o usuário pode avaliar o resultado.

Exemplos de feedback:

- “correto”;
- “incompleto”;
- “SQL ruim”;
- “resposta útil”;
- “resultado confuso”.

Isso permite ciclos de melhoria do agente.

---

## Stack principal

- **FastAPI** — API principal, rápida, moderna e bem estruturada.
- **Agno** — orquestração inteligente do agente e do raciocínio.
- **PostgreSQL** — banco relacional principal.
- **SQLAlchemy** — camada de ORM e persistência.
- **Alembic** — migrações e evolução do schema.

---

## Fluxo principal

1. Usuário envia uma pergunta.
2. FastAPI recebe a requisição.
3. Agno interpreta o contexto.
4. O sistema consulta o schema e as regras.
5. O SQL é gerado.
6. O SQL passa pela validação.
7. O banco executa a query.
8. O resultado é persistido no histórico.
9. O usuário recebe a resposta com explicação.

---

## Casos de uso reais

### Suporte

- identificar tickets atrasados;
- detectar temas recorrentes;
- medir SLA;
- priorizar chamados críticos.

### Financeiro

- reconciliar pagamentos;
- detectar divergências;
- listar inadimplência;
- acompanhar receita por período.

### Vendas

- analisar conversão por etapa;
- identificar leads com maior chance de fechar;
- ver performance de representantes;
- mapear oportunidades perdidas.

### Operações

- acompanhar gargalos;
- ver atrasos por processo;
- identificar falhas recorrentes;
- gerar relatórios operacionais.

---

## Endpoints

### `POST /query/preview`

Gera o SQL proposto sem executar.

### `POST /query/execute`

Executa a consulta após validação.

### `POST /query/confirm`

Confirma uma execução pendente, quando necessário.

### `GET /history`

Lista o histórico de consultas realizadas.

### `GET /history/{id}`

Retorna os detalhes de uma consulta específica.

### `POST /feedback`

Salva avaliação do resultado retornado.

### `GET /schema`

Exibe metadados do banco e mapeamentos disponíveis.

### `GET /metrics`

Retorna métricas de uso e performance.

---

## Modelo de dados sugerido

### Tabelas principais

- `users`
- `roles`
- `query_requests`
- `query_executions`
- `query_feedbacks`
- `audit_logs`
- `database_schemas`
- `database_tables`
- `database_columns`
- `execution_errors`

### O que pode ser salvo

- texto original da pergunta;
- SQL gerado;
- SQL final executado;
- resultado resumido;
- tempo de execução;
- usuário responsável;
- risco calculado;
- feedback recebido;
- data e hora;
- detalhes de erro, se houver.

---

## Regras de negócio sugeridas

- consultas destrutivas exigem confirmação explícita;
- queries sem escopo podem ser bloqueadas;
- tabelas sensíveis podem exigir permissões extras;
- a consulta precisa respeitar o domínio do usuário;
- consultas muito pesadas podem ser recusadas;
- toda ação deve ser auditável.

---

## Segurança

A segurança é uma parte central do projeto.

Boas práticas que podem ser incluídas:

- autenticação via JWT;
- autorização por perfil;
- validação forte de entrada;
- bloqueio de SQL perigoso;
- auditoria completa;
- rate limit;
- logs de tentativa de uso indevido;
- controle de acesso por domínio e funcionalidade.
