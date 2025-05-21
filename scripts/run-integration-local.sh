#!/usr/bin/env bash
set -e

# 1) Up server (assumes in neighbouring directory)
pushd ../federated-learning-clinical-safety-server
docker compose -f docker-compose.test.yml up --build -d

# 2) Extract token
LOGS=$(docker compose -f docker-compose.test.yml logs api)
export SDK_TEST_TOKEN=$(echo "$LOGS" | grep Token: | head -n1 | sed -E 's/.*Token:[[:space:]]*//')
echo "Using token=$SDK_TEST_TOKEN"
popd

# 3) Run SDK tests
export API_BASE_URL="http://localhost:8000/api"
poetry install
poetry run pytest src/tests/test_integration.py -q

# 4) Tear down
pushd ../federated-learning-clinical-safety-server
docker compose -f docker-compose.test.yml down --volumes
popd
