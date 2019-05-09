require 'rack'

class ExampleServer
  def call(env)
    ["200", {}, "hello world"]
  end
end


if __FILE__ == $0
  app = Rack::Builder.new do
    use Rack::Reloader
    run ExampleServer.new
  end.to_app

  Rack::Server.start(app: app, Port: 8282, Host: "0.0.0.0")
end
