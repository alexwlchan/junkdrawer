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
  ~/.virtualenvs/platform/bin/python $ROOT/fishconfig/vhscat.py "miro/$argv[1]"
end


# Get the contents of the JSON record for a Sierra record from the VHS.
#
function sierracat
  ~/.virtualenvs/platform/bin/python $ROOT/fishconfig/vhscat.py "sierra/$argv[1]"
end


# Save the contents of an SQS DLQ to S3
function sqs_freeze
  set queue_name "$argv[1]"
  ~/.virtualenvs/platform/bin/python ~/repos/dockerfiles/sqs_freezeray/freezeray.py \
    --src="https://sqs.eu-west-1.amazonaws.com/760097843905/"$queue_name"_dlq" \
    --bucket=wellcomecollection-platform-infra
end


alias ec2ssh "ssh -i ~/.ssh/wellcomedigitalplatform"

alias ec2scp "scp -i ~/.ssh/wellcomedigitalplatform"


# Aliases for the data science ASG
set -x PLATFORM_PYTHON ~/.virtualenvs/platform/bin/python

alias ds_start "$PLATFORM_PYTHON ~/repos/platform/data_science/scripts/toggle_asg.py --start"
alias ds_stop "$PLATFORM_PYTHON ~/repos/platform/data_science/scripts/toggle_asg.py --stop"
alias ds_tunnel "$PLATFORM_PYTHON ~/repos/platform/data_science/scripts/create_tunnel_to_asg.py"


alias issue_workflow_credentials "$PLATFORM_PYTHON $ROOT/aws/issue_temporary_credentials.py --account_id=299497370133 --role_name=platform-team-assume-role --profile_name=wellcomedigitalworkflow"


function amssh
  ssh -t -i ~/.ssh/wellcomedigitalworkflow \
    ec2-user@ec2-34-242-7-110.eu-west-1.compute.amazonaws.com \
      ssh -t -i wellcomedigitalworkflow "$argv[1]" sudo su
end
