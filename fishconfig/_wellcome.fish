function sqs_redrive
  set queue_name "$argv[1]"
  ~/.virtualenvs/platform/bin/python ~/repos/dockerfiles/sqs_redrive/redrive.py \
    --src="https://sqs.eu-west-1.amazonaws.com/760097843905/"$queue_name"_dlq" \
    --dst="https://sqs.eu-west-1.amazonaws.com/760097843905/"$queue_name
end
