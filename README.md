# Serverless CRUD API for Tasks with AWS CDK

## Prerequisites
1. **Install AWS CLI v2**:
    - Download and install the AWS CLI: [This link](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
    - Configure it with your AWS Credentials:
    ```bash
    aws configure
    ```
2. **Install Node.js**
    - Download and install Nodejs (is required to run AWS CDK): [This link](https://nodejs.org/en/download)
3. **Install Python**
    - Download and install Python 3.12 or higher: [This link](https://www.python.org/downloads/)
4. **Install AWS CDK**
    - Run the next command:
    ```bash
    npm install -g aws-cdk
    ```
## Project Setup
Follow the next steps to set up the project:

1. **Clone the repository**
    ```bash
    git clone https://github.com/blackstar1403/CDKCrudTest.git
    cd CDKCrudTest
    ```
2. **Create and activate a virtual env**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate #For linux
    .venv\Scripts\activate #For Windows
    ```
3. **Install Python dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Bootstrap the CDK environment**
    - It is only need it the first time per environment
    ```bash
    cdk bootstrap --profile <AWS CLI PROFILE>
    ```

## Deployment and Cleaning Instructions
Follow the next steps to deploy the project:
1. **Deploy the stacks**
    - Use the next command to deploy the whole CRUD:
    ```bash
    cdk deploy --all --profile <AWS CLI PROFILE>
    ```
2. **Destroy stacks**
    - Use the next command to destroy the whole infrastructure:
    ```bash
    cdk destroy --all --profile <AWS CLI PROFILE>