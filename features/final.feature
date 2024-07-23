
Feature: Login
  Como um usuário
  Eu quero fazer login na página

  Scenario: Login
    Given que esteja na página
    When digitar usuário e senha
    Then deve aparecer "Logado com sucesso"
