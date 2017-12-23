function __call_docker_image
  pushd $ROOT
    make $ROOT/.docker/$argv[1] >/dev/null
  popd

  docker run --rm --tty --volume (pwd):/data alexwlchan/$argv[1] "$argv[2..-1]"
end


function lessc
  __call_docker_image lessc
end
