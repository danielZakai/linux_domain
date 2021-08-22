# DATA FILE
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.26"
    }
  }
}
 # creds are for danzak5555
provider "aws" {
  region  = "${var.region}"
  profile = "default"
}
# USE TO MAKE SURE NAMES DON'T CONFLICT
resource "random_string" "random" {
  length  = 6
  special = false
  lower   = true
  upper   = false
}

# SECURITY ACCOUNT FILE

# SECURITY HUB ENABLE AND SET SECURITY STANDARDS
resource "aws_securityhub_account" "example" {}
# Enable basic AWS security standards
resource "aws_securityhub_standards_subscription" "secSub" {
        depends_on = [aws_securityhub_account.example]
        standards_arn = "arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0"
}

resource "aws_securityhub_action_target" "example" {
  depends_on  = [aws_securityhub_account.example]
  name        = "Send push chat"
  identifier  = "SendToChat"
  description = "This is custom action sends selected findings to chat"
}

# MACIE ENABLED
resource "aws_macie2_account" "test" {
        finding_publishing_frequency = "FIFTEEN_MINUTES"
        status = "ENABLED"
}


resource "null_resource" "previous" {}

resource "time_sleep" "wait_30_seconds" {
  depends_on = [null_resource.previous]

  create_duration = "40s"
}

# ENABLE GUARD DUTY
resource "aws_guardduty_detector" "example" {}

##### Need to add Guard Duty actions Here



# INSPECTOR ENABLEMENT AND RULES

data "aws_inspector_rules_packages" "rules" {}


########## Need to create a dynamic tagging system
resource "aws_inspector_resource_group" "inspect" {
  tags = {
    log = "inspect"
  }
}


resource "aws_inspector_assessment_target" "inspect" {
  name               = "SLZ-inspectorTarget-${random_string.random.id}"
  resource_group_arn = aws_inspector_resource_group.inspect.arn
}

resource "aws_inspector_assessment_template" "inspect" {
  name       = "SLZ-inspector-${random_string.random.id}"
  target_arn = aws_inspector_assessment_target.inspect.arn
  duration   = 3600

    rules_package_arns = data.aws_inspector_rules_packages.rules.arns
}



# IAM POLICIES AND ATTACH TO IAM USER

resource "aws_iam_policy" "SecretM-RW" {
  name = "SecAccount-ReadWrite-SecretManager-${random_string.random.id}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["secretsmanager:GetResourcePolicy", "secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret", "secretsmanager:ListSecretVersionIds", "secretsmanager:ListSecrets", "secretsmanager:CreateSecret", "secretsmanager:RotateSecret", "secretsmanager:UpdateSecret"]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}


# allow all IAM activities to this account
resource "aws_iam_policy" "all-IAM" {
  name = "SecAccount-all-IAM-${random_string.random.id}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["iam:*"]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

## setup IAM user and attach policies
resource "aws_iam_user" "user" {
  name = var.security_account_user
}
resource "aws_iam_user_policy_attachment" "attach-RW" {
  user       = aws_iam_user.user.name
  policy_arn = aws_iam_policy.SecretM-RW.arn
}

resource "aws_iam_user_policy_attachment" "attach-IAM" {
  user       = aws_iam_user.user.name
  policy_arn = aws_iam_policy.all-IAM.arn
}

# EVENT BUS + RULES

resource "aws_cloudwatch_event_bus" "sec" {
  name = "SLZ-secEventBus${random_string.random.id}"
}

resource "aws_cloudwatch_event_rule" "inspector" {
  name        = "SLZ-secHubRule-${random_string.random.id}"
  description = "log inspector logs to event bus"
  event_bus_name = aws_cloudwatch_event_bus.sec.name

  event_pattern = <<EOF
{
  "detail-type": [
    " AWS API Call via Security Hub"
  ]
}
EOF
}

resource "aws_cloudwatch_event_rule" "cloudtrailRule" {
  name        = "SLZ-cloudTrailRule-${random_string.random.id}"
  description = "log inspector logs to event bus"
  event_bus_name = aws_cloudwatch_event_bus.sec.name

  event_pattern = <<EOF
{
  "detail-type": [
    " AWS API Call via CloudTrail"
  ]
}
EOF
}
