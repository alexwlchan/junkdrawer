FROM docker.elastic.co/elasticsearch/elasticsearch-oss:6.1.1

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "An Elasticsearch instances optimised for low-power systems"

# Specifically, I want to run Elasticsearch for some private applications on
# a 1GB Linode instance.  There should only ever be one user (me!), which
# means the load on the cluster will be minimal -- I don't need 64GB!

RUN bin/elasticsearch-plugin remove --purge ingest-geoip
RUN bin/elasticsearch-plugin remove --purge ingest-user-agent

ENV ES_JAVA_OPTS "-Xms512M -Xmx512M"
ENV discovery.type single-node
