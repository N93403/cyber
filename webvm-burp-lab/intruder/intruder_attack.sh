#!/bin/sh
echo "🚀 Simulazione brute-force login"
for user in admin guest test; do
  for pass in 1234 password admin; do
    echo -e "POST /login.php HTTP/1.1\nHost: 192.168.0.34\nContent-Type: application/x-www-form-urlencoded\n\nusername=$user&password=$pass" > intruder_sample.txt
    echo "Trying $user:$pass"
    cat intruder_sample.txt
    echo "------"
  done
done
