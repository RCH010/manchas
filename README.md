# Lenguaje Manchas


El lenguaje Manchas, es un lenguaje imperativo con el propósito de simplificar algunas operaciones básicas que se utilizan comúnmente en el análisis estadístico. 

<br><br>

# Manual de usuario

Para poder correr el programa es necesario tener instalado Python3. Por lo que se recomienda seguir lo que se indica en la [documentación oficial](https://www.python.org/downloads/).

Por otro lado, tambien se requiere la librería de matplot, por lo que tambien se recomienda seguir el manual de instalación de la [documentación oficial](https://matplotlib.org/1.4.3/faq/installing_faq.html).


Finalmente, hay descargar este repositorio.

`git clone https://github.com/RCH010/manchas.git`

<br><br>

# Getting Started

Antes de adentrarnos en los detalles, hay que saber la estructura general de algún archivo en el lenguaje Manchas. 

```
program miPrimerPrograma;
let  miVariableGlobal: int;

function suma: int(varA: int, varB: int)
let algunaVariableLocal: float;
{
  return varA + varB;
}

main()
let otraVarLocal: int;
{
  println("Hola mundo");
  otraVarLocal = suma(10, 30);
  print("El resultado es: ", otraVarLocal);
}
```

Como se puede ver, al inicio de cadda programa debe estar la declaración del programa, y después se pueden declarar las variables globales del programa. 

**Nota**: La declaración de variables globales siempre debe ser antes que la declaración de alguna función.

Después en este pequeño programa, se observa la declaración de la función `suma`. Esta es de tipo _int_ y recibe dos parametros de tipo _int_.

En el bloque _main_, función que siempre se ejecutara primero, y siempre debe existir en un progrma tambien puede tener sus varibales locales, y estas se definen antes de las llaves (`{}`) y despues de la palabra reservada `main()`.

En el main, comienza imprimiendo en consola (con un salto de línea) el mensaje _"Hola mundo"_. Despues, podemos ver que la función suma, regresa el resultado de la suma de `10` con `30` y ese resultado se guarda en `otraVarLocal`. Finalmente se imprime el mensaje de _"El resultado es: 40"_ en la consola.

**Nota:** Todos los identificadores que se definan podrán tener letras minusculas a mayusculas (azAZ) y números (0-9). Estos no podran tener caracteres fuera de los mencionados.

 
<br>

Por ejemplo:

> ✅ let miVariable2: int; <br>
> ❌ let mi_variable2: int

<br><br>


# Ejecución
Para ejecutar tu código. Primero hay que posicionarse en la carpeta `proyecto`, y hay que colcar el archivo de tu programa en el mismo nivel.

Una vez ahi ejecuta el siguiente comando en la terminal:
> `python3 main.py miArchivo.txt`

<br>
<br>

## Tipos de operaciones
Manchas soporta las operaciones más comunes de los lengujaes populares:

| Operación | Operador |
| ------------- | ------------- |
| Suma  | +  |
| Resta  | -  |
| Multiplicación  | *  |
| División  | /  |
| Mayor que  | >  |
| Menor que  | <  |
| Mayor igual que  | >=  |
| Menor igual que  | <=  |
| Igual  | ==  |
| Diferente  | !=  |
| And  | &&  |
| Or  | \|\|  |
| Asignación  | =  |

<br><br>


## Tipos de datos
En el lenguaje Manchas existen:

- int
- float
- bool
- char

_int_, serían números enteros y _float_, números con decimales. _bool_ es de tipo booleano, donde las palabras reservadas para sus asignaciones o comparaciones son: `true` y `false`. Finalmente _char_ serían de tipo caracter. 

Revisa el siguiente ejemplo:

```
program ejemplo;

main()
let unEntero: int;
let flotante1, flotante2: float,
let unBooleano: bool;
let letra: char;
{
  unEntero =  10;
  flotante1 = unEntero / 2;
  flotante2 = 10.5;
  unBooleano = true;
  unBooleano = unBooleano && (unEntero > flotante1);
  letra = 'a';
}
```


## Declaración de funciones

Las funciones siempre deberan comenzar con la palabra reservada `function` seguidas del identificador de las mismas, y luego su tipo de retorno separado por dos puntos. Por otro lado, las funciones se deben declarar antes del main.

`function <nombre>: <tipo-de-retorno>(<parametros>){<estatutos>}`

**Nota:** Las funciones no pueden recibir ni regresar arreglos, para soluciar esto, se recomienda que los arreglos que se usen en varias funciones se definan de forma global.

Los tipos de retorno de una función, pueden ser los mismos que los definidos anteriormente. Aunque si una función no regresa nada, habria que poner que `void` en su lugar.


Por ejemplo:

> ✅ function suma: int(a:int, b:int){} <br>
> ❌ function suma(a:int, b:int){} <br>
> ❌ suma: int(a:int, b:int){} <br>

## Declaración de variables

La declaración de varibales siempre debe comenzar con la palabra reservada `let` seguida del identificador, luego dos puntos (`:`), y su tipo y un punto y coma (`;`). Tambien se pueden definir varias varables en el mismo estatuto, sólo que estas deben ser del mismo tipo.


Por ejemplo:

> ✅ let mivar: float; <br>
> ✅ let mivarA, mivarB: bool; <br>
> ❌ let mivarA, mivarB: bool <br>
> ❌ mivarA, mivarB: bool; <br>
> ❌ let mivar int; <br>
> ❌ let mivar: void; <br>
> ❌ let mivar; <br>



## Ciclos

En el lenguaje Manchas existen dos ciclos, que son los más populares en otros lenguajes. 


### While

El ciclo while ejecutara su contenido hasta que la condición dada sea falsa. Revisa el siguiente ejemplo:

```
program ejemplo;

main()
let unNumero: int;
{
  unNumero = 0;
  while(unNumero <= 10) do {
    print("El número es:", unNumero);
    unNumero = unNumero + 1;
    println("");
  }
}
```

En el ejemplo anterior, estara imprimiendo en la consola el mensaje de :

_El número es: 0_ <br>
_El número es: 1_ <br>
_El número es: 2_ <br>
_..._ <br>
_El número es: 10_ <br>

<br>

### For

Por otro lado, tambien se cuenta con el ciclo condicional _for_, el cual sí tiene una sitáxis un poco diferente. Revisa el siguiente ejemplo:


```
program ejemplo;
let unArreglo: int[10];

function printData: void()
let i: int;
{
  println("");
  for(i = 0 to i == 10 by 1) {
    print(unArreglo[i], ", ");
  }
  println("");
}


main()
let i: int;
{
  unNumero = 0;
  for(i = 0 to i == 10 by 1) {
    unArreglo[i] = i + 5;
  }
  printData();
}
```

En el ejemplo anterior, estara imprimiendo en la consola el mensaje de :

_5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_


<br>



<br><br>

## Condicionales
Se cuenta con el estatuto condicional _if_. Este tiene las palabras reservadas `if` y `else`. El bloque `if` puede o no ser seguido por un bloque `else`.

Revisa el siguiente ejemplo:
```
program ejemplo;

main()
let unNumero: int;
{
  unNumero = random(1, 10);
  if(unNumero > 6) {
    println("El número es mayor a 6");
  } else {
    println("El número es menor a 6");
  }
}
``` 

## Arreglos
En el lengujae manchas existen los arreglos de una sóla dimensión. Su declaración es muy similar a la declaración de las variables, a excepción que se le agrega unos corchetes, y el número entero que indica su extensión.


Por ejemplo:

> ✅ let miArregloDeFlotantes: float[5]; <br>
> ✅ let arrB1, arrB2: bool[3]; <br>
> ❌ let mivarA[5], mivarB: bool;<br>
> ❌ mivarA, mivarB: bool; <br>
> ❌ let mivar int[10]]; <br>
> ❌ let mivar: void; <br>


**Nota:** Una vez definida el tamaño de un arreglo, esta no se puede modificar.


Para acceder o asignar al arreglo se utiliza la sintaxis popular de acceder por medio de los corchetes.

Para acceder a un arreglo se comienza en la posición 0, si se intenta acceder a una posición fuera del espacio en el que se definicio será un error.


Revisa el siguiente ejemplo:
```
program ejemplo;

main()
let miArreglo: int[10];
{
  miArreglo[0] = 8;
  miArreglo[1] = 8 + miArreglo[0];
  println(miArreglo[1] + miArreglo[0]);
}
``` 


## Otras funciones

En el lenguaje Manchas, existen algunas funciones adicionales que podrían ser de ayuda en algún programa.

Estas funciones, regresan un valor de tipo flotante:
- `mean(unArreglo)`
- `median(unArreglo)`
- `random(min, max)` (enteras)
- `variance(unArreglo)`
- `pvariance(unArreglo)`
- `stdev(unArreglo)`
- `pstdev(unArreglo)`
<br><br>

Esta función no regresa nada. Las dimensiones de los arrelgos que se manden deberan ser iguales.
- `plot(unArreglo, otroArreglo)`

<br>
**Nota:** unArreglo y otroArreglo deberían ser arrelgos de tipo enteras o flotantes

# Recursos adicionales

- En [esta liga](https://github.com/RCH010/manchas/blob/main/documentacion/Documentacion_Diseno_de_Compiladores_Manchas.pdf) se puede encontrar una documentación más extensa sobre todo el proyecto.
- [Aquí](https://drive.google.com/file/d/15ucJMUwM2G65ES1DFTJYteumtlkPws0a/view?usp=sharing) podras ver un pequeño vídeo demostrativo del lenguaje.

<br><br>

---

### Autor
Raúl Castellanos Herrero <br>
24-nov-2021