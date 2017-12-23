function lessc
  pushd $ROOT
    make $ROOT/.docker/lessc >/dev/null
  popd

  docker run --rm --tty --volume (pwd):/data alexwlchan/lessc "$argv"
end
