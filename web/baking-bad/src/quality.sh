#!/bin/sh
ingredient="$1"
[ -z "$ingredient" ] && { echo "No ingredient!"; exit 1; }

purity=$(awk -v s="$RANDOM" 'BEGIN{srand(s);printf "%.1f",80+20*rand()}')
echo "Ingredient: $ingredient"
echo "Purity: $purity%"
