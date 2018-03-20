function s3mate
  set s3key $argv[1]
  set localname (basename $argv[1])

  pushd (mktemp -d)
    aws s3 cp "$s3key" "$localname"
    cp "$localname" "$localname.copy"
    mate -w "$localname"

    # If the files have changed, upload the new version back to S3.
    cmp "$localname" "$localname.copy" >/dev/null
    if [ "$status" != "0" ]
      aws s3 cp "$localname" "$s3key"
    end
  popd
end
