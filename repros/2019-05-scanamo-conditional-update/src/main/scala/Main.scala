import com.amazonaws.services.dynamodbv2.AmazonDynamoDB
import org.scanamo.{Scanamo, Table}
import org.scanamo.auto._
import org.scanamo.syntax._


trait Named {
  val name: String
}

case class Version(number: Int)

case class VersionedObject(name: String, version: Version) extends Named


object Main extends Helpers with App {
  val client: AmazonDynamoDB = createDynamoDBClient()

  // Creates a table with a single hash key "name"
  val tableName: String = createTable(client)
  println(s"*** The new table is called $tableName")

  val table = Table[VersionedObject](tableName)

  val box = VersionedObject(
    name = "box",
    version = Version(number = 3)
  )

  // Store the box in the table
  storeT(client, tableName, box)

  // Now do a conditional update.  By conditioning on
  //
  //    version.number < box.version.number
  //
  // this update should fail.
  //
  val conditionalPut =
    table
      .given('version \ 'number < box.version.number)
      .put(box)
  val conditionalPutResult = Scanamo.exec(client)(conditionalPut)
  println(s"*** Result of putting the same box: $conditionalPutResult")
}
