pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'hertin12/projet_devops'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat "echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin"
                }
            }
        }

        stage('Git Checkout') {
            steps {
                git credentialsId: 'github-credentials',
                    url: 'https://github.com/momode12/projet_devops.git',
                    branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% ."
                bat "docker tag %DOCKER_IMAGE%:%DOCKER_TAG% %DOCKER_IMAGE%:latest"
            }
        }

        stage('Push to DockerHub') {
            steps {
                bat "docker push %DOCKER_IMAGE%:%DOCKER_TAG%"
                bat "docker push %DOCKER_IMAGE%:latest"
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                bat "docker-compose down || echo No containers running"
                bat "docker-compose up -d --build"
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline terminé avec succès'
            emailext(
                subject: "SUCCESS - Build #${BUILD_NUMBER}",
                body: "Pipeline réussi 🚀\nApp: http://localhost:5000",
                to: "heritianajulien12@gmail.com"
            )
        }

        failure {
            echo '❌ Pipeline échoué'
            emailext(
                subject: "FAILED - Build #${BUILD_NUMBER}",
                body: "Pipeline échoué ❌\nVérifier Jenkins logs",
                to: "heritianajulien12@gmail.com"
            )
        }

        always {
            bat "docker images"
        }
    }
}