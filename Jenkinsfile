pipeline 
{
   agent any
   
   options 
   {
      disableConcurrentBuilds()
      buildDiscarder(logRotator(numToKeepStr: '3'))
   }

   stages
   {
      stage('Prepare') 
      {
         steps 
         {
            sh '''
                    echo "PATH = ${PATH}"
                '''

            git branch: 'main', 
                url: 'https://github.com/glroland/ansible-mcp.git'
         }
      }

      stage('Create Docker Image for ansible-mcp') 
      {
         steps 
         {
            sh 'docker build . --tag ansible-mcp:$BUILD_NUMBER'
            sh 'docker save ansible-mcp:$BUILD_NUMBER > ansible-mcp-dockerimage.tar'
            step(followSymlinks: false, artifacts: 'ansible-mcp-dockerimage.tar', $class: 'ArtifactArchiver')
            sh 'docker rmi ansible-mcp:$BUILD_NUMBER'
         }
      }

      stage('Reload then push images to quay') 
      {
         steps 
         {
            script 
            {
               docker.withRegistry('https://registry.home.glroland.com/', 'quay') 
               {
                  sh 'docker load -i ansible-mcp-dockerimage.tar'
                  sh 'docker tag ansible-mcp:$BUILD_NUMBER registry.home.glroland.com/ai/ansible-mcp:$BUILD_NUMBER'
                  sh 'docker rmi ansible-mcp:$BUILD_NUMBER'
                  sh 'docker push registry.home.glroland.com/ai/ansible-mcp:$BUILD_NUMBER'
                  sh 'docker rmi registry.home.glroland.com/ai/ansible-mcp:$BUILD_NUMBER'
               }
            }
         }
      }
   }
}
