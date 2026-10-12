set -e

echo "[build] Starting OAuth lab environment"

if ! command -v docker >/dev/null 2>&1; then
    echo "[build] docker not found, please install Docker"
    exit 1
fi

for scenario in open-redirect csrf-state jwt-bypass; do
    echo "[build] Building scenario: $scenario"
    docker-compose -f scenarios/$scenario/docker-compose.yml build
done

echo "[build] All scenarios built successfully"