// Experiments for https://stackoverflow.com/q/56245298/1558022

import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future
import scala.util.{Failure, Success, Try}

object Main extends App {
  def greet(name: String): Try[Unit] = Try {
    println(s"Hello $name!")
    Thread.sleep(1000)
    println(s"Goodbye $name!")
    ()
  }

  val x: Seq[Future[Unit]] = Seq("faythe", "grace", "heidi", "ivan", "judy").map { name =>
    Future(name).map {
      greet(_) match {
        case Success(()) => ()
        case Failure(err) => throw err
      }
    }
  }

  // val futures: Seq[Future[Unit]] = Seq(
  //   Future.fromTry { greet("alice") },
  //   Future.fromTry { greet("bob") },
  //   Future.fromTry { greet("carol") },
  //   Future.fromTry { greet("dave") },
  //   Future.fromTry { greet("eve") },
  // )

  //
  // Seq("alice", "bob", "carol", "dave", "eve").map { name =>
  //   Future.fromTry { greet(name) }
  // }
}
