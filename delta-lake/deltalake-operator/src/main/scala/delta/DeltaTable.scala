package delta
import io.delta.standalone.expressions.{And, EqualTo, Expression, Literal}
import util.Config
import io.delta.standalone.{DeltaLog, DeltaScan, Snapshot}
import io.delta.standalone.types.StructType
import org.apache.hadoop.conf.Configuration
import scala.collection.convert.ImplicitConversions.`map AsScala`

class DeltaTable(tablePath: String, partitions: Seq[String]) {
  private val config: Configuration = Config.getCommonFSConfiguration
  private val deltaLog: DeltaLog = DeltaLog.forTable(config, tablePath);
  private var snapshot: Snapshot = deltaLog.update();

  private def fetchLatestSnapshot(): Unit = {
    snapshot = deltaLog.update()
  }

  private def getLatestSchema: StructType = {
    fetchLatestSnapshot()
    snapshot.getMetadata.getSchema
  }

  def getLatestVersion: Long = {
    fetchLatestSnapshot()
    snapshot.getVersion
  }

  def getPartitionFileCount(partitions: Map[String, String]): Int = {
    if(partitions.isEmpty){
      0
    } else {
      fetchLatestSnapshot()
      var partitionFileCounter = 0
      snapshot.getAllFiles.forEach(file => {
        var filePartitions = file.getPartitionValues.toMap
        val diff = filePartitions.keys.toSet.diff(partitions.keySet)
        filePartitions = filePartitions.removedAll(diff)
        if (filePartitions == partitions) {
          partitionFileCounter += 1
        }
      })
      partitionFileCounter
    }
  }

  def betterGetPartitionFileCount(partitions: Map[String, String]): Int = {
    val schema: StructType = getLatestSchema
    // Generate scan expression
    val partitionExps: List[Expression] =
      partitions.keys
        .map(key => new EqualTo(schema.column(key), Literal.of(partitions.get(key).orNull)))
        .toList
        .filter(exp => exp != null)
    if(partitionExps.nonEmpty){
      val scan: DeltaScan = deltaLog
        .startTransaction
        .markFilesAsRead(partitionExps.reduce(new And(_, _)))
      var fileCounter: Int = 0;
      val iter = scan.getFiles
      while(iter.hasNext) {
        fileCounter += 1;
        iter.next()
      }
      fileCounter
    } else {
      0
    }
  }
}
