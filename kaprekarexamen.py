num = int(input("Ingresa un número de 4 dígitos: "))

if len(set(str(num))) == 1:
    print("Error: no se permiten números con todas las cifras iguales.")
else:
    pasos = 0

    while num != 6174:
        cadena = str(num).zfill(4)
        
        mayor = int("".join(sorted(cadena, reverse=True)))
        
        menor = int("".join(sorted(cadena)))

        num = mayor - menor
        pasos += 1
        print("Paso", pasos, ":", mayor, "-", menor, "=", num)

    print("\nse logro el 6174 en", pasos, "pasos!")
