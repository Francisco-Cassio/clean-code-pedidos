# Cálculo de Pedidos e Desconto VIP — Refatoração Verificável

Módulo em Python para cálculo do valor total de pedidos em centavos com aplicação de política de desconto para clientes VIP, refatorado com auxílio de IA sob verificação de testes automatizados (`unittest`).

> **Autores:** Francisco de Cássio da Silva Mourão Júnior e Álvaro Miguel Rodrigues Aquino Costa  
> **Disciplina:** Tópicos Especiais em Programação — IFPI

---

## 📋 Sobre o Projeto e Regras de Negócio (Contrato)

A função `total_centavos(precos, vip=False)` em [`pedido.py`](./pedido.py) calcula o total a pagar a partir de uma lista de preços inteiros não negativos (em centavos):

- **Soma dos itens:** Calcula o subtotal somando todos os preços da lista recebida.
- **Regra de Desconto VIP:** Se `vip=True` e o subtotal for **maior ou igual a `10000` centavos** (limiar inclusivo), aplica-se um desconto inteiro de `10%` (`subtotal // 10`).
- **Demais casos:** Retorna o próprio subtotal sem desconto.
- **Imutabilidade:** A lista original `precos` passada como argumento não é alterada.

---

## 🔄 Comparativo da Refatoração

### Antes (`pedido-antes.txt`)
```python
def total_centavos(precos, vip=False):
    s = 0
    for p in precos:
        s = s + p
    if vip:
        if s >= 10000:
            return s - s // 10
        else:
            return s
    else:
        return s
```

### Depois (`pedido.py`)
```python
def total_centavos(precos, vip=False):
    subtotal = sum(precos)
    if vip and subtotal >= 10000:
        desconto = subtotal // 10
        return subtotal - desconto
    return subtotal
```

### Diff (`git diff`)
```diff
 def total_centavos(precos, vip=False):
-    s = 0
-    for p in precos:
-        s = s + p
-    if vip:
-        if s >= 10000:
-            return s - s // 10
-        else:
-            return s
-    else:
-        return s
+    subtotal = sum(precos)
+    if vip and subtotal >= 10000:
+        desconto = subtotal // 10
+        return subtotal - desconto
+    return subtotal
```

---

## 🧠 Análise Técnica da Refatoração

### 1. Qual problema de organização havia?
- **Nomes pouco expressivos:** As variáveis `s` (acumulador) e `p` (item da lista) eram abreviações de uma única letra que não comunicavam os conceitos do domínio (`subtotal` e `preco`).
- **Laço de soma manual redundante:** Um loop `for` acumulava manualmente os valores (`s = s + p`) em vez de utilizar a função embutida `sum(precos)`.
- **Ramificações aninhadas e `else` desnecessários:** Havia dois blocos `if` aninhados (`if vip:` e `if s >= 10000:`) acompanhados de dois blocos `else` que apenas repetiam `return s`.

### 2. O que mudou?
- A variável `s` foi renomeada para `subtotal` e o laço manual foi substituído por `sum(precos)`.
- Os dois `if` aninhados foram combinados em uma única condição composta (`if vip and subtotal >= 10000:`), eliminando os dois blocos `else` redundantes.
- O cálculo do desconto passou a ser explicitado na variável `desconto = subtotal // 10`, retornando `subtotal - desconto` quando a regra VIP é atendida, ou `subtotal` diretamente no fluxo padrão.

### 3. Por que a regra continua preservada?
- **Assinatura e tipo do retorno:** `total_centavos(precos, vip=False)` permanece idêntica e retorna `int`.
- **Preservação da entrada:** `sum(precos)` apenas itera sobre a sequência sem mutar a lista original.
- **Limiar inclusivo:** O operador `>= 10000` foi mantido, garantindo que clientes VIP com subtotal exatamente igual a `10000` centavos recebam o desconto e paguem `9000`.
- **Desconto e arredondamento inteiro:** A divisão inteira `subtotal // 10` foi mantida (ex.: subtotal `10009` resulta em desconto `1000` e total `9009`).
- **Demais cenários:** Caso `vip` seja `False` ou `subtotal < 10000`, a condição do `if` não é satisfeita e a função retorna `subtotal`.

### 4. Caso de teste adicional sugerido
- **Cenário:** Cliente **não VIP** com subtotal exatamente no limite de 10000 centavos (`total_centavos([6000, 4000], False)`).
- **Resultado esperado:** `10000`
- **Justificativa:** A suíte atual valida o limite exato de `10000` apenas para cliente VIP (`test_vip_no_limite`) e valida cliente comum apenas acima do limite omitindo o parâmetro booleano (`test_sem_vip`). Testar `total_centavos([6000, 4000], False)` garante que o limiar de `10000` não conceda desconto indevido quando `vip=False` é informado explicitamente.

---

## 💬 Prompt Utilizado na IA

```text
Refatore apenas pedido.py para melhorar nomes e reduzir ramificações desnecessárias. Preserve a assinatura total_centavos(precos, vip=False), o tipo do retorno e todas as regras do contrato. Não mude test_pedido.py, não crie dependências nem funcionalidades novas. Primeiro explique sua proposta; depois apresente uma mudança pequena. Não afirme que executou testes se você não tiver como executá-los. Ao final, explique o que mudou e que comportamento deve permanecer igual.
```

---

## ✅ Como Executar os Testes e Evidências

Para rodar a suíte de testes automatizados (Python 3 padrão, sem dependências externas):

```bash
python test_pedido.py
```

### Evidência — Execução Inicial (Antes da Refatoração)
```text
test_arredondamento (__main__.TestPedido.test_arredondamento) ... ok
test_preserva_entrada (__main__.TestPedido.test_preserva_entrada) ... ok
test_sem_vip (__main__.TestPedido.test_sem_vip) ... ok
test_soma (__main__.TestPedido.test_soma) ... ok
test_vazio (__main__.TestPedido.test_vazio) ... ok
test_vip_abaixo (__main__.TestPedido.test_vip_abaixo) ... ok
test_vip_acima (__main__.TestPedido.test_vip_acima) ... ok
test_vip_no_limite (__main__.TestPedido.test_vip_no_limite) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.000s

OK
```

### Evidência — Execução Final (Após a Refatoração)
```text
test_arredondamento (__main__.TestPedido.test_arredondamento) ... ok
test_preserva_entrada (__main__.TestPedido.test_preserva_entrada) ... ok
test_sem_vip (__main__.TestPedido.test_sem_vip) ... ok
test_soma (__main__.TestPedido.test_soma) ... ok
test_vazio (__main__.TestPedido.test_vazio) ... ok
test_vip_abaixo (__main__.TestPedido.test_vip_abaixo) ... ok
test_vip_acima (__main__.TestPedido.test_vip_acima) ... ok
test_vip_no_limite (__main__.TestPedido.test_vip_no_limite) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.000s

OK
```

---

## 📁 Estrutura do Repositório

| Arquivo | Descrição |
| :--- | :--- |
| [`pedido.py`](./pedido.py) | Implementação refatorada da função `total_centavos(precos, vip=False)` |
| [`pedido-antes.txt`](./pedido-antes.txt) | Cópia do código original antes da refatoração |
| [`test_pedido.py`](./test_pedido.py) | Suíte com 8 testes unitários (`unittest`) que verificam o contrato |
| [`AGENTS.md`](./AGENTS.md) | Especificação de regras e restrições do contrato para o agente de IA |
| [`README.md`](./README.md) | Documentação do projeto, comparativo, análise e evidências de teste |

---

## 👥 Autores

- **Francisco de Cássio da Silva Mourão Júnior**
- **Álvaro Miguel Rodrigues Aquino Costa**
