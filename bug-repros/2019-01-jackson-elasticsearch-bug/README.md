# 2019-01-jackson-elasticsearch-bug

This was an attempt to reproduce a bug we were seeing in the catalogue API ([wellcometrust/platform#3233](https://github.com/wellcometrust/platform/issues/3233)), where making the following query to Elasticsearch:

```json
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "type": {
              "value": "IdentifiedWork"
            }
          }
        }
      ]
    }
  },
  "from": -1863463012,
  "size": 100,
  "sort": [
    {
      "canonicalId": {
        "order": "asc"
      }
    }
  ]
}
```

would throw the following stack trace:

```
Cannot deserialize instance of `java.lang.String` out of START_OBJECT token
 at [Source: (byte[])"{"root_cause":[{"type":"illegal_argument_exception","reason":"numHits must be > 0; please use TotalHitCountCollector if you just need the total hit count"}],"type":"search_phase_execution_exception","reason":"all shards failed","phase":"query","grouped":true,"failed_shards":[{"shard":0,"index":"srw2krjhxh","node":"FxaQqjdVTuCjXsVhuEHKWQ","reason":{"type":"illegal_argument_exception","reason":"numHits must be > 0; please use TotalHitCountCollector if you just need the total hit count"}}],"caused_"[truncated 298 bytes]; line: 1, column: 657] (through reference chain: com.sksamuel.elastic4s.http.ElasticError["caused_by"]->com.sksamuel.elastic4s.http.ElasticError$CausedBy["caused_by"])
com.fasterxml.jackson.databind.exc.MismatchedInputException: Cannot deserialize instance of `java.lang.String` out of START_OBJECT token
 at [Source: (byte[])"{"root_cause":[{"type":"illegal_argument_exception","reason":"numHits must be > 0; please use TotalHitCountCollector if you just need the total hit count"}],"type":"search_phase_execution_exception","reason":"all shards failed","phase":"query","grouped":true,"failed_shards":[{"shard":0,"index":"srw2krjhxh","node":"FxaQqjdVTuCjXsVhuEHKWQ","reason":{"type":"illegal_argument_exception","reason":"numHits must be > 0; please use TotalHitCountCollector if you just need the total hit count"}}],"caused_"[truncated 298 bytes]; line: 1, column: 657] (through reference chain: com.sksamuel.elastic4s.http.ElasticError["caused_by"]->com.sksamuel.elastic4s.http.ElasticError$CausedBy["caused_by"])
	at com.fasterxml.jackson.databind.exc.MismatchedInputException.from(MismatchedInputException.java:63)
	at com.fasterxml.jackson.databind.DeserializationContext.reportInputMismatch(DeserializationContext.java:1342)
	at com.fasterxml.jackson.databind.DeserializationContext.handleUnexpectedToken(DeserializationContext.java:1138)
	at com.fasterxml.jackson.databind.DeserializationContext.handleUnexpectedToken(DeserializationContext.java:1092)
	at com.fasterxml.jackson.databind.deser.std.StringDeserializer.deserialize(StringDeserializer.java:63)
	at com.fasterxml.jackson.databind.deser.std.StringDeserializer.deserialize(StringDeserializer.java:10)
	at com.fasterxml.jackson.databind.deser.SettableAnyProperty.deserialize(SettableAnyProperty.java:154)
	at com.fasterxml.jackson.databind.deser.SettableAnyProperty.deserializeAndSet(SettableAnyProperty.java:134)
	at com.fasterxml.jackson.databind.deser.BeanDeserializerBase.handleUnknownVanilla(BeanDeserializerBase.java:1561)
	at com.fasterxml.jackson.databind.deser.BeanDeserializer.deserialize(BeanDeserializer.java:258)
	at com.fasterxml.jackson.databind.deser.BeanDeserializer._deserializeUsingPropertyBased(BeanDeserializer.java:441)
	at com.fasterxml.jackson.databind.deser.BeanDeserializerBase.deserializeFromObjectUsingNonDefault(BeanDeserializerBase.java:1287)
	at com.fasterxml.jackson.databind.deser.BeanDeserializer.deserializeFromObject(BeanDeserializer.java:326)
	at com.fasterxml.jackson.databind.deser.BeanDeserializer.deserialize(BeanDeserializer.java:159)
	at com.fasterxml.jackson.module.scala.deser.OptionDeserializer.deserialize(OptionDeserializerModule.scala:60)
	at com.fasterxml.jackson.module.scala.deser.OptionDeserializer.deserialize(OptionDeserializerModule.scala:11)
	at com.fasterxml.jackson.databind.deser.SettableBeanProperty.deserialize(SettableBeanProperty.java:530)
	at com.fasterxml.jackson.databind.deser.BeanDeserializer._deserializeWithErrorWrapping(BeanDeserializer.java:528)
	at com.fasterxml.jackson.databind.deser.BeanDeserializer._deserializeUsingPropertyBased(BeanDeserializer.java:417)
	at com.fasterxml.jackson.databind.deser.BeanDeserializerBase.deserializeFromObjectUsingNonDefault(BeanDeserializerBase.java:1287)
	at com.fasterxml.jackson.databind.deser.BeanDeserializer.deserializeFromObject(BeanDeserializer.java:326)
	at com.fasterxml.jackson.databind.deser.BeanDeserializer.deserialize(BeanDeserializer.java:159)
	at com.fasterxml.jackson.databind.ObjectMapper._readMapAndClose(ObjectMapper.java:4013)
	at com.fasterxml.jackson.databind.ObjectMapper.readValue(ObjectMapper.java:3121)
	at com.fasterxml.jackson.module.scala.experimental.ScalaObjectMapper.readValue(ScalaObjectMapper.scala:202)
	at com.fasterxml.jackson.module.scala.experimental.ScalaObjectMapper.readValue$(ScalaObjectMapper.scala:201)
	at com.sksamuel.elastic4s.json.JacksonSupport$$anon$1.readValue(JacksonSupport.scala:11)
	at com.sksamuel.elastic4s.http.ElasticError$.parse(ElasticError.scala:37)
	at com.sksamuel.elastic4s.http.DefaultResponseHandler.handle(ResponseHandler.scala:49)
	at com.sksamuel.elastic4s.http.ElasticClient.$anonfun$execute$1(ElasticClient.scala:33)
	at scala.util.Success.$anonfun$map$1(Try.scala:251)
	at scala.util.Success.map(Try.scala:209)
	at scala.concurrent.Future.$anonfun$map$1(Future.scala:288)
	at scala.concurrent.impl.Promise.liftedTree1$1(Promise.scala:29)
	at scala.concurrent.impl.Promise.$anonfun$transform$1(Promise.scala:29)
	at scala.concurrent.impl.CallbackRunnable.run(Promise.scala:60)
	at java.util.concurrent.ForkJoinTask$RunnableExecuteAction.exec(ForkJoinTask.java:1402)
	at java.util.concurrent.ForkJoinTask.doExec(ForkJoinTask.java:289)
	at java.util.concurrent.ForkJoinPool$WorkQueue.runTask(ForkJoinPool.java:1056)
	at java.util.concurrent.ForkJoinPool.runWorker(ForkJoinPool.java:1692)
	at java.util.concurrent.ForkJoinWorkerThread.run(ForkJoinWorkerThread.java:157)
```

The specific error that triggers this behaviour from Elasticsearch as follows:

```json
{
  "error": {
    "root_cause": [
      {
        "type": "illegal_argument_exception",
        "reason": "numHits must be > 0; please use TotalHitCountCollector if you just need the total hit count"
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "shard": 0,
        "index": "7cd0277a406af3b1",
        "node": "FxaQqjdVTuCjXsVhuEHKWQ",
        "reason": {
          "type": "illegal_argument_exception",
          "reason": "numHits must be > 0; please use TotalHitCountCollector if you just need the total hit count"
        }
      }
    ],
    "caused_by": {
      "type": "illegal_argument_exception",
      "reason": "numHits must be > 0; please use TotalHitCountCollector if you just need the total hit count",
      "caused_by": {
        "type": "illegal_argument_exception",
        "reason": "numHits must be > 0; please use TotalHitCountCollector if you just need the total hit count"
      }
    }
  },
  "status": 400
}
```

Poking around with a Python script (see `run.py`), I realised that the simplest request that triggered this particular response:

```http
GET /indexName/_search
{"from": -10}
```

Making this query using elastic4s (see `Main.scala`) worked fine, but threw the JSON error in the context of the API tests.
I eventually realised that we were running an outdated version of elastic4s in the API -- 6.4.0, whereas our Elastic Cloud clusters are at least 6.5.0.
