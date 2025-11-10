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

                        writeFile file: 'kill_bg_gunicorn.sh', text: 'if grep -q "daemon" gunicorn_bg_instances
                                                                      then
                                                                        pkill gunicorn;
                                                                        echo "FOUND";
                                                                      else
                                                                        echo "NOT FOUND";
                                                                      fi'

                        sshPut remote: remote, from: 'kill_bg_gunicorn.sh', into: '.'
                        sshCommand remote: remote, command: 'chmod +777 kill_bg_gunicorn.ssh'

                        sshCommand remote: remote, command: './kill_bg_gunicorn.sh'
                        sshCommand remote: remote, command: 'cd ~/filmproject && source venv/bin/activate && git pull && gunicorn -b 0.0.0.0 "app:create_app()" --daemon'
                    }
                }
            }
        }
    }
}