function __call_docker_image

  # First we build the Docker image associated with this command.  If Make
  # detects that the target is already up-to-date, it prints:
  #
  #    make: `.docker/primitive' is up to date.
  #
  # which is just mildly annoying, so we check if the target is up-to-date
  # with a silent exit code before actually triggering it.
  pushd $ROOT
    if not make --question $ROOT/.docker/$argv[1]
      make $ROOT/.docker/$argv[1]
    end
  popd

  # Then we run the container itself, passing the current directory into
  # the container and mapping through any arguments to the function straight
  # into the container.
  docker run --rm --tty --volume (pwd):/data alexwlchan/$argv[1] $argv[2..-1]
end


function lessc
  __call_docker_image lessc $argv
end

function primitive
  __call_docker_image primitive $argv
end

function youtube-dl
  __call_docker_image youtube_dl $argv
end


function jq
  docker run --rm --interactive giantswarm/tiny-tools jq $argv
end


function aws
  set -q AWS_PROFILE; or set AWS_PROFILE default
  docker run --interactive --tty \
    --volume ~/.aws:/root/.aws \
    --env AWS_PROFILE="$AWS_PROFILE" \
    mesosphere/aws-cli $argv
end
