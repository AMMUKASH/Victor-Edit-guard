# 🛡️ Edit Guardian Bot 🤖

एक एडवांस्ड और सुपर स्टाइलिश टेलीग्राम बॉट जो ग्रुप्स में कॉपीराइट और सिक्योरिटी कंसर्न्स के चलते किसी भी यूजर, एडमिन, ओनर या बॉट द्वारा एडिट किए गए मैसेजेस को तुरंत डिलीट करता है और एक वीआईपी अलर्ट फ्लैश करता है।

---

## 📸 Bot Interface

जब भी कोई ग्रुप में मैसेज एडिट करेगा, बॉट उसे तुरंत डिलीट करके नीचे दिए गए प्रीमियम लेआउट में अलर्ट शो करेगा (जैसा कि फाइल `1000005352.png` में डिज़ाइन किया गया है):

<p align="center">
  <img src="https://files.catbox.moe/9eooj2.jpg" alt="Edit Guardian Bot Start Image" width="600"/>
</p>

---

## ✨ Features

* **⚡ Real-time Detection:** एडमिन, ओनर, मेंबर्स और दूसरे बॉट्स के एडिटेड मैसेज को तुरंत डिटेक्ट करता है।
* **🗑️ Safe Auto-Delete:** ओरिजिनल मैसेज को तुरंत डिलीट करने के बाद, वार्निंग अलर्ट को भी 60 सेकंड में गायब कर देता है ताकि ग्रुप साफ-सुथरा रहे।
* **💎 VIP Styling:** अट्रैक्टिव बॉक्स बॉर्डर और स्टाइलिश फॉन्ट्स के साथ यूजर की पूरी इंफॉर्मेशन (Name, ID, Username) शो करता है।
* **📢 Public Broadcast & Pin:** सभी कनेक्टेड ग्रुप्स में एक साथ मैसेज भेजने और उसे ऑटो-पिन करने की सुविधा।
* **📥 Service Logs:** जब भी बॉट किसी ग्रुप में ऐड होगा (`/addme`) या निकाला जाएगा (`/leave`), तो आपके लॉग ग्रुप में तुरंत अलर्ट जाएगा।
* **🌐 24/7 Alive:** Render पर होस्टिंग के लिए इन-बिल्ट Flask वेब सर्वर जो हमेशा बॉट को एक्टिव रखता है।

---

## 🛠️ Bot Configuration Used

बॉट के अंदर निम्नलिखित क्रेडेंशियल्स प्री-कॉन्फिगर कर दिए गए हैं:

| Configuration | Value |
| :--- | :--- |
| **Bot Username** | `@EditXguardbot` |
| **App API ID** | `38138069` |
| **App API Hash** | `2ed313ebcc45cbcf65d1fc736ec71681` |
| **Log Group ID** | `-1003947649552` |
| **Updates Channel** | [Join Channel](https://t.me/Edit_Guardian_Update) |
| **Support Group** | [Get Support](https://t.me/Genu_Bot_Support) |

---

## 🚀 Deployment Guide (Render + Cron-Jobs)

### 1. GitHub पर कोड पुश करें
अपने प्रोजेक्ट फोल्डर में केवल दो फाइलें रखें:
* `bot.py` (बॉट का मुख्य कोड)
* `requirements.txt` (डिपेंडेंसी लिस्ट)

### 2. Render.com पर सेटअप
1. **Render** पर जाएं और **New +** पर क्लिक करके **Web Service** चुनें।
2. अपनी GitHub रिपॉजिटरी को कनेक्ट करें।
3. नीचे दी गई सेटिंग्स भरें:
   * **Language:** `Python`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `python bot.py`
4. **Advanced -> Add Environment Variable** पर जाएं और यह वेरिएबल जोड़ें:
   * `PORT` = `8080`
5. **Deploy Web Service** पर क्लिक करें।

### 3. Cron-Job.org से 24/7 लाइव रखें
Render का फ्री टियर 15 मिनट बाद सो जाता है। इसे हमेशा जगाए रखने के लिए:
1. अपने Render डैशबोर्ड से लाइव URL कॉपी करें (उदा. `https://your-bot.onrender.com`)।
2. **Cron-job.org** पर जाएं और नया क्रॉन-जॉब बनाएं।
3. URL फील्ड में अपना Render URL पेस्ट करें।
4. शेड्यूल को **Every 5 minutes** पर सेट करें और सेव कर दें।

---

## 📜 Commands Reference

* `/start` - बॉट को शुरू करने और मुख्य स्टाइलिश मेनू देखने के लिए (Private & Public دونوں जगह काम करती है)।
* `/help` - बॉट को ग्रुप में सेट करने की पूरी गाइड देखने के लिए।
* `/broadcast` - किसी भी मैसेज का रिप्लाई करके इस कमांड को देने पर यह सभी ग्रुप्स में ब्रॉडकास्ट करके मैसेज पिन कर देगा।

---
<p align="center">
  Made with ❤️ by <b>Edit Guardian Team</b>
</p>
