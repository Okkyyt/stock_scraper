## terraform.tfvars に環境変数を記載

# ログイン情報
variable "aws_access_key" {
  description = "aws_access_key"
  type        = string
}

variable "aws_secret_key" {
  description = "aws_secret_key"
  type        = string
}

variable "aws_region" {
  description = "AWS Region"
  type        = string
}

# DBの情報
variable "db_username" {
  description = "DB username"
  type        = string
}

variable "db_password" {
  description = "DB password"
  type        = string
}