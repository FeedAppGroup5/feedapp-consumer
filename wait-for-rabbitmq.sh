#!/bin/sh
# wait-for-rabbitmq.sh

set -e

host="$1"
shift
cmd="$@"

until nc -z "$host" 5672; do
  echo "Waiting for RabbitMQ at $host:5672..."
  sleep 2
done

>&2 echo "RabbitMQ is up - executing command"
exec $cmd
