# 🐾 Cat Facts API

A simple and fun API that returns random cat facts along with optional cat images.
Built using **Python (Flask)** and deployed on **Vercel**.

---

## 🚀 Features

* Returns **random cat facts**
* Organized fact categories
* JSON API responses
* Lightweight & fast backend
* Deployable on **Vercel** (serverless functions)

---

## 📂 Project Structure

```
cat-fact-api/
│
├── app.py                # Main API file (Flask)
├── facts/                # Folder containing fact categories in JSON files
├── static/               # Images folder
├── requirements.txt      # Dependencies
└── vercel.json           # Vercel configuration
```

---

## 🛠 Installation (Local)

1. Clone the repository:

```bash
  git clone https://github.com/your-username/cat-fact-api.git
cd cat-fact-api
```

2. Install dependencies:

```bash
  pip install -r requirements.txt
```

3. Run the API locally:

```bash
  python app.py
```

Your API will be available at:

```
  http://127.0.0.1:5000/
```

---

## 🌐 API Endpoints

### **Get random cat fact**

```
  GET /api/fact
```

**Example response:**

```json
{
    "fact": "Cats sleep for 70% of their lives."
}
```

### **Get random fact from a category**

```
  GET /api/fact/<category>
```

Example:

```
  /api/fact/sleep
```

---

## 📦 Deploying on Vercel

1. Install Vercel CLI:

```bash
npm i -g vercel
```

2. Deploy:

```bash
vercel
```

3. For production:

```bash
vercel --prod
```

---

## 🧩 vercel.json Example

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

---

## 📸 Example Output

![Cat Image](https://placekitten.com/300/200)

---

## 🤝 Contributing

Pull requests are welcome!
If you have new cat facts or new fact categories, feel free to contribute.

---

## ⭐️ Support:

If you like this project, consider giving it a **star ⭐ on GitHub** — it helps a lot!

---

## 🐈 Made With Love

Made by **Muhammed Murshid ts** 🖤
*Because cats deserve their own API.*
✅ Add installation GIF
Just tell me!
