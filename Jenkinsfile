pipeline {
    agent any
    stages {
        stage('Scan') {
            steps {
                sh "ls -la"
                script {
                    scannerHome = tool 'sonarqube-scanner'
                }
                withSonarQubeEnv(installationName: 'NM-SonarQube') {
                    sh "ls -la ${scannerHome}/bin/sonar-scanner"
                    sh '''${scannerHome}/bin/sonar-scanner \
                         -Dsonar.projectKey=nithursan27 \
                         -Dsonar.projectName=filmproject \
                         -Dsonar.analysis.mode=publish \
                         -Dsonar.sources=api'''
                }
            }
        }
        stage('SSH') {
            steps{
                script{
                    withCredentials([sshUserPrivateKey(credentialsId: 'nm-ssh', keyFileVariable: 'identity')]) {
                        def remote=[:]
                        remote.name = 'film-vm'
                        remote.host = '34.9.22.196'
                        remote.user = 'nmuraleetharan'
                        remote.identityFile = identity
                        remote.allowAnyHosts = true

                        writeFile file: 'deploy.sh', text: '''\
                        pkill gunicorn
                        cd ~/filmproject
                        source venv/bin/activate
                        git pull
                        pip install -r requirements.txt
                        gunicorn -b 0.0.0.0 "app:create_app()" --daemon'''

                        sshPut remote: remote, from: 'deploy.sh', into: '.'
                        sshCommand remote: remote, command: 'chmod +x deploy.sh'

                        sshCommand remote: remote, command: './deploy.sh'
                    }
                }
            }
        }
    }
}