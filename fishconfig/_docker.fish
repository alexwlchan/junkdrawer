# Clean up all the Docker images/containers on a system, but ~also clean
# up any markers to those images that I might have lying around.
function docker-clean
  docker rm (docker ps --all --quiet)
  docker rmi (docker images --all --quiet)
  find ~/repos -name .docker | xargs rm -rf
end
