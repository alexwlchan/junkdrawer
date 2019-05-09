Consider the following server and test:

```ruby
# server.rb
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
```

```ruby
# test.rb
require 'minitest/autorun'
require 'rack/test'

require_relative './server'

class ExampleServerTest < Minitest::Test
  include Rack::Test::Methods

  def app
    ExampleServer.new
  end

  def test_get
    get '/foo'
    assert_equal 200, last_response.status
    assert_equal "hello world", last_response.body
  end
end
```

There's a bug in `server.rb` – the `"hello world"` should be wrapped in an array, like so:

```diff
-    ["200", {}, "hello world"]
+    ["200", {}, ["hello world"]]
```

If you run the test, it passes, but running the server directly and cURLing the `/` endpoint gets a NoMethodError:

```
[2018-11-26 12:33:13] ERROR NoMethodError: undefined method `each' for "hello world":String
	/usr/lib/ruby/gems/2.4.0/gems/rack-2.0.6/lib/rack/handler/webrick.rb:110:in `service'
	/usr/lib/ruby/2.4.0/webrick/httpserver.rb:140:in `service'
	/usr/lib/ruby/2.4.0/webrick/httpserver.rb:96:in `run'
	/usr/lib/ruby/2.4.0/webrick/server.rb:308:in `block in start_thread'
172.17.0.1 - - [26/Nov/2018:12:33:13 UTC] "GET / HTTP/1.1" 500 338
```

I'd guess that rack-test is making requests in a different way to the WEBrick server, and so it's missing this issue.
