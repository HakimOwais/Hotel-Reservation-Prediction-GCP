pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = 'my-project-01-452610'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'

    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins ......'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/HakimOwais/Hotel-Reservation-Prediction-GCP.git']])
                }
            }
        }

        stage('Setting up Virtual Environment and Installing dependencies'){
            steps{
                script{
                    echo 'Setting up Virtual Environment and Installing dependencies ......'
                    sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                    }
            }
        }

        stage('Building and pushing docker image to Google cloud registry'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script {
                        echo 'Building and pushing docker image to Google cloud registry .......'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker buildx create --use
                        docker buildx build --platform linux/amd64 -t gcr.io/${GCP_PROJECT}/ml-project:latest --push .
                        '''
                    }
                }
            }
        }

        stage('Deploy to Google Cloud Run'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Deploy to Google Cloud Run.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}


                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy ml-project \
                            --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
                            --platform=managed \
                            --region=us-central1 \
                            --allow-unauthenticated
                            
                        '''
                    }
                }
            }
        }
    }
}