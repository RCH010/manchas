# Avances del Proyecto

Raúl Castellanos Herrero  
A01154891

- Primer avance: 01/10/2021
- Segundo avance: 09/10/2021
- Tercer avance: 16/10/2021


En la carpeta de _documentación_ se encuentran los diagramas y documentos. En la carpeta _proyecto_ se encuentra el codigo de lo trabajado junto con algunos archivos pruebas con los que se estuvo probando.

---

## Primer avance:

Para este primer avance se diseño el la sintaxis del lenguaje. Se crearon los diagramas y gramatica y se realizo el analizador sintáctico usando PLY, este comprueba la sintáxis de un archivo txt como input y valida que sea correcta o incorrecta.

<br>

## Segundo avance:

Para este segundo avance se agregaron tres clases principales
- Directory
- Scopes_directory
- Vars

Las clases de _Scopesdirectory_ y _Vars_, heredan las propiedades de _Directory_, aunque se sobreescribe el constructor y para el case de Scopes se sobreescribe también la función de print().

Ambas clases, son usadas para poder tener los diccionarios de procedimientos y de variables. 

Por otro lado, se agregaron los puntos neurolgicos necesarios para poder agregar las scopes (global, de las funciones, y del main) al parser. Junto con los necesarios para añadir las variables que se declaren en sus scopes correspondientes.

Finalmente, se añade tambien la clase Operation, que esta será usada más adelante para los cuádruplos. En esta clase se define el tipo que debe retornar, dados dos tipos y la operación (simbolo).

<br>

## Tercer Avance

En este tercer avance se trabaja en la generación de código  de expresiones aritmeticas y asignaciones. Aunque quedan aquí pendientes la generación de algunos estatutos (print, read, mean, mode, etc...). 

Se crea la clase _Quadruples_, la cual sirve para representar las producciones de código. 

Utilizando esta clase, se añaden los puntos neuralgicos correspontientes para ir creando los cuadriplos de lo mencionado anteriormente. Para esto se crean varias pilas (operands, operators, types, jumps) que son utilizadas para agregar todo con forme su correcta precendencia.

Finalmente se hacen modificaciones en los archivos de test, y se añade uno, para seguir probando estos avances.

<br>

## Cuarto Avance

Para este cuarto avance, se trabajó con los estatutos condicionales, el while quedo implementado, aunque el for todavía tiene algunos casos extraños que sigo trabajando en ellos.

Además, reorganice algunas cosas del código que ya estaban complicándose, cree un constructor, y unos métodos para modificar sus atributos en los cuádruplos.

Durante esta semana, agregaré los puntos neurálgicos restantes y comenzaré a implementar la memoria para poder ya guardar direcciones en lugar de referencias que todavía no están. Además de revisar el código para la generación de código de funciones.

<br>


## Quinto Avance

