import com.amazonaws.auth.{AWSStaticCredentialsProvider, BasicAWSCredentials}
import com.amazonaws.client.builder.AwsClientBuilder.EndpointConfiguration
import com.amazonaws.services.dynamodbv2.model._
import com.amazonaws.services.dynamodbv2.util.TableUtils.waitUntilActive
import com.amazonaws.services.dynamodbv2.{AmazonDynamoDB, AmazonDynamoDBClientBuilder}
import org.scanamo.{DynamoFormat, Scanamo, Table}
import org.scanamo.syntax._

import scala.util.Random

trait Helpers {
  def createDynamoDBClient(): AmazonDynamoDB =
    AmazonDynamoDBClientBuilder.standard
      .withCredentials(
        new AWSStaticCredentialsProvider(
          new BasicAWSCredentials("accessKey", "secretKey")
        )
      )
      .withEndpointConfiguration(
        new EndpointConfiguration("http://localhost:8000", "localhost")
      )
      .build()

  def createTable(client: AmazonDynamoDB): String = {
    val name = Random.alphanumeric.take(10) mkString

    client.createTable(
      new CreateTableRequest()
        .withTableName(name)
        .withKeySchema(new KeySchemaElement()
          .withAttributeName("name")
          .withKeyType(KeyType.HASH))
        .withAttributeDefinitions(
          new AttributeDefinition()
            .withAttributeName("name")
            .withAttributeType("S")
        )
        .withProvisionedThroughput(new ProvisionedThroughput()
          .withReadCapacityUnits(1L)
          .withWriteCapacityUnits(1L)
        )
    )

    waitUntilActive(client, name)

    name
  }

  def storeT[T <: Named](
    client: AmazonDynamoDB,
    tableName: String,
    t: T)(
    implicit evidence: DynamoFormat[T]): Unit = {
    val table = Table[T](tableName)

    val putOp = table.put(t)
    val putResult = Scanamo.exec(client)(putOp)
    println(s"*** Result of putting t: $putResult")

    val getOp = table.get('name -> t.name)
    val getResult = Scanamo.exec(client)(getOp)
    val storedBox = getResult.get.right.get
    println(s"*** Stored value of t: $storedBox")
  }
}
