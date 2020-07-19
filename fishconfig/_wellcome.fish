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

function wrt
  docker run \
    --env AWS_PROFILE="$AWS_PROFILE" \
    --env AWS_SDK_LOAD_CONFIG=1 \
    --volume ~/.aws:/root/.aws \
    --volume (git rev-parse --show-toplevel):(git rev-parse --show-toplevel) \
    --workdir (git rev-parse --show-toplevel) \
    --interactive --tty --rm \
    wellcome/release_tooling:135a $argv
end
