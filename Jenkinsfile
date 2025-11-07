pipeline {
    agent any
    stages {
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
                        
                        
                        sshCommand remote: remote, command: 'ps aux | grep gunicorn > gunicorn_bg_instances'
                        sshCommand remote: remote, command: './kill_bg_gunicorn.sh'
                        sshCommand remote: remote, command: 'cd ~/filmproject && source venv/bin/activate && git pull && gunicorn -b 0.0.0.0 "app:create_app()" --daemon'
                        // sshCommand remote: remote, command: 'source venv/bin/activate'
                        // sshCommand remote: remote, command: 'git pull'
                        // sshCommand remote: remote, command: 'gunicorn -b 0.0.0.0 "app:create_app()"'
                    }
                }
            }
        }
    }
}