# VPC
resource "aws_vpc" "vpc" {
    # IPv4 CIDR ブロック
    cidr_block = "172.16.1.0/24"
    instance_tenancy = "default"

    # AuroraDBを使用するために必要なオプション
    enable_dns_support = true
    enable_dns_hostnames = true

    tags = {
        # 表示名
        Name = "stock-scraper-vpc"
    }
}

# サブネット1（ap-northeast-1a）
resource "aws_subnet" "subnet-1" {
    # VPC ID
    vpc_id = aws_vpc.vpc.id
    # IPv4 CIDR ブロック
    cidr_block = "172.16.1.0/26"
    # アベイラビリティゾーン
    availability_zone = "ap-northeast-1a"
    tags = {
        # 表示名
        Name = "stock-scraper-aurora-subnet-1"
    }
}

# サブネット2（ap-northeast-1c）
resource "aws_subnet" "subnet-2" {
    # VPC ID
    vpc_id = aws_vpc.vpc.id
    # IPv4 CIDR ブロック
    cidr_block = "172.16.1.64/26"
    # アベイラビリティゾーン
    availability_zone = "ap-northeast-1c"
    tags = {
        # 表示名
        Name = "stock-scraper-aurora-subnet-2"
    }
}

# サブネット3（ap-northeast-1d）
resource "aws_subnet" "subnet-3" {
    # VPC ID
    vpc_id = aws_vpc.vpc.id
    # IPv4 CIDR ブロック
    cidr_block = "172.16.1.128/26"
    # アベイラビリティゾーン
    availability_zone = "ap-northeast-1d"
    tags = {
        # 表示名
        Name = "stock-scraper-aurora-subnet-3"
    }
}

# インターネットゲートウェイ
resource "aws_internet_gateway" "igw" {
    # VPC ID
    vpc_id = aws_vpc.vpc.id
    tags = {
        # 表示名
        Name = "stock-scraper-igw"
    }
} 

# ルートテーブル
resource "aws_route_table" "route-table-1" {
    # VPC ID
    vpc_id = aws_vpc.vpc.id
    # ルート
    route {
        # CIDR ブロック
        cidr_block = "0.0.0.0/0"
        # インターネットゲートウェイID
        gateway_id = aws_internet_gateway.igw.id
    }
    tags = {
        # 表示名
        Name = "stock-scraper-route-table-1"
    }
}

# サブネット1のルートテーブル関連付け
resource "aws_route_table_association" "rta-1" {
    # サブネット ID
    subnet_id = aws_subnet.subnet-1.id
    # ルートテーブル ID
    route_table_id = aws_route_table.route-table-1.id
}

# サブネット2のルートテーブル関連付け
resource "aws_route_table_association" "rta-2" {
    # サブネット ID
    subnet_id = aws_subnet.subnet-2.id
    # ルートテーブル ID
    route_table_id = aws_route_table.route-table-1.id
}

# サブネット3のルートテーブル関連付け
resource "aws_route_table_association" "rta-3" {
    # サブネット ID
    subnet_id = aws_subnet.subnet-3.id
    # ルートテーブル ID
    route_table_id = aws_route_table.route-table-1.id
}
