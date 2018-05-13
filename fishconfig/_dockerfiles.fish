function __build_docker_image
  # Build the Docker image associated with this command.  If Make detects
  # that the target is already up-to-date, it prints:
  #
  #    make: `.docker/primitive' is up to date.
  #
  # which is just mildly annoying, so we check if the target is up-to-date
  # with a silent exit code before actually triggering it.
  pushd $ROOT
    if not make --question $ROOT/.docker/$argv[1]
      make docker-$argv[1]-build
    end
  popd
end

function __call_docker_image
  __build_docker_image $argv[1]

  # Then we run the container itself, passing the current directory into
  # the container and mapping through any arguments to the function straight
  # into the container.
  docker run --rm --tty \
    --volume (pwd):/data \
    --workdir /data \
    alexwlchan/$argv[1] $argv[2..-1]
end


function lessc
  __call_docker_image lessc $argv
end

function primitive
  __call_docker_image primitive $argv
end


function travis
  __build_docker_image travis

  # Travis needs:
  #
  #   - The current Git repo, because it uses the .git dir to work out the name
  #     of the associated GitHub repo, and set up certain things.
  #   - The ~/.travis dir, which is where Travis config lives
  #
  docker run --rm --tty \
    --volume (git rev-parse --show-toplevel):/repo \
    --volume ~/.travis:/root/.travis alexwlchan/travis $argv

end


function atool
  __call_docker_image atool $argv
end


function optipng
  __call_docker_image optipng $argv
end


function youtube-dl
  __call_docker_image youtube_dl $argv
end


function jq
  docker run --rm --interactive giantswarm/tiny-tools jq $argv
end


function aws
  set -q AWS_PROFILE; or set AWS_PROFILE default
  docker run --rm --interactive --tty \
    --volume (pwd):/data \
    --workdir /data \
    --volume ~/.aws:/root/.aws \
    --volume (pwd):/data \
    --workdir /data \
    --env AWS_PROFILE="$AWS_PROFILE" \
    mesosphere/aws-cli $argv
end


function wget
  __build_docker_image wget
  docker run --rm --volume (pwd):/data --workdir /data alexwlchan/wget $argv
end
