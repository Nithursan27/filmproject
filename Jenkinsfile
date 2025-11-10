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

                        // writeFile file: 'kill_bg_gunicorn.sh', text: '''\
                        // ps aux | grep gunicorn > gunicorn_bg_instances
                        // if grep -q "daemon" gunicorn_bg_instances
                        // then
                        //     pkill gunicorn;
                        //     echo "FOUND";
                        // else
                        //     echo "NOT FOUND";
                        // fi'''

                        // sshPut remote: remote, from: 'kill_bg_gunicorn.sh', into: '.'
                        // sshCommand remote: remote, command: 'chmod +x kill_bg_gunicorn.sh'

                        // sshCommand remote: remote, command: './kill_bg_gunicorn.sh'
                        sshCommand remote: remote, command: 'pkill gunicorn || cd ~/filmproject && source venv/bin/activate && git pull && pip install -r requirements.txt && gunicorn -b 0.0.0.0 "app:create_app()" --daemon'
                    }
                }
            }
        }
    }
}