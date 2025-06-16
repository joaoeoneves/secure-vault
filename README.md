# 🔐 SecureVault — Microserviços com Design Patterns

**Projeto académico** desenvolvido no âmbito da cadeira de **Arquiteturas de Software**, do **Mestrado em Informática Aplicada 2024/25** da **Escola Superior de Gestão e Tecnologia de Santarém** (ESGTS - IPSantarém).

## 📚 Contexto

O objetivo do projeto é aplicar os conceitos de **microserviços** e **Design Patterns** numa solução prática, demonstrando:
- separação de responsabilidades
- independência entre serviços
- aplicação de padrões de design clássicos e criativos
- comunicação entre serviços de forma desacoplada

O tema escolhido para este trabalho foi a construção de um **SecureVault** — um cofre digital moderno e seguro, capaz de gerir diferentes tipos de informação sensível dos utilizadores (não apenas passwords).

---

## 🏛️ Arquitetura

O sistema é composto por **3 microserviços de negócio**, cada um com um Design Pattern bem definido, e um **Frontend** para demonstração:

### 1️⃣ User Management Service
- **Responsabilidade:** gestão de utilizadores e autenticação.
- **Design Pattern:** *Facade Pattern* para disponibilização simples dos métodos (dos slides) + Singleton para DB propria (SQLAlchemy).

### 2️⃣ Vault Service (Cofre)
- **Responsabilidade:** guardar e gerir entradas encriptadas (Passwords, Notas, Cartões Bancários e Chaves SSH).
- **Design Pattern:** *Factory Method* para a criação dos diferentes tipos (dos slides) + Singleton para DB propria (SQLAlchemy).
  
### 3️⃣ Credential Health Service
- **Responsabilidade:** avaliar a "saúde" das credenciais (passwords fracas, reutilizadas, não atualizadas, cartões expirados, etc.).
- **Design Pattern:** *Chain of Responsibility* (padrão extra-aulas), vai passando pelos estágios mencionados até chegar a uma conclusão.

### ➕ Frontend
- **Responsabilidade:** interface simples para demonstrar a arquitetura (login/registo, cofre de entradas, resultados de health check das passwords).

---

## 🎨 Diagrama da Arquitetura

Por Acrescentar

---

## 🛠️ Tecnologias e Stack

- **Linguagem:** Python 3
- Outras a detalhar...

---

## 👩‍💻 Equipa

Projeto desenvolvido por:

- João Areosa  
- João Neves  
- Tomás Marques  
- Tomás Matos  

---

## ✅ Objetivos Pedagógicos

- Aplicação prática dos conceitos de **microserviços**.
- Aplicação de **3 Design Patterns**:
  - 2 padrões **vistos em aula** (Facade, Factory Method)
  - 1 padrão **extra e criativo** (Chain of Responsibility).
- Demonstração de um sistema **desacoplado**, **modular** e **escalável**.
- Exploração de tecnologias modernas.

---

## 🚀 Como Correr?

1. Abrir a pasta clonada do repositório
2. ``` docker compose build ```
3. ``` docker compose run ```
4. Abrir localhost:5000 no browser

---

## 📝 Licença

Este projeto é **exclusivamente académico** e não se destina a uso em produção.  
Qualquer utilização deverá respeitar as licenças das tecnologias envolvidas.

---
