# Vagrantfile — описание виртуальной машины для стенда OAuth.
# Создаёт ВМ Ubuntu 22.04, пробрасывает порты, монтирует папку проекта
# и запускает Ansible-провижининг для установки Docker.

Vagrant.configure("2") do |config|
  # Базовая операционная система. Образ ubuntu/jammy64 — официальный.
  config.vm.box = "ubuntu/jammy64"
  config.vm.hostname = "oauth-lab"

  # Увеличиваем таймаут загрузки: на слабых машинах Ubuntu грузится дольше 300 секунд.
  config.vm.boot_timeout = 600

  # Проброс портов: сервисы стенда доступны на localhost хост-машины.
  # open-redirect: auth-server 8080, client 8081, attacker 8082.
  # csrf-state:   auth-server 8083, client 8084, attacker 8085.
  # jwt-bypass:   auth-server 8086.
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 8081, host: 8081
  config.vm.network "forwarded_port", guest: 8082, host: 8082
  config.vm.network "forwarded_port", guest: 8083, host: 8083
  config.vm.network "forwarded_port", guest: 8084, host: 8084
  config.vm.network "forwarded_port", guest: 8085, host: 8085
  config.vm.network "forwarded_port", guest: 8086, host: 8086

  # Монтируем папку проекта в /vagrant внутри ВМ.
  # Изменения на хосте сразу видны в ВМ и наоборот.
  config.vm.synced_folder ".", "/vagrant"

  # Провижининг через Ansible: установка Docker, Python-зависимостей.
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "provisioning/playbook.yml"
    ansible.verbose = "v"
  end

  # Ресурсы виртуальной машины.
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = 2
  end
end