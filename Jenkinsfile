pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'hertin12/projet_devops'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
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
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', 
                                                   usernameVariable: 'DOCKER_USER', 
                                                   passwordVariable: 'DOCKER_PASS')]) {
                    bat "docker login -u %DOCKER_USER% -p %DOCKER_PASS%"
                    bat "docker push %DOCKER_IMAGE%:%DOCKER_TAG%"
                    bat "docker push %DOCKER_IMAGE%:latest"
                }
            }
        }
        
        stage('Deploy with Docker Compose') {
            steps {
                bat "docker-compose down || echo 'No containers to stop'"
                bat "docker-compose up -d"
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline terminé avec succès !'
            echo "🌐 Application disponible sur http://localhost:5000"
            emailext body: "Le build ${BUILD_NUMBER} a réussi !\nApplication : http://localhost:5000",
                     subject: "Build Réussi - Flask CRUD App",
                     to: 'heritianajulien12@gmail.com'
        }
        failure {
            echo '❌ Le pipeline a échoué !'
            emailext body: "Le build ${BUILD_NUMBER} a échoué. Vérifier les logs Jenkins.",
                     subject: "Build Échoué - Flask CRUD App",
                     to: 'heritianajulien12@gmail.com'
        }
        always {
            bat "docker images"
        }
    }
}