#!/bin/bash

num_azar=$RANDOM
echo "Generador de números aleatorios"
echo "-------------------------------"
echo "El número al azar que elegí es:$num_azar"
echo 
echo "Guardando el número en /app/num_azar.txt"
echo $num_azar >> /app/num_azar.txt