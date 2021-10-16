# Avance 2

Raúl Castellanos Herrero
A01154891
Primer avance: 01/10/2021
Segundo avance: 09/10/2021

En la carpeta de _documentación_ se encuentran los diagramas y documentos. En la carpeta _proyecto_ se encuentra el codigo de lo trabajado junto con algunos archivos pruebas con los que se estuvo probando.

Para este segundo avance se agregaron tres clases principales
- Directory
- Scopes_directory
- Vars

Las clases de Scopes_directory y Vars, heredan las propiedades de Directory, aunque se sobreescribe el constructor y para el case de Scopes se sobreescribe también la función de print().

Ambas clases, son usadas para poder tener los diccionarios de procedimientos y de variables. 

Por otro lado, se agregaron los puntos neurolgicos necesarios para poder agregar las scopes (global, de las funciones, y del main) al parser. Junto con los necesarios para añadir las variables que se declaren en sus scopes correspondientes.

Finalmente, se añade tambien la clase Operation, que esta será usada más adelante para los cuádruplos. En esta clase se define el tipo que debe retornar, dados dos tipos y la operación (simbolo).
