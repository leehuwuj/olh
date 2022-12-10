package delta
import org.scalatest.funsuite.AnyFunSuite
import util.TestUtils.withTempDir

class DeltaTableTest extends AnyFunSuite {
  test("tmp table data zero partition count") {
    withTempDir(dir => {
      val table = new DeltaTable(dir.getCanonicalPath, Seq())
      val fileNum = table.getPartitionFileCount(Map(("lang", "en")))
      assert(fileNum == 0)
    })
  }

  test("real table data have right number of files in a partition") {
    val table: DeltaTable = new DeltaTable(
      "src/test/resources/testtable",
      Seq()
    )
    val fileNum = table.getPartitionFileCount(Map())
    assert(fileNum == 1)
  }

  test("test minio data with Delta scan") {
    val table: DeltaTable = new DeltaTable(
      "s3a://lake/warehouse/tweetsfact",
      Seq()
    )
    val fileNum1 = table.getPartitionFileCount(Map("lang" -> "en"))
    val fileNum2 = table.betterGetPartitionFileCount(Map("lang" -> "en"))
    assert(fileNum1 == fileNum2)
  }

}
