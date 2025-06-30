def calculate_total_cost(car: dict) -> dict:
    """
    Расчёт полной стоимости автомобиля: доставка, таможня, утилизация и итог.
    """
    price = car.get("price", 0)
    year = car.get("year", 2020)

    if price <= 0:
        raise ValueError("Цена автомобиля должна быть больше нуля.")

    # Примерные значения
    delivery_cost = 100000  # доставка
    utilization_fee = 20000  # утильсбор

    # Условная логика для расчёта таможни:
    if year >= 2020:
        customs_duty = int(price * 0.15)
    elif 2010 <= year < 2020:
        customs_duty = int(price * 0.2)
    else:
        customs_duty = int(price * 0.3)

    total = price + delivery_cost + customs_duty + utilization_fee

    return {
        "delivery": delivery_cost,
        "customs": customs_duty,
        "utilization": utilization_fee,
        "total": total
    }
