ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.13.10"

lazy val deltalake_operator = (project in file("."))
  .settings(
    organization := "git.leehuwuj.olh",
    name := "deltalake-operator",
    libraryDependencies ++= Seq(
      "org.scalatest" %% "scalatest" % "3.2.14" % Test,
      "io.delta" %% "delta-standalone" % "0.5.0",
      "org.apache.hadoop" % "hadoop-client" % "3.3.1",
      "org.apache.hadoop" % "hadoop-aws" % "3.3.1",
      "org.apache.hadoop" % "hadoop-common" % "3.3.1"
    )
  )
