# Heartbleed Vulnerability Analysis

## Vulnerable Code (OpenSSL)
```c
unsigned int payload;
n2s(p, payload); // Read declared length from client
pl = p; // Point to payload

// VULNERABILITY: No bounds checking!
memcpy(bp, pl, payload); // Copy declared length, not actual

#Impact
Read server memory (64KB per request)

Private keys, passwords, session data exposure

No authentication required

#Mitigation
Input validation and bounds checking

#Update to patched OpenSSL versions
