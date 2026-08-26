# Projeto de Extensão em Desenvolvimento de Sistemas — Conecta Gerações

## Resumo
Este projeto propõe uma solução de apoio à inclusão digital de pessoas idosas, alinhada ao projeto de referência fornecido pela disciplina. A solução web organiza participantes, encontros, materiais didáticos e acompanhamentos de presença e aprendizado. O objetivo é apoiar os alunos monitores na execução das atividades práticas e permitir o registro estruturado do progresso. A implementação utiliza Flask, HTML/CSS e SQLite. Os resultados da ação de extensão devem ser preenchidos após a realização efetiva das atividades.

## Introdução
### Contextualização
A evolução das tecnologias digitais pode criar dificuldades de acesso e autonomia para pessoas que não tiveram contato contínuo com smartphones e mídias sociais. O documento-base aponta a inclusão digital como forma de ampliar comunicação, acesso à informação e autonomia.

### Justificativa
A proposta utiliza tecnologia para apoiar uma ação social e, simultaneamente, desenvolver competências técnicas, didáticas e de comunicação dos alunos.

### Objetivo geral
Desenvolver uma aplicação de apoio à organização e acompanhamento de uma ação de inclusão digital para pessoas com 60 anos ou mais.

### Objetivos específicos
- Organizar participantes.
- Disponibilizar o plano dos quatro encontros.
- Registrar presença e aprendizado.
- Apoiar monitores com materiais didáticos.
- Gerar indicadores simples para acompanhamento.

## Revisão de Literatura
Esta seção deve ser ampliada pelo grupo com fontes acadêmicas e documentação oficial. A base fornecida pela professora descreve inclusão digital, uso de smartphones e mídias sociais, segurança e avaliação qualitativa/quantitativa.

## Metodologia
Ferramentas: Python, Flask, SQLite, HTML e CSS. O ciclo adotado é levantamento → requisitos → modelagem → protótipo → implementação → testes → validação → documentação. Os papéis dos integrantes e o cronograma devem ser ajustados com os dados reais do grupo.

## Desenvolvimento da Solução
A solução possui dashboard, cadastro de participantes, plano de encontros, materiais didáticos e acompanhamento. Os requisitos detalhados estão em `01_requisitos.md`.

## Testes e Resultados
Os testes automatizados estão em `tests/`. Os resultados da execução local podem ser obtidos com `pytest -q`. Os resultados da ação de extensão não são simulados neste trabalho e devem ser registrados pelo grupo após os encontros.

## Conclusão
A solução cria uma base funcional para apoiar a organização da ação de inclusão digital. Como limitações, a versão inicial não possui autenticação, controle de permissões, hospedagem pública ou integração com serviços externos. Futuras versões podem incluir contas de monitores, relatórios PDF, exportação CSV, acessibilidade ampliada e sincronização em nuvem.

## Referências
UNIVERSIDADE NOVE DE JULHO. Projeto de Extensão: Inclusão Digital na Melhor Idade — Conectando Gerações. Documento fornecido na disciplina.
UNIVERSIDADE NOVE DE JULHO. Projeto de Extensão em Desenvolvimento de Sistemas — estrutura do trabalho. Documento fornecido na disciplina.

> Antes da entrega, revisar referências e formatar integralmente conforme ABNT, conforme orientação da professora.
