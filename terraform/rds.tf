# サブネットグループの作成
resource "aws_db_subnet_group" "db_subnet_group" {
  # サブネットグループ名
  name       = "stock-scraper-db-subnet-group"
  # 説明
  description = "Subnet group for stock scraper RDS"
  # サブネット ID
  subnet_ids = [
    aws_subnet.subnet-1.id,
    aws_subnet.subnet-2.id,
    aws_subnet.subnet-3.id,
  ]
  # タグ
  tags = {
    Name = "stock-scraper-db-subnet-group"
  }
}

# RDS 用セキュリティグループ
resource "aws_security_group" "rds" {
  name   = "stock-scraper-rds-sg"
  vpc_id = aws_vpc.vpc.id

  ingress {
    description = "Allow PostgreSQL from office IP"
    protocol    = "tcp"
    from_port   = 5432
    to_port     = 5432
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "stock-scraper-rds-sg"
  }
}

# RDSインスタンスの作成
resource "aws_db_instance" "rds_instance" {
  # DBインスタンス識別子
  identifier = "stock-scraper-rds"
  # DB名
  db_name = "postgres"
  # DBエンジン
  engine = "postgres"
  # DBエンジンバージョン
  engine_version = "16.6"
  # DBインスタンスタイプ
  instance_class = "db.t3.micro"
  # ストレージタイプ
  storage_type = "gp2"
  # ストレージサイズ
  allocated_storage = 20
  # AWSサブネットグループ
  db_subnet_group_name = aws_db_subnet_group.db_subnet_group.name
  # セキュリティグループ
  vpc_security_group_ids = [aws_security_group.rds.id]
  # パスワード（環境変数）
  password = var.db_password
  # ユーザー名（環境変数）
  username = var.db_username
  # マルチAZ配置
  multi_az = false
  # 公開アクセス
  publicly_accessible = true
  # ファイナルスナップショット(バックアップ)を作る
  skip_final_snapshot = false
  final_snapshot_identifier = "rds-final-${formatdate("YYYYMMDDhhmmss", timestamp())}"

  tags = {
    Name = "stock-scraper-rds"
  }
}

# RDSインスタンスのエンドポイントを出力
output "rds_endpoint" {
  value = aws_db_instance.rds_instance.endpoint
}
# DB_NAMEを出力
output "db_name" {
  value = aws_db_instance.rds_instance.db_name
}