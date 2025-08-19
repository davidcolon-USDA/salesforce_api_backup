provider "aws" {
  region = var.region
}

terraform {
  backend "local" {
    path = "state_files/terraform.tfstate"
  }
}
