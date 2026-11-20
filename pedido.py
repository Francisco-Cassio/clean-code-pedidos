def total_centavos(precos, vip=False):
    subtotal = sum(precos)
    if vip and subtotal >= 10000:
        desconto = subtotal // 10
        return subtotal - desconto
    return subtotal
