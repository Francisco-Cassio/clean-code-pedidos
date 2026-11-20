# Entrega — Aula 13: Refatoração Verificável com IA

## 1. Versão Anterior (`pedido-antes.txt`)

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

## 2. Versão Refatorada (`pedido.py`)

```python
def total_centavos(precos, vip=False):
    subtotal = sum(precos)
    if vip and subtotal >= 10000:
        desconto = subtotal // 10
        return subtotal - desconto
    return subtotal
```

### Diff da Refatoração (`git diff`)
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

## 3. Evidências das Duas Execuções

### 3.1. Execução Inicial (Antes da Refatoração)
Comando executado:
```bash
python test_pedido.py
```
Saída:
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

### 3.2. Execução Final (Depois da Refatoração)
Comando executado:
```bash
python test_pedido.py
```
Saída:
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

## 4. Prompt Utilizado

```text
Refatore apenas pedido.py para melhorar nomes e reduzir ramificações desnecessárias. Preserve a assinatura total_centavos(precos, vip=False), o tipo do retorno e todas as regras do contrato. Não mude test_pedido.py, não crie dependências nem funcionalidades novas. Primeiro explique sua proposta; depois apresente uma mudança pequena. Não afirme que executou testes se você não tiver como executá-los. Ao final, explique o que mudou e que comportamento deve permanecer igual.
```

---

## 5. Explicação Escrita da Entrega

### Qual problema de organização havia?
1. **Nomes pouco expressivos:** As variáveis `s` (acumulador) e `p` (elemento da lista) eram abreviações de uma letra que não comunicavam os conceitos do domínio (`subtotal` e `preco`).
2. **Soma manual desnecessária:** Um laço `for` acumulava manualmente os valores (`s = s + p`) em vez de utilizar a função nativa `sum(precos)`.
3. **Ramificações aninhadas e redundantes:** Havia dois blocos `if` aninhados (`if vip:` seguido de `if s >= 10000:`) e dois blocos `else` que apenas repetiam `return s`.

### O que mudou?
- A variável `s` foi renomeada para `subtotal` e o laço `for` manual foi substituído por `sum(precos)`.
- Os dois `if` aninhados foram combinados em uma única condição (`if vip and subtotal >= 10000:`), eliminando os dois blocos `else` redundantes.
- O cálculo do desconto foi explicitado na variável `desconto = subtotal // 10`, retornando `subtotal - desconto` quando aplicável, ou `subtotal` nos demais casos.

### Por que a regra continua preservada?
- **Assinatura e tipo de retorno:** `total_centavos(precos, vip=False)` permanece idêntica e continua retornando um inteiro (`int`).
- **Imutabilidade da lista recebida:** `sum(precos)` apenas lê os elementos da lista sem alterá-la.
- **Limiar inclusivo:** O operador `>= 10000` foi mantido intacto, garantindo que um cliente VIP com subtotal exatamente igual a `10000` centavos receba o desconto e pague `9000`.
- **Desconto e arredondamento inteiro:** A divisão inteira `subtotal // 10` foi preservada (por exemplo, subtotal `10009` gera desconto `1000` e total `9009`).
- **Demais casos:** Quando `vip` é `False` ou `subtotal < 10000`, a condição composta `vip and subtotal >= 10000` resulta em `False` e a função retorna `subtotal`.

### Caso adicional sugerido (Passo 5 — Limites da verificação)
- **Caso sugerido:** Cliente **não VIP** com subtotal exatamente no limite de 10000 centavos (`precos = [6000, 4000]`, `vip = False`).
- **Chamada:** `total_centavos([6000, 4000], False)`
- **Resultado esperado:** `10000`
- **Motivo:** A suíte atual testa o limite exato de `10000` apenas para cliente VIP (`test_vip_no_limite`) e testa cliente não VIP apenas com `[15000]` omitindo o segundo argumento (`test_sem_vip`). Esse caso adicional verifica explicitamente que atingir o limiar `10000` com `vip=False` não concede desconto indevido.
