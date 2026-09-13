git clone https://github.com/bilawalsidhu/gods-eye-view.git
cd gods-eye-view
npm ci
npm run doctor
npm run dev
man Clone-git https://github.com/auraecosystem/flow-tv-experience.git
cd flow-tv-experience
Start the local server:
npm start
const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname)));

app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
    console.log(`📺 Flow TV Server running on http://localhost:${PORT}`);
});
