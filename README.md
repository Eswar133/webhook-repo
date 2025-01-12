

# Gittracker: Documentation for ngrok and Payload Setup

This guide explains how to use **ngrok** to expose your local Flask app to the internet, how to test the app using **Postman**, how to access it in the browser, and how to handle payloads after the terminal is terminated.

---

## **1. What is ngrok?**

**ngrok** is a tool that creates a secure tunnel from a public endpoint (e.g., `https://<subdomain>.ngrok.io`) to your local machine. It allows you to expose your local development server to the internet, making it accessible to external services like GitHub webhooks.

---

## **2. Setting Up ngrok**

### **Step 1: Install ngrok**
1. Download ngrok from [ngrok.com](https://ngrok.com/download).
2. Install ngrok:
   - On Windows: Unzip the downloaded file and place `ngrok.exe` in a directory.
   - On macOS/Linux: Use the following command:
     ```bash
     npm install -g ngrok
     ```

### **Step 2: Authenticate ngrok**
1. Sign up for an ngrok account at [ngrok.com](https://ngrok.com/).
2. Get your authtoken from the ngrok dashboard.
3. Authenticate ngrok on your machine:
   ```bash
   ngrok authtoken YOUR_AUTH_TOKEN
   ```

### **Step 3: Start ngrok**
1. Start ngrok to expose your Flask app:
   ```bash
   ngrok http 5000
   ```
   - Replace `5000` with the port your Flask app is running on.
2. ngrok will provide a public URL (e.g., `https://e503-223-196-173-127.ngrok-free.app`).

---

## **3. Using ngrok with GitHub Webhooks**

### **Step 1: Update GitHub Webhook**
1. Go to your GitHub repository.
2. Navigate to **Settings** > **Webhooks**.
3. Add a new webhook:
   - **Payload URL**: Use the ngrok URL (e.g., `https://e503-223-196-173-127.ngrok-free.app/webhook`).
   - **Content type**: `application/json`.
   - **Events**: Select `push`, `pull_request`, and `merge`.

### **Step 2: Test the Webhook**
1. Trigger a GitHub action (e.g., push, pull request, merge).
2. Check the ngrok logs to see if the webhook is received:
   ```
   HTTP Requests
   -------------
   10:12:13.388 IST POST /webhook                  200 OK
   ```

---

## **4. Testing with Postman**

### **Step 1: Set Up Postman**
1. Open Postman.
2. Create a new request:
   - **Method**: `POST`.
   - **URL**: `http://localhost:5000/webhook` (or your ngrok URL, e.g., `https://e503-223-196-173-127.ngrok-free.app/webhook`).

### **Step 2: Add Headers**
1. Go to the **Headers** tab.
2. Add a new header:
   - **Key**: `Content-Type`.
   - **Value**: `application/json`.

### **Step 3: Add a Test Payload**
1. Go to the **Body** tab.
2. Select **raw** and set the format to **JSON**.
3. Add a sample payload:
   ```json
   {
     "action": "push",
     "sender": {
       "login": "testuser"
     },
     "ref": "refs/heads/main",
     "head_commit": {
       "id": "12345"
     }
   }
   ```

### **Step 4: Send the Request**
1. Click **Send**.
2. Check the response:
   - You should see a `200 OK` response with:
     ```json
     {
       "status": "success"
     }
     ```

---

## **5. Accessing the App in the Browser**

### **Step 1: Start Flask App**
1. Run your Flask app:
   ```bash
   python app.py
   ```
2. The app will start on `http://127.0.0.1:5000`.

### **Step 2: Access the UI**
1. Open your browser and go to `http://127.0.0.1:5000`.
2. You should see the UI displaying the latest GitHub actions (if any).

---

## **6. Handling Terminal Termination**

When you terminate the terminal, the ngrok tunnel and Flask app will stop running. To ensure your webhook continues to work, follow these steps:

### **Option 1: Run ngrok and Flask in the Background**
1. Use `nohup` to run ngrok and Flask in the background:
   ```bash
   nohup ngrok http 5000 &
   nohup python app.py &
   ```
2. The processes will continue running even after the terminal is closed.

### **Option 2: Use a Process Manager**
1. Use a process manager like **PM2** (for Node.js) or **Supervisor** (for Python) to keep ngrok and Flask running.
2. Example with PM2:
   ```bash
   npm install -g pm2
   pm2 start ngrok -- http 5000
   pm2 start app.py --interpreter python
   ```

### **Option 3: Deploy to a Cloud Service**
1. Deploy your Flask app to a cloud service like **Render**, **Heroku**, or **AWS**.
2. Use the cloud service's URL for your GitHub webhook.

---

## **7. Example Workflow**

### **Step 1: Start ngrok**
```bash
ngrok http 5000
```

### **Step 2: Start Flask App**
```bash
python app.py
```

### **Step 3: Update GitHub Webhook**
- Payload URL: `https://<ngrok-subdomain>.ngrok-free.app/webhook`

### **Step 4: Test the Webhook**
1. Push to your GitHub repository.
2. Check the ngrok logs and Flask app logs to verify the webhook is received.

---

## **8. Troubleshooting**

### **Issue 1: ngrok Tunnel Stops After Terminal Termination**
- **Fix**: Use `nohup` or a process manager to keep ngrok running in the background.

### **Issue 2: Webhook Not Received**
- **Fix**:
  - Ensure ngrok is running and the tunnel is active.
  - Verify the GitHub webhook URL is correct.

### **Issue 3: Flask App Not Running**
- **Fix**:
  - Ensure the Flask app is running on the correct port (e.g., `5000`).
  - Check for errors in the Flask logs.

---

## **9. Conclusion**

- **ngrok** is a powerful tool for exposing local servers to the internet.
- Use **Postman** to test your `/webhook` endpoint.
- Access the app in the browser to view the latest GitHub actions.
- Use background processes or cloud deployment to ensure your webhook remains active after terminal termination.
- Test your setup thoroughly to ensure GitHub webhooks are received and processed correctly.

---
