# QuiniBot

[![Heroku Deploy](https://www.herokucdn.com/deploy/button.svg)](https://quinibot.herokuapp.com/)

## Breve descripción del proyecto

Se trata de un Bot de Telegram desarrollado en Python en el que se puede consultar la última quiniela en juego, así como los premios según los aciertos e incluso comprobar tu boleto, introduciendo tus resultados.

El bot responderá acorde a lo que el usuario introduzca

## Instalación

Para instalar el bot en una máquina es necesario descargar todos los ficheros que sean necesarios para la ejecución del bot. Para ello, ejecutando la orden:

```
git clone git@github.com:sergiocaceres/QuiniBot.git
```

Ahora tendremos que instalar las dependencias. Para ello, se ha creado un fichero llamado requirements.txt . No obstante, desde el Makefile se pueden instalar automáticamente, ejecutando 

```
make install
```

Para el caso del TOKEN de nuestro bot, lo que se ha hecho ha sido crear una variable de entorno con dicho valor, de esta manera no es necesaria ponerla en el código. 

Una vez que tenemos listo nuestro bot, podremos ejecutarlo con la orden

```
make execute
```

## Funcionamiento

Existen varias opciones para nuestro bot

* _/Resultados_: Nos muestra todos los resultados(1X2) de los equipos que se encuentran en la quiniela. Para ello, el partido debe haber finalizado
* _/Comprobar_: Nos muestra el número de aciertos que hemos tenido. Para ello, tendremos que pasarle nuestros resultados separados por guiones. Ejemplo: /comprobar 1-X-2-X-X-1.....-M-0
* _/Premio_: Devuelve la cantidad de dinero que nos ha tocado, según los aciertos que le digamos que hemos tenido. Ejemplo: /premio 14

Por supuesto, cada opción tiene su comprobación de si se han introducido de forma correcta los datos

## Despliegue

El bot se ha desplegado en Heroku. Para ello, necesitamos el fichero Procfile que se encuentra subido en la raíz de este repositorio

El bot se encuentra en funcionamiento y puede consultarse en https://telegram.me/QuinieBot

## Imágenes del bot en funcionamiento

Para iniciarlo basta con hacer /start y así poder ver las opciones que existen. Comprobamos también con uno de los premios para ver cuánto dinero nos ha tocado

![Imagen 1](http://i63.tinypic.com/2pyoqvl.png)

Vemos como nos imprime los resultados y comprobamos poniendo varios partidos acertados para ver que el pleno al 15 funciona y fallando el pleno al 15 para ver que el dinero está correcto

![Imagen 2](http://i65.tinypic.com/2uom875.png)

Ahora ponemos números aleatorios y vemos cuál es el resultado

![Imagen 3](http://i63.tinypic.com/epng9t.png)