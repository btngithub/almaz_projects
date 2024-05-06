Basic GitLab CI\CD pipeline which tests, builds and deploys a code

Process:
1. Tests the code with predefined tests prepared using make
2. Builds an image from a dockerfile and pushes it to the DockerHub
3. Deploys the image on a server in a docker container
