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
