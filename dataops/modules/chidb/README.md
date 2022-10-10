# CLickHouse


```bash


kubectl patch svc clickhouse-chi-dev \
-p '{"spec":{"ports":[{"port":9000,"targetPort":9000,"name":"https"}],"type":"NodePort"}}'
```

```bash
clickhouse-client -h ip-address-or-lb-domain -u clickhouse_operator --password clickhouse_operator_password 
```