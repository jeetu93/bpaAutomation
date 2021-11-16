# get the access to lagg maping details

curl -X POST \
  http://100.67.249.20:2680/bits_automation/web/api/device/get-aggregator \
  -H 'Authorization: Basic YWRtaW46MTIzNDU2' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 2074491c-fefd-422b-b819-ad8532b3abde' \
  -H 'cache-control: no-cache' \
  -d '{
    "hostnames": "BGL_SGT_925_1AC_M_CASR920R080"
}'
