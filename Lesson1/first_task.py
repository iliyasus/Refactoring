def get_package(package_weight, package_distance, vip_package):
    if package_weight <= 0 or package_distance <= 0:
        print("Bad data")
        return 0
    PRICE_BEFORE = 200
    PRICE_AFTER = 500
    # Общая стоимость 
    if package_weight <= 5:
        result = PRICE_BEFORE + (package_distance * 15)      
    else:
        result = PRICE_AFTER + (package_distance * 15)

    # Стиомость срочной посылки
    if vip_package == 1:
        result += 300

    return result
#Название переменных 3/3 Магические числа 2/2 Драй 2/2 Логика 3/3 Оценка 10/10
