package delta
import io.delta.standalone.DeltaLog
import org.apache.hadoop.conf.Configuration
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

}
