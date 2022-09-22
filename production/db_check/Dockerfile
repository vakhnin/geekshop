FROM alpine

RUN apk update && apk add postgresql-client
CMD until pg_isready --host=db; do sleep 1; done

CMD echo "Postgres is up"
