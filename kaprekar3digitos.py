
#rafael garcia kepler 3 digitos 

print("CONSTANTE DE KAPREKAR 3 DIGITOS")
numero = input("Ingresa un número de 3 dígitos: ")

if len(numero) != 3 or not numero.isdigit():
    print("Debes ingresar un número de 3 dígitos.")
else:
    
    if numero[0] == numero[1] == numero[2]:
        print("No se permiten números con todos los dígitos iguales.")
    else:
        num = int(numero)
        contador = 0

        while num != 495:
            digitos = list(str(num).zfill(3))  
            digitos.sort(reverse=True)
            mayor = int(""  .join(digitos))

            digitos.sort()
            menor = int("".join(digitos))

            num = mayor - menor
            contador += 1 
        print(f"Paso {contador}: {mayor} - {menor} = {num}")
        print(f"\nSISISISISISISISI llgaste a la constante de Kaprekar 495 en {contador} pasos.")
