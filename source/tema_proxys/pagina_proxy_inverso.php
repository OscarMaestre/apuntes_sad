<!DOCTYPE html>
<html>
  
  <head>
    <title>Página HTML para Servidor web con proxy inverso</title>
    <meta charset="utf-8">
  </head>
  <!--Cuerpo-->
  <body>
  <h1>Bienvenido a nuestra página</h1>
  <p>
    <?php

    $fecha=date("d/m/Y");
    $hora =date("h:i:s");

    echo "Esta página se generó en el servidor el $fecha a las $hora.";
    ?>
  </p>
  </body>
</html>