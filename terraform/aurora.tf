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

# AURORA 用セキュリティグループ
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

# AURORA DB クラスターの作成
resource "aws_rds_cluster" "aurora_cluster" {
  # クラスター名
  cluster_identifier = "stock-scraper-rds-cluster"
  # DBエンジン
  engine            = "aurora-postgresql"
  # DBエンジンバージョン
  engine_version    = "16.6"
  # DB名
  database_name     = var.db_name
  # マスターユーザー名
  master_username   = var.db_username
  # パスワード
  master_password   = var.db_password
  # DBサブネットグループ
  db_subnet_group_name = aws_db_subnet_group.db_subnet_group.name
  # VPCセキュリティグループ
  vpc_security_group_ids = [aws_security_group.rds.id]
  # ストレージサイズ
  serverlessv2_scaling_configuration {
    max_capacity             = 1.0
    min_capacity             = 0.5
  }
  engine_mode             = "provisioned" # Aurora Serverless v2ではこの指定でOK
  # DATA API の有効化
  enable_http_endpoint    = true

  ## スナップショットの設定
  backup_retention_period = 7 # スナップショットの保持期間
  preferred_backup_window = "07:00-09:00" # スナップショットの取得時間
  skip_final_snapshot = false # cluster削除時にスナップショットを取得するかどうか
  final_snapshot_identifier = "final-snap-${formatdate("YYYYMMDDhhmmss", timestamp())}" # スナップショットの名前

  tags = {
    Name = "stock-scraper-aurora-cluster"
  }
}

# AURORA DB インスタンスの作成
resource "aws_rds_cluster_instance" "rds_instance" {
  # クラスター名
  cluster_identifier = aws_rds_cluster.aurora_cluster.id
  # DBインスタンスタイプ
  instance_class     = "db.serverless"
  # DBエンジン
  engine            = aws_rds_cluster.aurora_cluster.engine
  # DBエンジンバージョン
  engine_version    = aws_rds_cluster.aurora_cluster.engine_version
  # パブリックアクセス
  publicly_accessible = true
  # DBサブネットグループ
  db_subnet_group_name = aws_db_subnet_group.db_subnet_group.name

  tags = {
    Name = "stock-scraper-rds-instance"
  }
}


# RDSインスタンスのエンドポイントを出力
output "rds_endpoint" {
  value = aws_rds_cluster.aurora_cluster.endpoint
}
# DB_NAMEを出力
output "db_name" {
  value = aws_rds_cluster.aurora_cluster.database_name
}