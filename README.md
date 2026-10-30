# AuthPrivacyChain – Project Execution Guide

## Prerequisites

Install the following tools before running the project:

- Python
- Node.js and npm
- Ganache
- Git
- IPFS

## Step 1: Start the Blockchain

1. Open the project code folder.
2. Navigate to `hello-eth/node_modules/.bin`.
3. Run the `Run Blockchain` file.
4. Once it starts, a Mnemonic phrase will be displayed.
5. Keep this phrase locally for Ganache configuration. Never publish it on GitHub.

## Step 2: Configure Ganache

1. Open Ganache.
2. Select **New Workspace**.
3. Enter your project name.
4. Change the port number to `9545`.
5. Under Account Key, enter the Mnemonic phrase generated in Step 1.
6. Start the workspace.

## Step 3: Deploy the Smart Contract

1. Open Command Prompt in the blockchain project directory.
2. Execute the project's migration command (`migrate` in the original setup instructions).
3. After deployment, two addresses will be displayed.
4. Copy the second address.

## Step 4: Configure the Smart Contract Address

1. Navigate to the `AuthPrivacyChain time based access control` folder.
2. Open `Auth Privacy App`.
3. Open the `Views.py` file.
4. Update the contract address references at lines 133, 159 and 189 with the deployed address.

## Step 5: Start IPFS

1. Navigate to the `AuthPrivacyChain time based access control` project folder.
2. Run the `Start_IPFS` batch file.
3. Keep the IPFS process running.

## Step 6: Start the Application Server

1. In the same project folder, run the `runServer` batch file.
2. Wait for the server to start.

The local server address will be:

`http://127.0.0.1:8000/`

## Step 7: Open the Application

1. Open Google Chrome.
2. Enter the following URL:

`http://127.0.0.1:8000/index.html`

3. The AuthPrivacyChain application will open.

---

**Important:** Ganache, IPFS and the application server should remain running while testing the project.

**Security:** Never upload private Mnemonic phrases, wallet credentials or private keys to GitHub.
