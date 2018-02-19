# If I'm inside the Wellcome platform repo, select the "wellcome" AWS key.
#
# TODO: As we get more repos, 'wellcome' is a poor name for this key.
# Rename it to something more suitable!
#
# TODO: Event handlers are cool!  You should write a blog post.
#
function __autoselect_platform_aws_profile --on-variable PWD
  set _PLATFORM_REPO "/Users/alexwlchan/repos/platform"
  set _PWD_ROOT (string sub --length (string length "$_PLATFORM_REPO") $PWD)

  if [ "$_PWD_ROOT" = "$_PLATFORM_REPO" ]
    set --export --global AWS_PROFILE wellcome
  else
    set --erase AWS_PROFILE
  end
end
