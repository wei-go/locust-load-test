#!/bin/bash
export GRAFANA_HOST="${GRAFANA_HOST:=http://localhost:3000}"
export GRAFANA_CRED="${GRAFANA_CRED:=admin:admin}"
export GRAFANA_OVERWRITE="${GRAFANA_OVERWRITE:=false}"
export PGHOST="locust-timescale"
export PGPORT="${PGPORT:=5432}"
export DS_NAME="${DS_NAME:=locust_timescale}"

curl -u "$GRAFANA_CRED" $GRAFANA_HOST/api/datasources -XPOST -H "Accept: application/json" -H "Content-Type: application/json" -d '{"access": "proxy","basicAuth": false,"basicAuthPassword": "","basicAuthUser": "","database": "postgres","isDefault": false,"jsonData": {"postgresVersion": 1200,"sslmode": "disable", "timescaledb": true},"name": "'$DS_NAME'","orgId": 1,"password": "","readOnly": false,"secureJsonData": {"password": "password"},"type": "postgres","url": "'$PGHOST':'$PGPORT'","user": "postgres","version": 3,"withCredentials": false}'

ds=(10878 14423 14422 15419);
for d in "${ds[@]}"; do
  echo -n "Processing $d: "
  j=$(curl -s -k -u "$GRAFANA_CRED" $GRAFANA_HOST/api/gnet/dashboards/$d | jq .json )
  cleaned_json=$(echo "$j" | tr '\n' ' ')
  echo "{\"dashboard\":"${cleaned_json}",\"overwrite\":$GRAFANA_OVERWRITE,\"inputs\":[{\"name\":\"DS_LOCUST\",\"type\":\"datasource\", \"pluginId\":\"postgres\",\"value\":\"$DS_NAME\"}]}" > payload.json
  curl -v -k -u "$GRAFANA_CRED" -H "Accept: application/json"\
    -H "Content-Type: application/json"\
    -d @payload.json \
    $GRAFANA_HOST/api/dashboards/import; echo ""
done


