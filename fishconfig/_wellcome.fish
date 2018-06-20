function sqs_redrive
  set queue_name "$argv[1]"
  ~/.virtualenvs/platform/bin/python ~/repos/dockerfiles/sqs_redrive/redrive.py \
    --src="https://sqs.eu-west-1.amazonaws.com/760097843905/"$queue_name"_dlq" \
    --dst="https://sqs.eu-west-1.amazonaws.com/760097843905/"$queue_name
end


# Uses Keybase to decrypt a string encrypted with my PGP key.
#
# This adds the necessary PGP headers, which saves me a small amount
# of hassle each time.
#
function keybase_decrypt
  pushd (mktemp -d)
    echo "-----BEGIN PGP MESSAGE-----"  > encrypted.txt
    echo ""                            >> encrypted.txt
    pbpaste                            >> encrypted.txt
    echo "-----END PGP MESSAGE-----"   >> encrypted.txt

    keybase decrypt -i encrypted.txt
  popd
end


# Get the contents of the JSON record for a Miro image from the VHS.
#
function mirocat
  set s3url (python3 -c 'import sys; print(f"s3://wellcomecollection-vhs-sourcedata/miro/{sys.argv[1][:-3:-1]}/{sys.argv[1]}/0.json")' $argv[1])
  s3cat "$s3url" | tail -n 1 | python -c 'import sys, json; print(json.dumps(json.loads(json.loads(sys.stdin.read())["data"]), indent=2, sort_keys=True))'
end
