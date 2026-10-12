# build.ps1 — сборка стенда OAuth из Windows.
# Запуск: .\build.ps1

Write-Host "[build] Starting OAuth lab environment"

if (-not (Get-Command vagrant -ErrorAction SilentlyContinue)) {
    Write-Host "[build] vagrant not found, please install Vagrant"
    exit 1
}

Write-Host "[build] Starting VM"
vagrant up

Write-Host "[build] Building all scenarios inside VM"
vagrant ssh -c "cd /vagrant && ./build.sh"

Write-Host "[build] Done"