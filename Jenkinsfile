pipeline {
  agent {
    node {
      label 'any'
    }
    
  }
  stages {
    stage('build') {
      parallel {
        stage('build') {
          steps {
            sh 'python --version'
          }
        }
        stage('Naor') {
          steps {
            echo 'naor!!'
          }
        }
      }
    }
  }
}