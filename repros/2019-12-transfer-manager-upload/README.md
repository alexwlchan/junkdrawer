# transfer-manager-upload

I was seeing a bug in some Scala tests where calling `AmazonS3.putObject()` would never assign a storage class to an object, even when one was set on the request.  I wasn't sure if this was a bug in the AWS SDK (unlikely) or the test container we were using (more likely), so I wrote a Java repro against the real S3.

This code sets the correct storage class when writing to real S3, so there's a bug somewhere in our test container.
