# Makefile — управление стендом.
# Отступы перед командами — табуляция, а не пробелы.

.PHONY: up down test clean

# Запуск виртуальной машины.
up:
	vagrant up

# Запуск сценария open-redirect.
up-open:
	vagrant ssh -c "cd /vagrant && docker-compose -f scenarios/open-redirect/docker-compose.yml up -d"

# Остановка сценария open-redirect.
down-open:
	vagrant ssh -c "cd /vagrant && docker-compose -f scenarios/open-redirect/docker-compose.yml down"

# Запуск всех тестов.
test:
	vagrant ssh -c "cd /vagrant && pytest tests/ -v"

# Полное удаление виртуальной машины.
clean:
	vagrant destroy -f