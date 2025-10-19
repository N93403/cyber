#!/bin/sh
echo "🔍 Estrazione cookie"
grep "Cookie" request.txt | cut -d ":" -f2
