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

Este quinto avances tiene un gran progreso en cuando a la generación del código intermedio. Se añadieron los puntos neuralgicos para algunos estatutos líneales como el del main, return, entre otros. 

Principalmente en este avance se trabajo con las funciones, y todo lo que implico. Se creo un arreglo para los parametros, y se modifica el directorio de funciones para añadir donde empieza, y la memoria. Por otro lado se añaden todos los puntos neuralgicos para la definición y utilización de las funciones.

Finalmente comence a definir como estará estructurada la memoria para ya implementar esta ídea en la creación de código intermedio. Quedo pendiente empezar a trabajar con la maquina virtual para la ejecición de expresiones aritmeticas.


<br>

## Sexto Avance

Para este avance me enfrenté con varios problemas que no me había dado cuenta, problemas que había estado acarreando desde entregas pasadas. Lo cual implicó cambios en la gramática y algunas refactorizaciones en todo el proyecto.

Para este avance se definió como se estaría trabajando con la memoria y se hicieron los cambios necesarios para que el código intermedio fuera totalmente escrito con direcciones de memoria. Cambios como, la tabla de constantes y validaciones de la memoria a la que se accedía.

Además, se añadieron los puntos neurálgicos para la definición de y uso de arreglos, y se crearon sus cuádruplos correspondientes.

Finalmente, se estuvo trabajando en la máquina virtual, ya se tienen todas las operaciones aritméticas y booleanas, y además los condicionales y ciclos.


<br>

## Séptimo Avance

Con este avance se comenzaron a unir todas las piezas que estaban pendientes. Primeramente, se arreglaron unos errores detectados al llamar una función. Se corrigieron los problemas que estaban causando una llamada de una función que esperaba un valor de retorno y una función que podía ser sin ningún valor de retorno.

Después, se creó la clase Memory, que sería la base para poder tener la memoria en la máquina virtual. Con esto, se podrían agregar validaciones que estaban pendientes sobre los límites de memoria. Una vez que esto se logró, se implementó la ejecución de funciones en la máquina virtual.

Además, se implementó el manejo de apuntadores para poder hacer uso de las direcciones virtuales que son apuntadores. Con esto, se implementó también la ejecución de código intermedio que utilizará arreglos. La ejecución de arreglos implico de nuevo varios cambios en los puntos neurálgicos ya existentes y en la gramática porque estaban creándose unas inconsistencias al momento de indexar en los arreglos.

Por otro lado, se completó la generación de cuádruplos para los estatutos pendientes, aquí incluidas las funciones particulares del programa. Con esto también se trabajó con su ejecución.

Finalmente, se realizaron varios de los programas que se estarán utilizando como pruebas para validar el funcionamiento del programa y se comenzó a trabajar en la documentación del proyecto.
