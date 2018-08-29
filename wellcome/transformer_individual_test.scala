// This is a snippet for dropping into SierraTransformableTransformerTest
// to run when you have a specific JSON string that's failing.

it("transforms this record") {
  val jsonString = """<...>"""
  import SierraTransformable._
  val transformable = fromJson[SierraTransformable](jsonString).get

  transformToWork(transformable)
}
