#!/bin/sh
echo "🔍 Analisi risposta XSS"
grep "<script>" xss_response.txt
