package delta
import util.Config
import io.delta.standalone.{DeltaLog, Snapshot}
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

  def getLatestSchema: StructType = {
    fetchLatestSnapshot()
    snapshot.getMetadata.getSchema
  }

  def getPartitionFileCount(partitions: Map[String, String]): Int = {
    fetchLatestSnapshot()
    var partitionFileCounter = 0
    snapshot.getAllFiles.forEach(file => {
      var filePartitions = file.getPartitionValues.toMap
      val diff = filePartitions.keys.toSet.diff(partitions.keySet)
      filePartitions = filePartitions.removedAll(diff)
      if(filePartitions == partitions) {
        partitionFileCounter += 1
      }
    })
    partitionFileCounter
  }

}
