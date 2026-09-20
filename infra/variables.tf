variable "student_id" {
  type        = string
  description = "Votre identifiant unique (ex: initiales ou prenom)"
  default     = "mourad" # L'étudiant met son nom ici
}
variable "environment" {
  type    = string
  default = "dev"
}
