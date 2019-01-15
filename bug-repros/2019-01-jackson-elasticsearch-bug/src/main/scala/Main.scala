import com.sksamuel.elastic4s.http.ElasticDsl._
import com.sksamuel.elastic4s.http.index.IndexResponse
import com.sksamuel.elastic4s.http.search.SearchResponse
import com.sksamuel.elastic4s.http.{ElasticClient, Response}
import com.sksamuel.elastic4s.searches.SearchRequest
import com.sksamuel.elastic4s.searches.sort.SortOrder
import org.apache.http.auth.{AuthScope, UsernamePasswordCredentials}
import org.apache.http.HttpHost
import org.apache.http.impl.client.BasicCredentialsProvider
import org.apache.http.impl.nio.client.HttpAsyncClientBuilder
import org.elasticsearch.client.RestClient
import org.elasticsearch.client.RestClientBuilder.HttpClientConfigCallback

import scala.util.Random


class ElasticCredentials(username: String, password: String)
    extends HttpClientConfigCallback {
  val credentials = new UsernamePasswordCredentials(username, password)
  val credentialsProvider = new BasicCredentialsProvider()
  credentialsProvider.setCredentials(AuthScope.ANY, credentials)

  override def customizeHttpClient(
    httpClientBuilder: HttpAsyncClientBuilder): HttpAsyncClientBuilder = {
    httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider)
  }
}


object Example extends App {
  val indexName = "testing_" + Random.alphanumeric.take(10).mkString.toLowerCase
  println(s"The index is $indexName")

  // Set up authentication for the Elasticsearch client.
  val restClient = RestClient
    .builder(new HttpHost("localhost", 9200, "http"))
    .setHttpClientConfigCallback(new ElasticCredentials("elastic", "changeme"))
    .build()

  val client: ElasticClient = ElasticClient.fromRestClient(restClient)

  val indexResponse: Response[IndexResponse] =
    client
      .execute { indexInto(indexName / "doctype").fields("name" -> "alex") }
      .await
  println(indexResponse)

  val searchRequest =
    search(indexName)
      .from(-10)

  println(s"@@AWLC searchRequest = ${searchRequest.show}")

  val response: Response[SearchResponse] =
    client
      .execute { searchRequest }
      .await

  println(response.error)

  client.close()
}
