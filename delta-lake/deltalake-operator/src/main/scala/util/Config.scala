package util

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.Path

object Config {
  val FS_CONFIG_PATH: String = sys.env.getOrElse("CONFIG_PATH", "src/main/resources/fs.xml")

  def getCommonFSConfiguration: Configuration = {
    val fsConf: Configuration = new Configuration()
    fsConf.addResource(new Path(FS_CONFIG_PATH))
    fsConf
  }
}
