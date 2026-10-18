<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Hub Mini App</title>
    <!-- টেলিগ্রাম Web App এর অফিশিয়াল স্ক্রিপ্ট -->
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <!-- আপনার অ্যাড নেটওয়ার্কের স্ক্রিপ্ট (যেমন Monetag / Adsterra) এখানে বসাবেন -->
    <script src="YOUR_AD_SCRIPT_HERE"></script>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #fff; padding: 15px; text-align: center; margin: 0; }
        .video-card { background: #1e293b; padding: 15px; margin: 10px 0; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155; }
        .watch-btn { background: #3b82f6; color: white; padding: 10px 15px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
        .watch-btn:active { background: #2563eb; }
    </style>
</head>
<body>
    <h2>🎬 Video Hub</h2>
    <p>পছন্দের ভিডিওতে ক্লিক করে চ্যাটে আনুন:</p>

    <!-- ভিডিও লিস্ট -->
    <div class="video-card">
        <span>⭐ Premium Video</span>
        <button class="watch-btn" onclick="requestVideo('vid_1')">Watch</button>
    </div>
    <div class="video-card">
        <span>🌍 English Video</span>
        <button class="watch-btn" onclick="requestVideo('vid_2')">Watch</button>
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand(); // অ্যাপটি ফুল স্ক্রিন করবে

        function requestVideo(videoId) {
            // অ্যাড শো হওয়ার পর পাইথন বটের কাছে ডেটা পাঠিয়ে মিনি অ্যাপ বন্ধ করে দেবে
            alert('বিজ্ঞাপন শেষ হলে ভিডিওটি আপনার টেলিগ্রাম চ্যাটে পাঠানো হবে!');
            tg.sendData(videoId); 
        }
    </script>
</body>
</html>
